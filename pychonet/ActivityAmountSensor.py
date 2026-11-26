# ActivityAmountSensor class for Echonet Lite protocol implementation in Python.
# This class represents an activity amount sensor device that can be monitored using the Echonet Lite protocol. 
# It provides methods to get and set the operation status, activity threshold level, activity status, and measured activity amount.

# Author: Scotty
# Date: 2026-03


from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF, DICT_31_8_LEVELS

class ActivityAmountSensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # Activity amount sensor class
        0x80: [_int, DICT_30_ON_OFF],  # "Operation status",
        0xB0: [_int, DICT_31_8_LEVELS],  # Device-specific activity threshold
        0xB1: [_int, {0x41: "active", 0x42: "inactive"}],  # Device-specific activity status
        0xE1: _int,  # Maximum number of human body IDs
        0xE2: [_int, DICT_31_8_LEVELS],  # Activity amount level 2
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x2A
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        return await self.setMessage(0x80, status)

    async def getActivityThresholdLevel(self):
        return await self.getMessage(0xB0)

    async def setActivityThresholdLevel(self, level):
        return await self.setMessage(0xB0, level)

    async def getActivityStatus(self):
        readable = self.getGetProperties()
        epc = 0xB1 if 0xE2 not in readable and 0xB1 in readable else 0xE2
        return await self.getMessage(epc)

    async def getMeasuredActivityAmount(self):
        readable = self.getGetProperties()
        epc = 0xE0 if 0xE2 not in readable and 0xE0 in readable else 0xE2
        return await self.getMessage(epc)
