# MicromotionSensor.py
# Micromotion sensor class for Echonet Lite protocol implementation in Python.
# This class represents a micromotion sensor device that can be controlled and monitored using the Echonet Lite protocol.
# It provides methods to get and set the operation status, detection threshold level, micromotion detection status, detection counter, sampling count, and sampling cycle.

# Author: Scotty
# Date: 2026-03

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF, DICT_31_8_LEVELS

# Custom dictionary for micromotion detection status
DICT_41_MICROMOTION_STATUS = {0x41: 'detected', 0x42: 'not_detected'}

class MicromotionSensor(EchonetInstance):
    """Echonet Lite Micromotion Sensor implementation.

    This class maps the Echonet Lite EPCs relevant to a micromotion sensor to
    convenient async methods for getting and setting values. The class uses
    helper functions and dictionaries from :mod:`pychonet.lib.epc_functions`
    to interpret the raw payload data.
    """

    # Mapping of EPC codes to (function, optional mapping dictionary)
    EPC_FUNCTIONS = {
        0x80: [_int, DICT_30_ON_OFF],            # Operation status (ON/OFF)
        0xB0: [_int, DICT_31_8_LEVELS],          # Detection threshold level (8 steps)
        0xB1: [_int, DICT_41_MICROMOTION_STATUS],  # Micromotion detection status
        0xB2: [_int],                            # Detection counter (unsigned short)
        0xBC: [_int],                            # Sampling count (unsigned short)
        0xBD: [_int],                            # Sampling cycle (unsigned short, msec)
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        # The class/group codes for a micromotion sensor. These values are
        # placeholders; replace with the correct codes if they differ.
        self._eojgc = 0x00
        self._eojcc = 0x1E
        EchonetInstance.__init__(self, host, self._eojgc, self._eojcc, instance, api_connector)

    # ---- Operation status -------------------------------------------------
    async def getOperationStatus(self):
        """Retrieve the operation status (ON/OFF)."""
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        """Set the operation status (ON/OFF)."""
        return await self.setMessage(0x80, status)

    # ---- Detection threshold level ---------------------------------------
    async def getDetectionThresholdLevel(self):
        """Retrieve the detection threshold level (8 steps)."""
        return await self.getMessage(0xB0)

    async def setDetectionThresholdLevel(self, level):
        """Set the detection threshold level (8 steps)."""
        return await self.setMessage(0xB0, level)

    # ---- Micromotion detection status ------------------------------------
    async def getMicromotionDetectionStatus(self):
        """Retrieve the micromotion detection status."""
        return await self.getMessage(0xB1)

    # ---- Detection counter ------------------------------------------------
    async def getDetectionCounter(self):
        """Retrieve the micromotion detection count."""
        return await self.getMessage(0xB2)

    async def setDetectionCounter(self, count):
        """Set the micromotion detection count."""
        return await self.setMessage(0xB2, count)

    # ---- Sampling count ---------------------------------------------------
    async def getSamplingCount(self):
        """Retrieve the micromotion detection sampling count."""
        return await self.getMessage(0xBC)

    async def setSamplingCount(self, count):
        """Set the micromotion detection sampling count."""
        return await self.setMessage(0xBC, count)

    # ---- Sampling cycle ---------------------------------------------------
    async def getSamplingCycle(self):
        """Retrieve the micromotion detection sampling cycle (msec)."""
        return await self.getMessage(0xBD)

    async def setSamplingCycle(self, cycle):
        """Set the micromotion detection sampling cycle (msec)."""
        return await self.setMessage(0xBD, cycle)
