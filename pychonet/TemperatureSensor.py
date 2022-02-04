from pychonet.EchonetInstance import EchonetInstance

MEASURED_TEMP = 0xE0

# ----- Tempereature Sensor -------


def _0011E0(edt):
    return float(int.from_bytes(edt, "big")) / 10


class TemperatureSensor(EchonetInstance):
    EPC_FUNCTIONS = {
        0xE0: _0011E0,
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x11
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    def getMeasuredTemperature(self):
        return self.getMessage(MEASURED_TEMP)
