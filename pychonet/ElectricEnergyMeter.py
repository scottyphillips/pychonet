from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int


def _0280E2(edt):
    # return array x 48 unsigned long big-endian
    return _int(edt, {0x01: 0.1, 0x02: 0.01})


class ElectricEnergyMeter(EchonetInstance):
    """ECHONET Lite Electric Energy Meter device class.

    EOJGC: 0x02 (Power Supply device group)
    EOJCC: 0x80 (Electric Energy Meter)
    
    Properties:
        0x80 - Operation status (ON/OFF)
        0xE0 - Cumulative energy measurement value (unsigned long, 4 bytes)
        0xE2 - Energy unit decimal places (0.1 or 0.01 kWh)
        0xE3 - Measurement log 1 (past 24 hours, 30-min segments x 48)
        0xE4 - Measurement log 2 (past 45 days, 30-min segments x 48 x 45)
    """

    EPC_FUNCTIONS = {
        0x80: _int,  # Operation status
        0xE0: _int,  # Cumulative energy measurement value (unsigned long)
        0xE2: _0280E2,  # Energy unit decimal places (0.1 or 0.01 kWh)
        0xE3: _int,  # Measurement log 1 (past 24 hours, 30-min segments x 48)
        0xE4: _int,  # Measurement log 2 (past 45 days, 30-min segments x 48 x 45)
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x80
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    def getOperationStatus(self):
        """Get operation status (ON=0x30, OFF=0x31)."""
        return self.getMessage(0x80)

    def setOperationStatus(self, value):
        """Set operation status. ON=0x30, OFF=0x31."""
        return self.setMessage(0x80, value)

    def getAccumulatedEnergyLeft(self):
        """Get cumulative energy measurement value (unsigned long, 4 bytes)."""
        return self.getMessage(0xE0)

    def getEnergyUnitDecimalPlaces(self):
        """Get number of decimal places for cumulative energy (0.1 or 0.01 kWh)."""
        return self.getMessage(0xE2)

    def getMeasurementLog1(self):
        """Get measurement log for past 24 hours (30-min segments x 48)."""
        return self.getMessage(0xE3)

    def getMeasurementLog2(self):
        """Get measurement log for past 45 days (30-min segments x 48 x 45)."""
        return self.getMessage(0xE4)
