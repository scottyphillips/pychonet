from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int


def _0280E2(edt):
    # return array x 48 unsigned long big-endian
    return _int(edt, {0x01: 0.1, 0x02: 0.01})


class ElectricEnergyMeter(EchonetInstance):
    EPC_FUNCTIONS = {
        0xE0: _int,  # 0xE0: "Cumulative amounts of electric energy measurement value",
        0xE2: _0280E2,  # 0xE2: "Cumulative amounts of electric energy unit",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x80
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
