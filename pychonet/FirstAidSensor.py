# pychonet/FirstAidSensor.py
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF, DICT_31_8_LEVELS


class FirstAidSensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # First-aid sensor class
        0x80: [_int, DICT_30_ON_OFF],  # "Operation status",
        0xB0: [_int, DICT_31_8_LEVELS],  # "Detection threshold level",
        0xB1: [_int, {0x41: 'First-aid occurrence status found', 0x42: 'First-aid occurrence status not found'}],  # "First-aid occurrence status",
        0xBF: [_int, {0x00: 'Reset'}],  # "First-aid occurrence status resetting",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x04
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        return await self.setMessage(0x80, status)

    async def getDetectionThresholdLevel(self):
        return await self.getMessage(0xB0)

    async def setDetectionThresholdLevel(self, level):
        return await self.setMessage(0xB0, level)

    async def getFirstAidOccurrenceStatus(self):
        return await self.getMessage(0xB1)

    async def resetFirstAidOccurrenceStatus(self):
        return await self.setMessage(0xBF, 0x00)