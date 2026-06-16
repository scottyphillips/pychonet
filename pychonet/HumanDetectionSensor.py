# HumanDetectionSensor class for ECHONET Lite protocol implementation in Python.
# This class represents a human detection sensor that can monitor presence
# using the ECHONET Lite protocol. It provides methods to get operation status
# and human detection status.
#
# Author: Scotty
# Date: 2026-03

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF

# Mapping for human detection status (EPC 0xB1)
HUMAN_DETECTION_MAP = {
    0x41: "detected",
    0x42: "not_detected",
}


class HumanDetectionSensor(EchonetInstance):
    """
    HumanDetectionSensor implements the ECHONET Lite protocol for human detection devices.
    EOJ: Group Code 0x00, Class Code 0x07
    """

    # EPC functions mapping for the human detection sensor
    EPC_FUNCTIONS = {
        # 0x80: Operation status (ON/OFF)
        0x80: [_int, DICT_30_ON_OFF],
        # 0xB1: Human detection status
        0xB1: [_int, HUMAN_DETECTION_MAP],
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        """
        Initialize a new HumanDetectionSensor instance.

        :param host: IP address of the device.
        :param api_connector: Optional API connector for sending messages.
        :param instance: Instance number (0x01–0x7F). 0x00 is all-instance.
        """
        self._eojgc = 0x00          # Class group code (Sensors)
        self._eojcc = 0x07          # Class code for human detection sensor
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
    # Human detection status (0xB1)
    # ----------------------------------------------------------------------
    async def getHumanDetectionStatus(self):
        """Get the human detection status.

        Returns:
            str: 'detected' if a person is detected, 'not_detected' otherwise.
        """
        return await self.getMessage(0xB1)