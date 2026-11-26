from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    TIME_SYNCHRONIZATION_STATUS,
    _date_time,
    _hh_mm_ss,
    _int,
    _signed_int,
)


TOLERANCE_CLASSES = {code: f"n{code}" for code in range(1, 8)}
TOLERANCE_CLASSES[0xFF] = "other"
ENERGY_UNITS = {
    0x00: 1,
    0x01: 0.1,
    0x02: 0.01,
    0x03: 0.001,
    0x04: 0.0001,
    0x0A: 10,
    0x0B: 100,
    0x0C: 1000,
    0x0D: 10000,
}


def _028ED4(edt):
    return ENERGY_UNITS.get(_int(edt))


def _energy_count(edt):
    if len(edt) != 4:
        return None
    count = _int(edt)
    return None if count == 0xFFFFFFFE else count


def _history_day(edt):
    if len(edt) != 2:
        return None
    day = _int(edt)
    return None if day == 0xFFFF else day


def _energy_history(edt):
    if len(edt) != 194:
        return None
    return {
        "day": _history_day(edt[:2]),
        "readings_48_half_hourly": [
            _energy_count(edt[offset : offset + 4]) for offset in range(2, 194, 4)
        ],
    }


def _energy_at_fixed_time(edt):
    if len(edt) != 11:
        return None
    return {"time": _date_time(edt[:7]), "electric_energy": _energy_count(edt[7:])}


class DistributedGeneratorElectricEnergyMeter(EchonetInstance):
    """Device object 0x028E from the ECHONET Lite Appendix, Release R rev.4."""

    EPC_FUNCTIONS = {
        0x80: _int,
        0xA0: _energy_count,
        0xA1: _energy_history,
        0xA2: _energy_at_fixed_time,
        0xA3: _energy_count,
        0xA4: _energy_history,
        0xA5: _energy_at_fixed_time,
        0xA6: _energy_count,
        0xA7: _energy_history,
        0xA8: _energy_at_fixed_time,
        0xA9: _energy_count,
        0xAA: _energy_history,
        0xAB: _energy_at_fixed_time,
        0xB0: _energy_count,
        0xB1: _energy_count,
        0xB2: _energy_count,
        0xB3: _energy_count,
        0xB4: _energy_count,
        0xB5: _energy_count,
        0xB6: _energy_history,
        0xB7: _energy_at_fixed_time,
        0xD2: [_int, TOLERANCE_CLASSES],
        0xD3: _history_day,
        0xD4: _028ED4,
        0xD5: _history_day,
        0xD7: [_int, TOLERANCE_CLASSES],
        0xD8: [_int, TOLERANCE_CLASSES],
        0xD9: [_int, TOLERANCE_CLASSES],
        0xDA: _hh_mm_ss,
        0xDB: [_int, TIME_SYNCHRONIZATION_STATUS],
        0xE0: _int,
        0xE1: _energy_history,
        0xE2: _int,
        0xE3: _energy_history,
        0xE4: _int,
        0xE5: _energy_history,
        0xE6: _energy_at_fixed_time,
        0xE7: _energy_at_fixed_time,
        0xE8: _energy_at_fixed_time,
        0xE9: _signed_int,
        0xEA: _signed_int,
    }

    def __init__(self, host, api_connector=None, instance=0x01):
        self._eojgc = 0x02
        self._eojcc = 0x8E
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
