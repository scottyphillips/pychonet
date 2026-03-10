# PassageSensor class for Echonet Lite protocol implementation in Python.
# This class represents a passage sensor device that can be controlled and monitored
# using the Echonet Lite protocol. It provides methods to get and set the
# operation status, detection threshold level, passage detection hold time,
# and passage detection direction.
#
# Author: Scotty
# Date: 2026-03

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF, DICT_31_8_LEVELS

# Custom mapping for passage detection direction (EPC 0xE0)
# 0x30: No passage
# 0x31–0x38: Direction of passage (1–8)
# 0x39: Passage detected but not located
# Any other values are treated as "unknown".
PASSAGE_DIRECTION_MAP = {
    0x30: "no passage",
    0x31: "direction-1",
    0x32: "direction-2",
    0x33: "direction-3",
    0x34: "direction-4",
    0x35: "direction-5",
    0x36: "direction-6",
    0x37: "direction-7",
    0x38: "direction-8",
    0x39: "passage not located",
}

class PassageSensor(EchonetInstance):
    """
    PassageSensor implements the Echonet Lite protocol for passage detection devices.
    """

    # EPC functions mapping for the passage sensor
    EPC_FUNCTIONS = {
        # 0x80: Operation status (ON/OFF)
        0x80: [_int, DICT_30_ON_OFF],
        # 0xB0: Detection threshold level (8 steps)
        0xB0: [_int, DICT_31_8_LEVELS],
        # 0xBE: Passage detection hold time (ms)
        0xBE: _int,
        # 0xE0: Passage detection direction
        0xE0: [_int, PASSAGE_DIRECTION_MAP],
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        """
        Initialize a new PassageSensor instance.

        :param host: IP address of the device.
        :param api_connector: Optional API connector for sending messages.
        :param instance: Instance number (0x01–0x7F). 0x00 is all-instance.
        """
        self._eojgc = 0x00          # Class group code
        self._eojcc = 0x27          # Class code for passage sensor
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    # ----------------------------------------------------------------------
    # Operation status (0x80) – ON/OFF
    # ----------------------------------------------------------------------
    async def getOperationStatus(self):
        """Get the operation status (ON/OFF)."""
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        """
        Set the operation status.

        :param status: One of DICT_30_ON_OFF values (e.g., 'on', 'off').
        """
        return await self.setMessage(0x80, status)

    # ----------------------------------------------------------------------
    # Detection threshold level (0xB0) – 8 step
    # ----------------------------------------------------------------------
    async def getDetectionThresholdLevel(self):
        """Get the detection threshold level."""
        return await self.getMessage(0xB0)

    async def setDetectionThresholdLevel(self, level):
        """
        Set the detection threshold level.

        :param level: One of DICT_31_8_LEVELS values (e.g., 'level-1', 'level-8').
        """
        return await self.setMessage(0xB0, level)

    # ----------------------------------------------------------------------
    # Passage detection hold time (0xBE) – ms
    # ----------------------------------------------------------------------
    async def getPassageDetectionHoldTime(self):
        """Get the passage detection hold time in milliseconds."""
        return await self.getMessage(0xBE)

    async def setPassageDetectionHoldTime(self, hold_time_ms):
        """
        Set the passage detection hold time.

        :param hold_time_ms: Unsigned short (0–65533 ms).
        """
        return await self.setMessage(0xBE, hold_time_ms)

    # ----------------------------------------------------------------------
    # Passage detection direction (0xE0)
    # ----------------------------------------------------------------------
    async def getPassageDetectionDirection(self):
        """Get the passage detection direction."""
        return await self.getMessage(0xE0)