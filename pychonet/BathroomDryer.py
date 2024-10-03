from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DICT_41_AUTO_8_LEVELS,
    DICT_41_AUTO_STANDARD,
    DICT_41_ON_OFF,
    _int,
    _hh_mm,
    _signed_int,
)


class BathroomDryer(EchonetInstance):
    EOJGC = 0x02
    EOJCC = 0x73

    EPC_FUNCTIONS = {
        0xB0: [
            _int,
            {
                0x10: "ventilation",
                0x20: "prewarming",
                0x30: "heating",
                0x40: "drying",
                0x50: "circulation",
                0x60: "mistSauna",
                0x61: "waterMist",
                0x00: "stop",
            },
        ],  # "Operation setting",
        0xB1: [
            _int,
            {**DICT_41_AUTO_STANDARD, **DICT_41_AUTO_8_LEVELS},
        ],  # "Ventilation operation setting",
        0xB2: [
            _int,
            {**DICT_41_AUTO_STANDARD, **DICT_41_AUTO_8_LEVELS},
        ],  # "Bathroom pre-warmer operation setting",
        0xB3: [
            _int,
            {**DICT_41_AUTO_STANDARD, **DICT_41_AUTO_8_LEVELS},
        ],  # "Bathroom heater operation setting",
        0xB4: [
            _int,
            {**DICT_41_AUTO_STANDARD, **DICT_41_AUTO_8_LEVELS},
        ],  # "Bathroom dryer operation setting",
        0xB5: [
            _int,
            {**DICT_41_AUTO_STANDARD, **DICT_41_AUTO_8_LEVELS},
        ],  # "Cool air circulator operation setting",
        0xB6: [
            _int,
            {**DICT_41_AUTO_STANDARD, **DICT_41_AUTO_8_LEVELS},
        ],  # "Mist sauna operation setting",
        0xB7: [
            _int,
            {**DICT_41_AUTO_STANDARD, **DICT_41_AUTO_8_LEVELS},
        ],  # "Water mist operation setting",
        0xBA: _int,  # "Measured relative bathroom humidity",
        0xBB: _signed_int,  # "Measured bathroom temperature",
        0xC2: [_int, DICT_41_AUTO_8_LEVELS],  # "Ventilation air flow rate setting",
        0xCF: [_int, DICT_41_ON_OFF],  # "Filter cleaning reminder sign setting",
        0xE0: [_int, DICT_41_ON_OFF],  # "Human body detection status",
        0x90: [_int, DICT_41_ON_OFF],  # "“ON timer-based reservation” setting 1",
        0xE1: [
            _int,
            {
                0x10: "ventilationReservation",
                0x20: "prewarmingReservation",
                0x30: "heatingReservation",
                0x40: "dryingReservation",
                0x50: "circulationReservation",
                0x60: "mistSaunaReservation",
                0x61: "waterMistReservation",
                0x00: "noReservation",
            },
        ],  # "“ON timer-based reservation” setting 2",
        0x91: _hh_mm,  # "ON timer setting (time)",
        0x92: _hh_mm,  # "ON timer setting (relative time)",
        0x94: [_int, DICT_41_ON_OFF],  # "“OFF timer-based reservation” setting",
        0x95: _hh_mm,  # "OFF timer setting (time)",
        0x96: _hh_mm,  # "OFF timer setting (relative time)",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = self.EOJGC
        self._eojcc = self.EOJCC
        super().__init__(host, self._eojgc, self._eojcc, instance, api_connector)
