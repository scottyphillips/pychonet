import asyncio

from pychonet.lib.const import (ENL_GETMAP, ENL_MANUFACTURER, ENL_PORT, INSTANCE_LIST,
                                ENL_SETMAP, ENL_UID, GET, MESSAGE_TIMEOUT, ENL_STATMAP,
                                SETRES, GETRES, INF, INFC, SETC_SND, GET_SNA, INF_SNA)
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

    async def echonetMessageReceived(self, raw_data, addr):
        updated = False
        host = addr[0]
        processed_data = decodeEchonetMsg(raw_data)
        tid = processed_data["TID"]
        tid_data = self._message_list.get(tid)
        isPush = not tid_data
        if self._debug_flag:
            self._logger(f"ECHONETLite Message Received - Processed data is {processed_data}")
        seojgc = processed_data["SEOJGC"]
        seojcc = processed_data["SEOJCC"]
        seojci = processed_data["SEOJCI"]
        esv = processed_data["ESV"]
        key = f"{host}-{seojgc}-{seojcc}-{seojci}"
        esv_set = esv in [SETRES, SETC_SND]
        esv_get = esv in [GETRES, GET_SNA, INF, INF_SNA, INFC]
        # handle discovery message response
        for opc in processed_data["OPC"]:
            epc = opc["EPC"]
            if seojgc == 0x0E and seojcc == 0xF0:
                if (epc in [INSTANCE_LIST, ENL_MANUFACTURER, ENL_UID]): # process discovery data
                    await self.process_discovery_data(host, opc)
                else:
                    # @todo handling others (0x05: Notify of change instance list, etc...)
                    continue
            elif host not in self._state: # echonet packet arrived we dont know about
                if self._debug_flag:
                    self._logger(f"Unknown ECHONETLite node has been identified at {host} - discovery packet fired")
                # await self.discover(host)
            else: # process each EPC in order
                if epc == ENL_SETMAP or epc == ENL_GETMAP or epc == ENL_STATMAP:
                    map = EPC_SUPER_FUNCTIONS[epc](opc["EDT"])
                    self._state[host]["instances"][seojgc][seojcc][seojci][epc] = map
                elif epc in (ENL_UID, ENL_MANUFACTURER):
                    self._state[host]["instances"][seojgc][seojcc][seojci][
                        epc
                    ] = EPC_SUPER_FUNCTIONS[epc](opc["EDT"])
                else: # Check for responses to ignore
                    if esv_set:
                        if opc["PDC"] > 0 or tid_data is None:
                            if tid_data:
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
                            if tid_data:
                                self._failure_list[tid] = True
                            continue
                    else:
                        # @todo more esv support
                        continue

                    if epc not in self._state[host]["instances"][seojgc][seojcc][seojci] or self._state[host]["instances"][seojgc][seojcc][seojci][epc] != opc["EDT"]:
                        updated = True
                    self._state[host]["instances"][seojgc][seojcc][seojci][epc] = opc["EDT"]

        # Call update callback functions
        if updated and key in self._update_callbacks:
            for update_func in self._update_callbacks[key]:
                await update_func(isPush)

        # if we get duplicate packets that have already been processed then dont worry about the message list.
        # but still process them regardless.
        if tid_data:
            del self._message_list[tid]

    async def discover(self, host="224.0.23.0"):
        return await self.echonetMessage(host, 0x0E, 0xF0, 0x00, GET, [
            {"EPC": ENL_MANUFACTURER},
            {"EPC": ENL_UID},
            {"EPC": INSTANCE_LIST}
        ])

    async def echonetMessage(self, host, deojgc, deojcc, deojci, esv, opc):
        payload = None
        message_array = {
            "DEOJGC": deojgc,
            "DEOJCC": deojcc,
            "DEOJCI": deojci,
            "ESV": esv,
            "OPC": opc,
        }
        if host not in list(self._state.keys()):
            self._state[host] = {"instances": {}}

        tid_data = {}
        for opc_data in opc:
            if opc_data.get("EDT") is not None:
                if isinstance(opc_data["EDT"], int):
                    tid_data[opc_data["EPC"]] = opc_data["EDT"].to_bytes(opc_data["PDC"], 'big')

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

        self._message_list[tx_tid] = tid_data
        self._server.send(payload, (host, ENL_PORT))
        for x in range(0, self._message_timeout):
            # Wait up to 20(0.1*200) seconds depending on the Echonet specifications.
            await asyncio.sleep(0.1)
            # if tx_tid is not in message list then the message listener has received the message
            if not self._message_list.get(tx_tid):
                # transaction sucessful remove from list
                if not self._failure_list.get(tx_tid):
                    res = True
                else:
                    res = False
                    del self._failure_list[tx_tid]
                return res
        del self._message_list[tx_tid]
        return False

    async def getAllPropertyMaps(self, host, eojgc, eojcc, eojci):
        return await self.echonetMessage(
            host, eojgc, eojcc, eojci, GET, [{"EPC": ENL_STATMAP}, {"EPC": ENL_GETMAP}, {"EPC": ENL_SETMAP}]
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
                self._state[host]['uid'] = EPC_SUPER_FUNCTIONS[ENL_UID](opc_data["EDT"])
            elif opc_data["EPC"] == ENL_MANUFACTURER:
                self._state[host]['manufacturer'] = EPC_SUPER_FUNCTIONS[ENL_MANUFACTURER](opc_data["EDT"])
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
            if self._state[host].get('uid') != None and self._state[host].get('manufacturer') != None and len(self._state[host]["instances"]):
                self._state[host]["discovered"] = True

    def register_async_update_callbacks(self, host, eojgc, eojcc, eojci, fn):
        key = f"{host}-{eojgc}-{eojcc}-{eojci}"
        if key not in self._update_callbacks:
            self._update_callbacks[key] = []
        self._update_callbacks[key].append(fn)
