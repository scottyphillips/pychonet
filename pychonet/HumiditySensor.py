from pychonet.EchonetInstance import EchonetInstance

MEASURED_HUMIDITY = 0xE0


def _0012E0(edt):
    """Decode humidity value from ECHONET Lite format.

    MRA definition: number_0-100percent
    - Format: uint8
    - Unit: %
    - Range: 0-100
    """
    return float(int.from_bytes(edt, "big"))


class HumiditySensor(EchonetInstance):
    EPC_FUNCTIONS = {
        0xE0: _0012E0,
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x12
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    def getMeasuredHumidity(self):
        """Get the measured relative humidity value.

        Returns:
            float: Humidity percentage (0-100%)
        """
        return self.getMessage(MEASURED_HUMIDITY)