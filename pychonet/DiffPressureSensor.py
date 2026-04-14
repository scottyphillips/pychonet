# DiffPressureSensor class for Echonet Lite protocol implementation in Python.
# This class represents a differential pressure sensor device that can be controlled and monitored using the Echonet Lite protocol. 
# It provides methods to get and set the operation status and to get the measured value of differential pressure.

# Author: Scotty
# Date: 2026-03

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF

class DiffPressureSensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # Diff Pressure Sensor class
        0x80: [_int, DICT_30_ON_OFF],  # "Operation status",
        0xE0: _int,  # "Measured value of differential pressure (Pa)",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x1E
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        return await self.setMessage(0x80, status)

    async def getDifferentialPressure(self):
        return await self.getMessage(0xE0)

