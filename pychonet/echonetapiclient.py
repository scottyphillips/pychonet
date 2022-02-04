import asyncio
import datetime

from aioudp import UDPServer
# import socket
import struct
import sys
import time
from pychonet.lib.const import GET, MESSAGE_TIMEOUT
from pychonet.lib.functions import decodeEchonetMsg, buildEchonetMsg, preparePayload, TIDError
from pychonet.lib.eojx import EOJX_GROUP, EOJX_CLASS
from pychonet.lib.const import ENL_STATUS, ENL_UID, ENL_SETMAP, ENL_GETMAP, ENL_PORT, ENL_MANUFACTURER
from pychonet.lib.epc_functions import EPC_SUPER_FUNCTIONS
from pychonet.lib.epc import EPC_CODE, EPC_SUPER


class ECHONETAPIClient:
    def __init__(self, server, loop):
        self._server = server
        self._loop = loop
        self._server.subscribe(self.echonetMessageReceived)
        self._state = {}
        self._next_tx_tid = 0x0000
        self._message_list = []
        self._message_timeout = MESSAGE_TIMEOUT
        self._debug_flag = False

    async def echonetMessageReceived(self, raw_data, addr):
        host = addr[0]
        processed_data = decodeEchonetMsg(raw_data)
        if self._debug_flag == True:
            print(
                f"Echonet Message Received - Processed data is {processed_data}")
        # if we get duplicate packets that have already been processed then dont worry about the message list.
        # but still process them regardless.
        if processed_data["TID"] in self._message_list:
            self._message_list.remove(processed_data["TID"])
        # handle discovery message response
        for opc in processed_data['OPC']:
            seojgc = processed_data['SEOJGC']
            seojcc = processed_data['SEOJCC']
            seojci = processed_data['SEOJCI']
            epc = opc['EPC']
            if seojgc == 14 and seojcc == 240 and epc == 0xd6:
                await self.process_discovery_data(host, opc)
            else:
                if epc == ENL_SETMAP:
                    map = EPC_SUPER_FUNCTIONS[epc](opc['EDT'])
                    self._state[host]["instances"][seojgc][seojcc][seojci][epc] = map
                elif epc == ENL_GETMAP:
                    map = EPC_SUPER_FUNCTIONS[epc](opc['EDT'])
                    self._state[host]["instances"][seojgc][seojcc][seojci][epc] = map
                elif epc in (ENL_UID, ENL_MANUFACTURER):
                    self._state[host]["instances"][seojgc][seojcc][seojci][epc] = EPC_SUPER_FUNCTIONS[epc](
                        opc['EDT'])
                else:
                    self._state[host]["instances"][seojgc][seojcc][seojci][epc] = opc['EDT']

    async def discover(self, host="224.0.23.0"):
        return await self.echonetMessage(host, 0x0E, 0xF0, 0x00, GET, [{'EPC': 0xD6}])

    async def echonetMessage(self, host, deojgc, deojcc, deojci, esv, opc):
        payload = None
        message_array = {
            'DEOJGC': deojgc,
            'DEOJCC': deojcc,
            'DEOJCI': deojci,
            'ESV': esv,
            'OPC': opc
        }
        if host not in list(self._state.keys()):
            self._state[host] = {"instances": {}}

        self._next_tx_tid += 1
        tx_tid = self._next_tx_tid
        message_array['TID'] = tx_tid
        try:
            payload = buildEchonetMsg(message_array)
        except TIDError:  # Quashing the rollover bug hopefully once and for all...
            self._next_tx_tid = 1
            tx_tid = self._next_tx_tid
            message_array['TID'] = tx_tid
            payload = buildEchonetMsg(message_array)

        self._message_list.append(tx_tid)
        self._server.send(payload, (host, ENL_PORT))
        for x in range(0, self._message_timeout):
            await asyncio.sleep(0.01)
            # if tx_tid is not in message list then the message listener has received the message
            if tx_tid not in self._message_list:
                # transaction sucessful remove from list
                return True
        return False

    async def getAllPropertyMaps(self, host, eojgc, eojcc, eojci):
        return await self.echonetMessage(host, eojgc, eojcc, eojci, GET, [{'EPC': ENL_GETMAP}, {'EPC': ENL_SETMAP}])

    async def getIdentificationInformation(self, host, eojgc, eojcc, eojci):
        return await self.echonetMessage(host, eojgc, eojcc, eojci, GET, [{'EPC': ENL_UID}, {'EPC': ENL_MANUFACTURER}])

    async def process_discovery_data(self, host, opc_data):
        if 'discovered' not in self._state[host]:
            edt = bytearray(opc_data['EDT'])
            # 1st byte: Total number of instances
            # 2nd to 253rd bytes: ECHONET object codes (EOJ3 bytes) enumerated
            edtnum = bytearray(edt)[0]
            for x in range(edtnum):
                eojgc = bytearray(edt)[1 + (3 * x)]
                eojcc = bytearray(edt)[2 + (3 * x)]
                eojci = bytearray(edt)[3 + (3 * x)]

                # populate state table
                if eojgc not in list(self._state[host]["instances"].keys()):
                    self._state[host]["instances"].update({eojgc: {}})
                if eojcc not in list(self._state[host]["instances"][eojgc].keys()):
                    self._state[host]["instances"][eojgc].update({eojcc: {}})
                if eojci not in list(self._state[host]["instances"][eojgc][eojcc].keys()):
                    self._state[host]["instances"][eojgc][eojcc][eojci] = {}
                    self._state[host]["instances"][eojgc][eojcc][eojci].update({
                                                                               ENL_SETMAP: []})
                    self._state[host]["instances"][eojgc][eojcc][eojci].update({
                                                                               ENL_GETMAP: []})
            self._state[host]["discovered"] = True
