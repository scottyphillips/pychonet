# pychonet/CigaretteSensor.py

# CigaretteSensor class for ECHONET Lite
# This class represents a cigarette sensor device in the ECHONET Lite protocol.
# It provides methods to get and set the operation status, detection threshold level, and smoke detection status.
# The class uses the EchonetInstance class to interact with the ECHONET Lite API.
# Reference: https://echonet.jp/wp/wp-content/uploads/pdf/General/Standard/Release/Release_R/Appendix_Release_R_rev3_E.pdf

# author: Scott Phillips
# date: 2026-02
# license: MIT 

# +----------------------------+------+--------------------------------+-----------+------+--------+--------+-----------+
# | Property Name              | EPC  | Contents (Value Range)         | Data Type | Size | Access | Mandat.| Announce. |
# +----------------------------+------+--------------------------------+-----------+------+--------+--------+-----------+
# | Operation status           | 0x80 | ON=0x30, OFF=0x31              | u_char    | 1 B  | Set/Get| Get (O)|     O     |
# | Detection threshold level  | 0xB0 | 8-step: 0x31-0x38              | u_char    | 1 B  | Set/Get|        |           |
# | Smoke detection status     | 0xB1 | Found=0x41, Not Found=0x42     | u_char    | 1 B  | Get    |    O   |     O     |
# +----------------------------+------+--------------------------------+-----------+------+--------+--------+-----------+


from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_31_8_LEVELS, DICT_30_ON_OFF

class CigaretteSensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # Cigarette sensor class
        0x80: [_int, DICT_30_ON_OFF],  # "Operation status",
        0xB0: [_int, DICT_31_8_LEVELS],  # "Detection threshold level",
        0xB1: [_int, {0x41: 'Smoke (cigarette) detection status found', 0x42: 'Smoke (cigarette) detection status not found'}],  # "Smoke (cigarette) detection status",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x05
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

    async def getSmokeDetectionStatus(self):
        return await self.getMessage(0xB1)




