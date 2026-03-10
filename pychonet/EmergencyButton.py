# pychonet/EmergencyButton.py

# EmergencyButton class for ECHONET Lite
# This class represents an emergency button device in the ECHONET Lite protocol.
# It provides methods to get and set the operation status, emergency occurrence status, and reset the emergency status.
# The class uses the EchonetInstance class to interact with the ECHONET Lite API.
# Reference: https://echonet.jp/wp/wp-content/uploads/pdf/General/Standard/Release/Release_R/Appendix_Release_R_rev3_E.pdf

#  Author: Scott Phillips
#  Date: 2026-02
#  License: MIT

# +----------------------------+------+--------------------------------+-----------+------+--------+--------+-----------+
# | Property Name              | EPC  | Contents (Value Range)         | Data Type | Size | Access | Mandat.| Announce. |
# +----------------------------+------+--------------------------------+-----------+------+--------+--------+-----------+
# | Operation status           | 0x80 | ON=0x30, OFF=0x31              | u_char    | 1 B  | Set/Get| Get (O)|     O     |
# | Emergency occurrence stat. | 0xB1 | Found=0x41, Not Found=0x42     | u_char    | 1 B  | Get    |    O   |     O     |
# | Emergency status resetting | 0xBF | Reset=0x00                     | u_char    | 1 B  | Set    |        |           |
# +----------------------------+------+--------------------------------+-----------+------+--------+--------+-----------+

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF


class EmergencyButton(EchonetInstance):
    EPC_FUNCTIONS = {
        # Emergency button class
        0x80: [_int, DICT_30_ON_OFF],  # "Operation status",
        0xB1: [_int, {0x41: 'Found', 0x42: 'Not Found'}],  # "Emergency occurrence status",
        0xBF: [_int, {0x00: 'Reset'}],  # "Emergency occurrence status resetting",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x03
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        return await self.setMessage(0x80, status)

    async def getEmergencyOccurrenceStatus(self):
        return await self.getMessage(0xB1)

    async def resetEmergencyOccurrenceStatus(self):
        return await self.setMessage(0xBF, 0x00)  # Reset command