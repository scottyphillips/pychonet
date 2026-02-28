# pychonet/EmergencyButton.py
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF


class EmergencyButton(EchonetInstance):
    EPC_FUNCTIONS = {
        # Emergency button class
        0x80: [_int, DICT_30_ON_OFF],  # "Operation status",
        0xB1: [_int, {0x41: 'Emergency occurrence status found', 0x42: 'Emergency occurrence status not found'}],  # "Emergency occurrence status",
        0xBF: [_int, {0x00: 'Reset'}],  # "Emergency occurrence status resetting",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x03
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        return await self.setMessage(0x80, status)

    async def getEmergencyOccurrenceStatus(self):
        return await self.getMessage(0xB1)

    async def resetEmergencyOccurrenceStatus(self):
        return await self.setMessage(0xBF, 0x00)  # Reset command