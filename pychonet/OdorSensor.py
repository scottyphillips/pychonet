# OdorSensor class for Echonet Lite protocol implementation in Python.
# This class represents an odor sensor device that can be controlled and monitored using the Echonet Lite protocol. 
# It provides methods to get and set the operation status, detection threshold level, odor detection status, and measured odor value.

# Author: Scotty
# Date: 2026-03


from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF, DICT_31_8_LEVELS

class OdorSensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # Odor sensor class
        0x80: [_int, DICT_30_ON_OFF],  # "Operation status",
        0xB0: [_int, DICT_31_8_LEVELS],  # "Detection threshold level",
        0xB1: [_int, {0x41: 'found', 0x42: 'not found'}],  # "Odor detection status",
        0xE0: _int,  # "Measured value of odor",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x1D
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

    async def getOdorDetectionStatus(self):
        return await self.getMessage(0xB1)

    async def getMeasuredOdorValue(self):
        return await self.getMessage(0xE0)