# CurrentSensor class for Echonet Lite protocol implementation in Python.
# This class represents a current sensor device that can be monitored using the Echonet Lite protocol. 
# It provides methods to get the operation status, measured current value, and rated voltage value.
# Note: Current sensor devices are read-only - no set methods available.

# Author: Scotty
# Date: 2026-03

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF

class CurrentSensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # Current sensor class (read-only device)
        0x80: [_int, DICT_30_ON_OFF],  # "Operation status" - ON/OFF
        0xE0: _int,  # "Measured current value 1 (mA)"
        0xE1: _int,  # "Rated voltage to be measured (V)" - raw voltage value
        0xE2: _int,  # "Measured current value 2 (mA)"
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x23
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getOperationStatus(self):
        """Get the operation status (ON/OFF)."""
        return await self.getMessage(0x80)

    async def getMeasuredCurrentValue1(self):
        """Get measured current value 1 in milliamperes."""
        return await self.getMessage(0xE0)

    async def getRatedVoltage(self):
        """Get rated voltage to be measured in volts."""
        return await self.getMessage(0xE1)

    async def getMeasuredCurrentValue2(self):
        """Get measured current value 2 in milliamperes."""
        return await self.getMessage(0xE2)