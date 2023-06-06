import asyncio

from pychonet.lib.const import (ENL_GETMAP, ENL_MANUFACTURER, ENL_PRODUCT_CODE, ENL_PORT, INSTANCE_LIST,
                                ENL_SETMAP, ENL_UID, GET, MESSAGE_TIMEOUT, ENL_STATMAP,
                                SETRES, GETRES, INF, INFC, SETC_SND, GET_SNA, INF_SNA,
                                SETI, ENL_MULTICAST_ADDRESS)
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
            self._logger(f"ECHONETLite Message Received from {host} - Raw data is {raw_data}")

        processed_data = decodeEchonetMsg(raw_data)

        if self._debug_flag:
            self._logger(f"ECHONETLite Message Received from {host} - Processed data is {processed_data}")

        tid = processed_data["TID"]
        tid_data = self._message_list.get(tid)

        if self._debug_flag:
            self._logger(f"ECHONETLite Message Received from {host} - tid_data is {tid_data}")

        isPush = tid_data is None
        seojgc = processed_data["SEOJGC"]
        seojcc = processed_data["SEOJCC"]
        seojci = processed_data["SEOJCI"]
        esv = processed_data["ESV"]

        if self._state.get(host) is None: # echonet packet arrived we dont know about
            self._logger(f"Unknown ECHONETLite node has been identified - {host}")
            if callable(self._discover_callback):
                if self._debug_flag:
                    self._logger(f"Called _discover_callback('{host}')")
                await self._discover_callback(host)
            return

        key = f"{host}-{seojgc}-{seojcc}-{seojci}"
        esv_set = esv in [SETRES, SETC_SND]
        esv_get = esv in [GETRES, GET_SNA, INF, INF_SNA, INFC]
        # handle discovery message response
        for opc in processed_data["OPC"]:
            epc = opc["EPC"]
            if seojgc == 0x0E and seojcc == 0xF0: # Node Profile Class Response
                if (epc in [INSTANCE_LIST, ENL_MANUFACTURER, ENL_PRODUCT_CODE, ENL_UID]): # process discovery data
                    is_discovery = True
                    await self.process_discovery_data(host, opc)
                else:
                    # @todo handling others
                    '''
                    Ex. 0x05: Instance list notification
                    A property to announce the configuration of instances to be disclosed to the network at startup.
                    This property also announces instances held at the self-node each time the configuration of
                    instances disclosed to the network is changed during system operation, such as instance
                    addition or deletion.
                    '''
                    '''
                    It is desirable to dynamically add and delete entities when there is an increase
                    or decrease in the number of instances within a device already configured with HA,
                    but that will be an issue for the future.
                    '''
                    continue
            else: # process each EPC in order
                if epc == ENL_SETMAP or epc == ENL_GETMAP or epc == ENL_STATMAP:
                    map = EPC_SUPER_FUNCTIONS[epc](opc["EDT"])
                    self._state[host]["instances"][seojgc][seojcc][seojci][epc] = map
                elif epc in (ENL_UID, ENL_MANUFACTURER, ENL_PRODUCT_CODE):
                    self._state[host]["instances"][seojgc][seojcc][seojci][
                        epc
                    ] = EPC_SUPER_FUNCTIONS[epc](opc["EDT"])
                else: # Check for responses to ignore
                    if esv_set:
                        if opc["PDC"] > 0 or isPush:
                            if not isPush:
                                self._failure_list[tid] = True
                            continue
                        if tid_data.get(epc) is None:
                            self._failure_list[tid] = True
                            if self._debug_flag:
                                self._logger(f"EDT is not set in send data for EPC '{epc}' - process each EPC")
                            continue
                        else:
                            # set request data
                            opc["EDT"] = tid_data[epc]
                    elif esv_get:
                        if opc["PDC"] == 0:
                            if tid_data is not None:
                                self._failure_list[tid] = True
                            continue
                    else:
                        # @todo more esv support
                        continue

                    if epc not in self._state[host]["instances"][seojgc][seojcc][seojci] or self._state[host]["instances"][seojgc][seojcc][seojci][epc] != opc["EDT"]:
                        updated = True
                    self._state[host]["instances"][seojgc][seojcc][seojci][epc] = opc["EDT"]

        # Markup "discovered"
        if is_discovery and len(self._state[host]["instances"]):
            if self._state[host].get('uid') is None:
                self._state[host]['uid'] = EPC_SUPER_FUNCTIONS[ENL_UID](b'', host)
            if self._state[host].get('manufacturer') is None:
                self._state[host]['manufacturer'] = EPC_SUPER_FUNCTIONS[ENL_MANUFACTURER](0xFFFFFF.to_bytes(3, 'big'))
            self._state[host]["discovered"] = True

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
                {"EPC": INSTANCE_LIST}
            ]
        return await self.echonetMessage(host, 0x0E, 0xF0, 0x01, GET, opc)

    async def echonetMessage(self, host, deojgc, deojcc, deojci, esv, opc):
        no_res = True if esv is SETI else False
        payload = None
        message_array = {
            "DEOJGC": deojgc,
            "DEOJCC": deojcc,
            "DEOJCI": deojci,
            "ESV": esv,
            "OPC": opc,
        }
        if self._state.get(host) is None:
            self._state[host] = {"instances": {}}

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

        if no_res:
            result = True
        else:
            result = False
            tid_data = {}
            for opc_data in opc:
                if opc_data.get("EDT") is not None:
                    if isinstance(opc_data["EDT"], int):
                        tid_data[opc_data["EPC"]] = opc_data["EDT"].to_bytes(opc_data["PDC"], 'big')
            self._message_list[tx_tid] = tid_data

        self._server.send(payload, (host, ENL_PORT))

        if not no_res:
            for x in range(0, self._message_timeout):
                # Wait up to 20(0.1*200) seconds depending on the Echonet specifications.
                await asyncio.sleep(0.1)
                # if tx_tid is not in message list then the message listener has received the message
                if self._message_list.get(tx_tid) is None:
                    # transaction sucessful remove from list
                    if self._failure_list.get(tx_tid) is None:
                        result = True
                    else:
                        del self._failure_list[tx_tid]
                    break
            if not result and self._message_list.get(tx_tid) is not None:
                del self._message_list[tx_tid]

        self._waiting[host] -= 1
        return result

    async def getAllPropertyMaps(self, host, eojgc, eojcc, eojci):
        return await self.echonetMessage(
            host, eojgc, eojcc, eojci, GET, [{"EPC": ENL_STATMAP}, {"EPC": ENL_GETMAP}, {"EPC": ENL_SETMAP}, {"EPC": ENL_PRODUCT_CODE}]
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
                self._state[host]['uid'] = EPC_SUPER_FUNCTIONS[ENL_UID](opc_data["EDT"], host)
            elif opc_data["EPC"] == ENL_MANUFACTURER:
                self._state[host]['manufacturer'] = EPC_SUPER_FUNCTIONS[ENL_MANUFACTURER](opc_data["EDT"])
            elif opc_data["EPC"] == ENL_PRODUCT_CODE:
                self._state[host]['product_code'] = EPC_SUPER_FUNCTIONS[ENL_PRODUCT_CODE](opc_data["EDT"])
            else:
                edt = bytearray(opc_data["EDT"])
                # 1st byte: Total number of instances
                # 2nd to 253rd bytes: ECHONET object codes (EOJ3 bytes) enumerated
                edtnum = bytearray(edt)[0]
                for x in range(edtnum):
                    eojgc = bytearray(edt)[1 + (3 * x)]
                    eojcc = bytearray(edt)[2 + (3 * x)]
                    eojci = bytearray(edt)[3 + (3 * x)]
                    if eojgc != 0x0F: # ignore this group code.
                        # populate state table
                        if eojgc not in list(self._state[host]["instances"].keys()):
                            self._state[host]["instances"].update({eojgc: {}})
                        if eojcc not in list(self._state[host]["instances"][eojgc].keys()):
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
