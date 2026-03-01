# AirSpeedSensor class for Echonet Lite protocol implementation in Python.
# This class represents an air speed sensor device that can be controlled and monitored using the Echonet Lite protocol. 
# It provides methods to get and set the operation status and to get the measured value of air speed and air flow direction.

# author: Scotty
# Date: 2026-03

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF

class AirSpeedSensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # Air speed sensor class
        0x80: [_int, DICT_30_ON_OFF],  # "Operation status",
        0xE0: _int,  # "Measured value of air speed (0.01 m/sec)",
        0xE1: _int,  # "Air flow direction (degrees)",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x1F
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        return await self.setMessage(0x80, status)

    async def getAirSpeed(self):
        return await self.getMessage(0xE0)

    async def getAirFlowDirection(self):
        return await self.getMessage(0xE1)