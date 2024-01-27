from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _hh_mm, _signed_int, _on_off


class FloorHeater(EchonetInstance):
    EOJGC = 0x02
    EOJCC = 0x7B

    EPC_FUNCTIONS = {
        0xE0: _int,  # "Temperature setting 1",
        0xE1: _int,  # "Temperature setting 2",
        0xD1: _int,  # "The maximum settable level is the top step of temperature setting 2"
        0xE2: _signed_int,  # "Measured room temperature",
        0xE3: _signed_int,  # "Measured floor temperature",
        0xE4: _int,  # "Zone change setting",
        0xE5: _int,  # "Special operation setting",
        0xE6: _int,  # "Daily timer setting",
        # 0xE7: ,  # "Daily timer setting 1",
        # 0xE8: ,  # "Daily timer setting 2",
        0x90: _on_off,  # "ON timer reservation setting",
        0x91: _hh_mm,  # "Time set by ON timer",
        0x92: _hh_mm,  # "Relative ON timer setting",
        0x94: _on_off,  # "OFF timer reservation setting",
        0x95: _hh_mm,  # "Time set by OFF timer",
        0x96: _hh_mm,  # "Relative OFF timer setting",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = self.EOJGC
        self._eojcc = self.EOJCC
        super().__init__(host, self._eojgc, self._eojcc, instance, api_connector)
