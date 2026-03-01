# WaterFlowSensor class for Echonet Lite protocol implementation in Python.
# This class represents a water flow sensor device that can be monitored using the Echonet Lite protocol.
# It provides methods to get the operation status, cumulative flow rate, and instantaneous flow rate.

# Author: Scotty
# Date: 2026-03

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF

class WaterFlowSensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # Water flow sensor class
        0x80: [_int, DICT_30_ON_OFF],  # "Operation status"
        0xE0: _int,  # "Cumulative flow rate (cm³)"
        0xE2: _int,  # "Flow rate (cm³/min)"
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x25
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def get_cumulative_flow_rate(self):
        return await self.getMessage(0xE0)

    async def get_flow_rate(self):
        return await self.getMessage(0xE2)