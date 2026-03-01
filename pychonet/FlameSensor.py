# FlameSensor class for Echonet Lite protocol implementation in Python.
# This class represents a flame sensor device that can be controlled and monitored using the Echonet Lite protocol. 
# It provides methods to get and set the operation status, detection threshold level, flame detection status, and reset flame detection status.

# Author: Scotty
# Date: 2026-03

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF, DICT_31_8_LEVELS

class FlameSensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # Flame sensor class
        0x80: [_int, DICT_30_ON_OFF],  # "Operation status", ON=0x30, OFF=0x31
        0xB0: [_int, DICT_31_8_LEVELS],  # "Detection threshold level", 0x31–0x38
        0xB1: [_int, {0x41: 'found', 0x42: 'not found'}],  # "Flame detection status"
        0xBF: [_int, {0x00: 'reset'}],  # "Flame detection status resetting"
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00  # Class group code
        self._eojcc = 0x21  # Class code
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getOperationStatus(self):
        """Get the operation status of the flame sensor."""
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        """Set the operation status of the flame sensor."""
        return await self.setMessage(0x80, status)

    async def getDetectionThresholdLevel(self):
        """Get the detection threshold level of the flame sensor."""
        return await self.getMessage(0xB0)

    async def setDetectionThresholdLevel(self, level):
        """Set the detection threshold level of the flame sensor."""
        return await self.setMessage(0xB0, level)

    async def getFlameDetectionStatus(self):
        """Get the flame detection status of the flame sensor."""
        return await self.getMessage(0xB1)

    async def resetFlameDetectionStatus(self):
        """Reset the flame detection status of the flame sensor."""
        return await self.setMessage(0xBF, 0x00)