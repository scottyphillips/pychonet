
# OpenCloseSensor class for Echonet Lite protocol implementation in Python.
# This class represents an open/close sensor device that can be monitored using the Echonet Lite protocol. 
# It provides methods to get and set the operation status, detection threshold level, open/close detection status, and degree-of-opening detection status.

# Author: Scotty
# Date: 2026-03

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF, DICT_31_8_LEVELS

class OpenCloseSensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # Open/close sensor class
        0x80: [_int, DICT_30_ON_OFF],  # "Operation status",
        0xB0: [_int, DICT_31_8_LEVELS],  # "Detection threshold level",
        0xB1: [_int, {0x41: 'open detected', 0x42: 'close detected'}],  # "Degree-of-opening detection status",
        0xE0: [_int, {0x30: 'close detected', 0x31: 'level-1', 0x32: 'level-2', 0x33: 'level-3', 0x34: 'level-4', 0x35: 'level-5', 0x36: 'level-6', 0x37: 'level-7', 0x38: 'level-8', 0x39: 'open detected but degree-of-opening unknown'}],  # "Open/close detection status and degree-of-opening",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x29
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

    async def getDegreeOfOpeningDetectionStatus(self):
        return await self.getMessage(0xB1)

    async def getOpenCloseDetectionStatus(self):
        return await self.getMessage(0xE0)