import asyncio

from pychonet.lib.const import (
    ENL_GETMAP,
    ENL_MANUFACTURER,
    ENL_PRODUCT_CODE,
    ENL_PORT,
    INSTANCE_LIST,
    ENL_SETMAP,
    ENL_UID,
    GET,
    MESSAGE_TIMEOUT,
    ENL_STATMAP,
    SETRES,
    GETRES,
    INF,
    INFC,
    SETC_SND,
    GET_SNA,
    INF_SNA,
    SETI,
    SETC,
    ENL_MULTICAST_ADDRESS,
)
from pychonet.lib.epc_functions import EPC_SUPER_FUNCTIONS
from pychonet.lib.functions import TIDError, buildEchonetMsg, decodeEchonetMsg


class ECHONETAPIClient:
    def __init__(self, server):
        self._server = server
        self._logger = print
        self._server.subscribe(self.echonetMessageReceived)
        self._state = {}
        self._next_tx_tid = 0x0000
        self._message_list = {}
        self._failure_list = {}
        self._opc_counts = {}
        self._message_timeout = MESSAGE_TIMEOUT
        self._debug_flag = False
        self._update_callbacks = {}
        self._discover_callback = None
        self._waiting = {}

    async def echonetMessageReceived(self, raw_data, addr):
        updated = False
        host = addr[0]
        is_discovery = False

        if self._debug_flag:
            self._logger(
                f"ECHONETLite Message Received from {host} - Raw data is {raw_data}"
            )

        processed_data = decodeEchonetMsg(raw_data)

        if self._debug_flag:
            self._logger(
                f"ECHONETLite Message Received from {host} - Processed data is {processed_data}"
            )

        tid = processed_data["TID"]
        tid_data = self._message_list.get(tid)

        if self._debug_flag:
            self._logger(
                f"ECHONETLite Message Received from {host} - tid_data is {tid_data}"
            )

        isPush = tid_data is None
        seojgc = processed_data["SEOJGC"]
        seojcc = processed_data["SEOJCC"]
        seojci = processed_data["SEOJCI"]
        esv = processed_data["ESV"]

        if self._state.get(host) is None:  # echonet packet arrived we dont know about
            self._logger(f"Unknown ECHONETLite node has been identified - {host}")
            if callable(self._discover_callback):
                if self._debug_flag:
                    self._logger(f"Called _discover_callback('{host}')")
                await self._discover_callback(host)
            return

        key = f"{host}-{seojgc}-{seojcc}-{seojci}"
        esv_set = esv in [SETRES, SETC_SND]
        esv_get = esv in [GETRES, GET_SNA, INF, INF_SNA, INFC]
        if not isPush:
            self._failure_list[tid] = 0
            self._opc_counts[tid] = len(processed_data["OPC"])
        # handle discovery message response
        for opc in processed_data["OPC"]:
            epc = opc["EPC"]
            if seojgc == 0x0E and seojcc == 0xF0:  # Node Profile Class Response
                if epc in [
                    INSTANCE_LIST,
                    ENL_MANUFACTURER,
                    ENL_PRODUCT_CODE,
                    ENL_UID,
                ]:  # process discovery data
                    is_discovery = True
                    await self.process_discovery_data(host, opc)
                else:
                    # @todo handling others
                    """
                    Ex. 0x05: Instance list notification
                    A property to announce the configuration of instances to be disclosed to the network at startup.
                    This property also announces instances held at the self-node each time the configuration of
                    instances disclosed to the network is changed during system operation, such as instance
                    addition or deletion.
                    """
                    """
                    It is desirable to dynamically add and delete entities when there is an increase
                    or decrease in the number of instances within a device already configured with HA,
                    but that will be an issue for the future.
                    """
                    continue
            elif seojgc == 0x0F:  # User definition class group
                if self._debug_flag:
                    self._logger(
                        f"Packet received from {host} for user definition class group 0x0F"
                    )
                    self._logger(f"Full packet details are {processed_data}")
                    self._logger(f"ignoring packet but please notify devs on Github.")
            else:  # process each EPC in order
                if epc == ENL_SETMAP or epc == ENL_GETMAP or epc == ENL_STATMAP:
                    map = EPC_SUPER_FUNCTIONS[epc](opc["EDT"])
                    self._state[host]["instances"][seojgc][seojcc][seojci][epc] = map
                elif epc in (ENL_UID, ENL_MANUFACTURER, ENL_PRODUCT_CODE):
                    try:
                        self._state[host]["instances"][seojgc][seojcc][seojci][
                            epc
                        ] = EPC_SUPER_FUNCTIONS[epc](opc["EDT"])
                    except KeyError as e:
                        if self._debug_flag:
                            self._logger(
                                f"ECHONET _state _key error {e} of {host} this packet contains the following data: {processed_data}"
                            )
                        continue
                        # raise Exception(
                        #     f"ECHONET Packet contains the following data: {processed_data}"
                        # )
                else:
                    if esv_set:
                        if opc["PDC"] > 0 or isPush:
                            if not isPush:
                                self._failure_list[tid] += 1
                            continue
                        if tid_data.get(epc) is None:
                            self._failure_list[tid] += 1
                            if self._debug_flag:
                                self._logger(
                                    f"EDT is not set in send data for EPC '{epc}' - process each EPC"
                                )
                            continue
                        else:
                            # set request data
                            opc["EDT"] = tid_data[epc]
                    elif esv_get:
                        if opc["PDC"] == 0:
                            if not isPush:
                                self._failure_list[tid] += 1
                            continue
                    else:
                        # @todo more esv support
                        continue

                    if (
                        epc
                        not in self._state[host]["instances"][seojgc][seojcc][seojci]
                        or self._state[host]["instances"][seojgc][seojcc][seojci][epc]
                        != opc["EDT"]
                    ):
                        updated = True
                    self._state[host]["instances"][seojgc][seojcc][seojci][epc] = opc[
                        "EDT"
                    ]

        # Markup "discovered"
        if is_discovery and len(self._state[host]["instances"]):
            if self._state[host].get("uid") is None:
                self._state[host]["uid"] = EPC_SUPER_FUNCTIONS[ENL_UID](b"", host)
            if self._state[host].get("manufacturer") is None:
                self._state[host]["manufacturer"] = EPC_SUPER_FUNCTIONS[
                    ENL_MANUFACTURER
                ](0xFFFFFF.to_bytes(3, "big"))
            self._state[host]["discovered"] = True

        # Markup "available"
        _to_available = False
        if host in self._state:
            if not self._state[host].get("available"):
                _to_available = True
                self._state[host]["available"] = True

        if _to_available:
            # Call update callback functions
            # key is f"{host}-{deojgc}-{deojcc}-{deojci}"
            for _key in self._update_callbacks:
                if _key.startswith(host):
                    for update_func in self._update_callbacks[_key]:
                        await update_func(False)
        else:
            # Call update callback functions
            if updated and key in self._update_callbacks:
                for update_func in self._update_callbacks[key]:
                    await update_func(isPush)

        # if we get duplicate packets that have already been processed then dont worry about the message list.
        # but still process them regardless.
        if tid_data is not None:
            del self._message_list[tid]

    async def discover(self, host=ENL_MULTICAST_ADDRESS):
        if host is ENL_MULTICAST_ADDRESS:
            opc = [{"EPC": INSTANCE_LIST}]
        else:
            opc = [
                {"EPC": ENL_MANUFACTURER},
                {"EPC": ENL_PRODUCT_CODE},
                {"EPC": ENL_UID},
                {"EPC": INSTANCE_LIST},
            ]
        return await self.echonetMessage(host, 0x0E, 0xF0, 0x01, GET, opc)

    async def echonetMessage(self, host, deojgc, deojcc, deojci, esv, opc):
        no_res = True if esv is SETI else False
        payload = None
        # Is node profile
        is_node_profile = deojgc == 0x0E and deojcc == 0xF0
        map_epcs = {ENL_STATMAP, ENL_GETMAP, ENL_SETMAP}
        # Check OPC Code
        try:
            if not is_node_profile:
                if esv == GET:
                    check_map = set(
                        self._state[host]["instances"][deojgc][deojcc][deojci].get(
                            ENL_GETMAP, []
                        )
                    )
                    check_map |= map_epcs
                elif esv == SETC:
                    check_map = set(
                        self._state[host]["instances"][deojgc][deojcc][deojci].get(
                            ENL_SETMAP, []
                        )
                    )
                else:
                    check_map = {}
                if len(check_map):
                    checked_opc = []
                    for values in opc:
                        if values.get("EPC") in check_map:
                            checked_opc.append(values)
                    opc = checked_opc
        except KeyError:
            pass

        message_array = {
            "DEOJGC": deojgc,
            "DEOJCC": deojcc,
            "DEOJCI": deojci,
            "ESV": esv,
            "OPC": opc,
        }
        if self._state.get(host) is None:
            self._state[host] = {"instances": {}, "available": True}

        # Consecutive requests to the device must wait for a response
        if self._waiting.get(host) is None:
            self._waiting[host] = 0
        if self._waiting[host] > 0:
            for x in range(0, self._message_timeout):
                # Wait up to 20(0.1*200) seconds depending on the Echonet specifications.
                await asyncio.sleep(0.1)
                if not self._waiting[host]:
                    break
            if self._waiting[host]:
                return False
        self._waiting[host] += 1

        self._next_tx_tid += 1
        tx_tid = self._next_tx_tid
        message_array["TID"] = tx_tid
        try:
            payload = buildEchonetMsg(message_array)
        except TIDError:  # Quashing the rollover bug hopefully once and for all...
            self._next_tx_tid = 1
            tx_tid = self._next_tx_tid
            message_array["TID"] = tx_tid
            payload = buildEchonetMsg(message_array)

        opc_count = len(opc)
        if no_res:
            is_success = True
        else:
            is_success = False
            tid_data = {}
            for opc_data in opc:
                if opc_data.get("EDT") is not None:
                    if isinstance(opc_data["EDT"], int):
                        tid_data[opc_data["EPC"]] = opc_data["EDT"].to_bytes(
                            opc_data["PDC"], "big"
                        )
            self._message_list[tx_tid] = tid_data

        self._server.send(payload, (host, ENL_PORT))

        if not no_res:
            not_timeout = False
            for x in range(0, self._message_timeout):
                # Wait up to 20(0.1*200) seconds depending on the Echonet specifications.
                await asyncio.sleep(0.1)
                # if tx_tid is not in message list then the message listener has received the message
                if self._message_list.get(tx_tid) is None:
                    # Check OPC count in results
                    if not is_node_profile and tx_tid in self._opc_counts:
                        res_opc_count = self._opc_counts[tx_tid]
                        del self._opc_counts[tx_tid]
                        if self._debug_flag:
                            self._logger(
                                f"OPC count in results is {res_opc_count}/{opc_count} from IP {host}."
                            )
                        if res_opc_count < opc_count:
                            self._waiting[host] -= 1
                            raise EchonetMaxOpcError(res_opc_count)

                    # transaction sucessful remove from list
                    if self._failure_list.get(tx_tid, opc_count) < opc_count:
                        is_success = True
                    if tx_tid in self._failure_list:
                        del self._failure_list[tx_tid]
                    not_timeout = True
                    break
            self._waiting[host] -= 1
            if not is_success:
                if self._message_list.get(tx_tid) is not None:
                    del self._message_list[tx_tid]
            if self._state[host]["available"] != not_timeout:
                self._state[host]["available"] = not_timeout
                # Call update callback functions
                # key is f"{host}-{deojgc}-{deojcc}-{deojci}"
                for key in self._update_callbacks:
                    if key.startswith(host):
                        for update_func in self._update_callbacks[key]:
                            await update_func(False)
        else:
            self._waiting[host] -= 1
        return is_success

    async def getAllPropertyMaps(self, host, eojgc, eojcc, eojci):
        return await self.echonetMessage(
            host,
            eojgc,
            eojcc,
            eojci,
            GET,
            [
                {"EPC": ENL_STATMAP},
                {"EPC": ENL_GETMAP},
                {"EPC": ENL_SETMAP},
            ],
        )

    async def getIdentificationInformation(self, host, eojgc, eojcc, eojci):
        return await self.echonetMessage(
            host,
            eojgc,
            eojcc,
            eojci,
            GET,
            [{"EPC": ENL_UID}, {"EPC": ENL_MANUFACTURER}],
        )

    async def process_discovery_data(self, host, opc_data):
        if "discovered" not in self._state[host]:
            if opc_data["EPC"] == ENL_UID:
                self._state[host]["uid"] = EPC_SUPER_FUNCTIONS[ENL_UID](
                    opc_data["EDT"], host
                )
            elif opc_data["EPC"] == ENL_MANUFACTURER:
                self._state[host]["manufacturer"] = EPC_SUPER_FUNCTIONS[
                    ENL_MANUFACTURER
                ](opc_data["EDT"])
            elif opc_data["EPC"] == ENL_PRODUCT_CODE:
                self._state[host]["product_code"] = EPC_SUPER_FUNCTIONS[
                    ENL_PRODUCT_CODE
                ](opc_data["EDT"])
            else:
                edt = bytearray(opc_data["EDT"])
                # 1st byte: Total number of instances
                # 2nd to 253rd bytes: ECHONET object codes (EOJ3 bytes) enumerated
                edtnum = bytearray(edt)[0]
                for x in range(edtnum):
                    eojgc = bytearray(edt)[1 + (3 * x)]
                    eojcc = bytearray(edt)[2 + (3 * x)]
                    eojci = bytearray(edt)[3 + (3 * x)]
                    if eojgc != 0x0F:  # ignore this group code.
                        # populate state table
                        if eojgc not in list(self._state[host]["instances"].keys()):
                            self._state[host]["instances"].update({eojgc: {}})
                        if eojcc not in list(
                            self._state[host]["instances"][eojgc].keys()
                        ):
                            self._state[host]["instances"][eojgc].update({eojcc: {}})
                        if eojci not in list(
                            self._state[host]["instances"][eojgc][eojcc].keys()
                        ):
                            self._state[host]["instances"][eojgc][eojcc][eojci] = {}
                            self._state[host]["instances"][eojgc][eojcc][eojci].update(
                                {ENL_STATMAP: []}
                            )
                            self._state[host]["instances"][eojgc][eojcc][eojci].update(
                                {ENL_SETMAP: []}
                            )
                            self._state[host]["instances"][eojgc][eojcc][eojci].update(
                                {ENL_GETMAP: []}
                            )

    def register_async_update_callbacks(self, host, eojgc, eojcc, eojci, fn):
        key = f"{host}-{eojgc}-{eojcc}-{eojci}"
        if key not in self._update_callbacks:
            self._update_callbacks[key] = []
        self._update_callbacks[key].append(fn)


class EchonetMaxOpcError(Exception):
    pass
