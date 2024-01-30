from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import DICT_41_ON_OFF, _int, _hh_mm, _signed_int


class FloorHeater(EchonetInstance):
    EOJGC = 0x02
    EOJCC = 0x7B

    EPC_FUNCTIONS = {
        0xE0: _int,  # "Temperature setting 1",
        0xE1: _int,  # "Temperature setting 2",
        0xD1: _int,  # "Temperature setting 2 – Maximum settable level"
        0xE2: _signed_int,  # "Measured room temperature",
        0xE3: _signed_int,  # "Measured floor temperature",
        # 0xE4: _int,  # "Zone change setting", Sets the target zone for control and gets the number of controllable zones b0–b7 is allocated to 0 to 7 Each bit 1: with control, 0: without control
        0xE5: [
            _int,
            {
                0x41: "Normal",
                0x42: "Modest",
                0x43: "High power",
            },
        ],  # "Special operation setting",
        0xE6: [
            _int,
            {
                0x40: "Timer OFF",
                0x41: "Timer 1",
                0x42: "Timer 2",
            },
        ],  # "Daily timer setting",
        # 0xE7: ,  # "Daily timer setting 1", Set the time in the unit of 30 minutes, dividing 24 hours by 30 minutes and allocated to 6 bytes. Each bit 1: worked 0: stopped
        # 0xE8: ,  # "Daily timer setting 2", Set the time in the unit of 30 minutes, dividing 24 hours by 30 minutes and allocated to 6 bytes. Each bit 1: worked 0: stopped
        0x90: [_int, DICT_41_ON_OFF],  # "ON timer reservation setting",
        0x91: _hh_mm,  # "Time set by ON timer",
        0x92: _hh_mm,  # "Relative ON timer setting",
        0x94: [_int, DICT_41_ON_OFF],  # "OFF timer reservation setting",
        0x95: _hh_mm,  # "Time set by OFF timer",
        0x96: _hh_mm,  # "Relative OFF timer setting",
        0x84: _signed_int,  # "Measured instantaneous power consumption",
        0x85: _signed_int,  # "Measured cumulative electric energy consumption",
        0xE9: _signed_int,  # "Rated power consumption",
        0xEA: [
            _int,
            {
                0x41: "Node unit",
                0x42: "Class unit",
                0x43: "Instance unit",
            },
        ],  # "Power consumption measurement method",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = self.EOJGC
        self._eojcc = self.EOJCC
        super().__init__(host, self._eojgc, self._eojcc, instance, api_connector)
