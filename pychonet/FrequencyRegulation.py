from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DICT_30_ON_OFF,
    TIME_SYNCHRONIZATION_STATUS,
    _date_time,
    _hh_mm_ss,
    _int,
    _signed_int,
)


def _history_information(edt):
    if len(edt) != 16:
        return None
    return {
        "stored_entries": _int(edt[:2]),
        "capacity": _int(edt[2:4]),
        "oldest": _date_time(edt[4:10]),
        "latest": _date_time(edt[10:16]),
    }


def _power_reading(edt):
    power = _signed_int(edt)
    if power in (-0x80000000, 0x7FFFFFFE, 0x7FFFFFFF):
        return None
    return power


def _power_history(edt):
    if len(edt) != 246:
        return None
    return {
        "time": _date_time(edt[:6]),
        "readings_w": [
            _power_reading(edt[offset : offset + 4]) for offset in range(6, 246, 4)
        ],
    }


def _communication_cycle(edt):
    if len(edt) != 2:
        return None
    return _int(edt) * 10  # milliseconds


def _regulation_information(edt):
    if len(edt) != 4:
        return None
    return {"available_modes": _int(edt[:2]), "active_modes": _int(edt[2:])}


class FrequencyRegulation(EchonetInstance):
    """Device object 0x02A7 from the ECHONET Lite Appendix, Release R rev.4."""

    EPC_FUNCTIONS = {
        0xC0: [_int, {0x30: "device point", 0x31: "power receiving point"}],
        0xC2: _signed_int,
        0xC7: _signed_int,
        0xC8: [_int, DICT_30_ON_OFF],
        0xC9: _hh_mm_ss,
        0xCA: [_int, TIME_SYNCHRONIZATION_STATUS],
        0xCB: _history_information,
        0xCC: [_int, {0x30: "enabled", 0x31: "disabled"}],
        0xCD: _date_time,
        0xCE: _power_history,
        0xD0: _communication_cycle,
        0xD3: _int,
        0xD5: _regulation_information,
    }

    def __init__(self, host, api_connector=None, instance=0x01):
        super().__init__(host, 0x02, 0xA7, instance, api_connector)
