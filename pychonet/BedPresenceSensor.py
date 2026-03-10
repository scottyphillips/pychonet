# BedPrecenceSensor class for Echonet Lite protocol implementation in Python.
# This class represents a bed presence detection sensor that can be controlled and monitored
# using the Echonet Lite protocol. It provides methods to get and set the
# operation status, detection threshold level, and bed presence detection status.
#
# Author: Scotty
# Date: 2026-03

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF, DICT_31_8_LEVELS

# Mapping for bed presence detection status (EPC 0xB1)
BED_PRESENCE_MAP = {
    0x41: "bed present",
    0x42: "bed absent",
}

class BedPresenceSensor(EchonetInstance):
    """
    BedPrescenceSensor implements the Echonet Lite protocol for bed presence detection devices.
    """

    # EPC functions mapping for the bed presence sensor
    EPC_FUNCTIONS = {
        # 0x80: Operation status (ON/OFF)
        0x80: [_int, DICT_30_ON_OFF],
        # 0xB0: Detection threshold level (8 steps)
        0xB0: [_int, DICT_31_8_LEVELS],
        # 0xB1: Bed presence detection status
        0xB1: [_int, BED_PRESENCE_MAP],
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        """
        Initialize a new BedPrescenceSensor instance.

        :param host: IP address of the device.
        :param api_connector: Optional API connector for sending messages.
        :param instance: Instance number (0x01–0x7F). 0x00 is all-instance.
        """
        self._eojgc = 0x00          # Class group code
        self._eojcc = 0x28          # Class code for bed presence sensor
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
    # Bed presence detection status (0xB1)
    # ----------------------------------------------------------------------
    async def getBedPresenceDetectionStatus(self):
        """Get the bed presence detection status."""
        return await self.getMessage(0xB1)