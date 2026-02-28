#python pychonet/CrimeSensor.py

# CrimeSensor class for ECHONET Lite
# This class represents a crime prevention sensor device in the ECHONET Lite protocol.
# It provides methods to get and set the operation status, detection threshold level, and invasion occurrence status.
# The class uses the EchonetInstance class to interact with the ECHONET Lite API.
#  Author: Scott Phillips
#  Date: 2024-06
#  License: MIT

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_41_ON_OFF, DICT_31_8_LEVELS

class CrimeSensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # Crime prevention sensor class
        0x80: [_int, {0x30: 'ON', 0x31: 'OFF'}],  # "Operation status",
        0xB0: [_int, DICT_31_8_LEVELS],  # "Detection threshold level",
        0xB1: [_int, {0x41: 'Invasion occurrence status found', 0x42: 'Invasion occurrence status not found'}],  # "Invasion occurrence status",
        0xBF: [_int, {0x00: 'Reset'}],  # "Invasion occurrence status resetting",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x02
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

    async def getInvasionOccurrenceStatus(self):
        return await self.getMessage(0xB1)

    async def resetInvasionOccurrenceStatus(self):
        return await self.setMessage(0xBF, 0x00)  # Reset command

