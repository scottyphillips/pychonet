from datetime import datetime
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int

ENL_LVSEEM_COEF = 0xD3
ENL_LVSEEM_DIGITS = 0xD7
ENL_LVSEEM_ENG_UNIT = 0xE1
ENL_LVSEEM_ENG_NOR = 0xE0
ENL_LVSEEM_ENG_REV = 0xE3
ENL_LVSEEM_INSTANT_ENG = 0xE7
ENL_LVSEEM_INSTANT_CUR = 0xE8


def _0288E0(edt):
    if len(edt) < 1:
        return None
    power_val = _int(edt)
    return None if power_val == 4294967294 else power_val  # no measurement


def _0288E1(edt):
    return _int(
        edt,
        {
            0x00: 1,
            0x01: 0.1,
            0x02: 0.01,
            0x03: 0.001,
            0x04: 0.0001,
            0x0A: 10,
            0x0B: 100,
            0x0C: 1000,
            0x0D: 10000,
        },
        None,
    )


def _0288E2(edt):
    """
    1-2 bytes: day for which the
    historical data of measured
    cumulative amounts of electric
    energy is to be retrieved 0x0000–
    0x0063 (0-99)
    3 and succeeding bytes: measured
    cumulative amounts of electric
    energy 0x00000000–0x05F5E0FF
    (0–99,999,999)

    unsigned short + unsigned long × 48
    """
    return "Not implemented"


def _0288E7(edt):
    if len(edt) < 1:
        return None
    power_val = _signed_int(edt)
    as_None = power_val in [
        -2147483648,
        2147483647,
        2147483646,
    ]  # underflow, overflow, no measurement
    return None if as_None else power_val


def _0288E8(edt):
    if len(edt) < 1:
        return {"r_phase_amperes": None, "t_phase_amperes": None}
    r_phase = float(_signed_int(edt[0:2])) / 10  # R Phase
    t_phase = float(_signed_int(edt[2:4])) / 10  # T Phase
    asNone = [-3276.8, 3276.7, 3276.6]  # underflow, overflow, no measurement
    if r_phase in asNone:
        r_phase = None
    if t_phase in asNone:
        t_phase = None
    return {"r_phase_amperes": r_phase, "t_phase_amperes": t_phase}


def _0288EA(edt):
    """
    1–4 bytes: date of measurement
    YYYY: 0x0001–0x270F
    (1–9999)
    MM: 0x01–0x0C (1–12)
    DD: 0x01–0x1F (1–31)
    5–7 bytes: time of measurement
    hh: 0x00–0x17 (0–23)
    mm: 0x00–0x3B (0–59)
    ss: 0x00–0x3B (0–59)
    8–11 bytes: cumulative amounts of
    electric energy measured
    0x00000000–0x05F5E0FF
    (0–99,999,999)

    unsigned short + unsigned char ×2
        +
    unsigned char × 3
        +
    unsigned long
    """
    year = int.from_bytes(edt[0:2], "big")
    month = int.from_bytes(edt[2:3], "big")
    day = int.from_bytes(edt[3:4], "big")
    hour = int.from_bytes(edt[4:5], "big")
    minute = int.from_bytes(edt[5:6], "big")
    second = int.from_bytes(edt[6:7], "big")
    culmative = int.from_bytes(edt[7:], "big")
    return {
        "time": datetime(year, month, day, hour, minute, second).isoformat(),
        "culmative_value": culmative,
    }


def _0288EC(edt):
    """
    1–6 bytes: date and time for which
    the historical data is to be retrieved
    YYYY: 0x0001–0x270F (1–9999)
    MM: 0x01–0x0C (1–12)
    DD: 0x01–0x1F (1–31)
    hh: 0x00–0x17 (0–23)
    mm: 0x00/0x1E (0/30)
    7 byte: number of collection
    segments
    0x01–0x0C (1–12)
    8th and succeeding bytes:
    Measured cumulative amount of
    electric energy (normal direction)
    0x00000000–0x05F5E0FF
    (0–99,999,999)
    Measured cumulative amount of
    electric energy (reverse direction)
    0x00000000–0x05F5E0FF
    (0–99,999,999)

    unsigned short + unsigned char × 4
        +
    unsigned char + (unsigned long + unsigned long) × (Max) 12
    """
    return "Not implemented"


def _0288ED(edt):
    """
    1–6 bytes: date and time for which
    the historical data is to be retrieved
    YYYY: 0x0001–0x270F (1–9999)
    MM: 0x01–0x0C (1–12)
    DD: 0x01–0x1F (1–31)
    hh: 0x00–0x17 (0–23)
    mm: 0x00/0x1E (0/30)
    7 byte: number of collection
    segments
    0x01–0x0C (1–12)

    unsigned short + unsigned char × 4 + unsigned char
    """
    return "Not implemented"


class LowVoltageSmartElectricEnergyMeter(EchonetInstance):
    EPC_FUNCTIONS = {
        0xD3: _int,  # "Coefficient"
        0xD7: _int,  # "Number of effective digits for cumulative amounts of electric energy"
        0xE0: _0288E0,  # "Measured cumulative amount of electric energy (normal direction)"
        0xE1: [
            _int,
            {
                0x00: 1,
                0x01: 0.1,
                0x02: 0.01,
                0x03: 0.001,
                0x04: 0.0001,
                0x0A: 10,
                0x0B: 100,
                0x0C: 1000,
                0x0D: 10000,
            },
            None,
        ],  # "Unit for cumulative amounts of electric energy (normal and reverse directions)"
        # 0xE2: _0288E2, #"Historical data of measured cumulative amounts of electric energy 1 (normal direction)"
        0xE3: _0288E0,  # "Measured cumulative amounts of electric energy (reverse direction)"
        # 0xE4: _0288E2, #"Historical data of measured cumulative amounts of electric energy 1 (reverse direction)"
        # 0xE5: _int, #"Day for which the historical data of measured cumulative amounts of electric energy is to be retrieved 1"
        0xE7: _0288E7,  # "Measured instantaneous electric energy"
        0xE8: _0288E8,  # "Measured instantaneous currents"
        # 0xEA: _0288EA,  # "Cumulative amounts of electric energy measured at fixed time (normal direction)"
        # 0xEB: _0288EA,  # "Cumulative amounts of electric energy measured at fixed time (reverse direction)"
        # 0xEC: _0288EC, #"Historical data of measured cumulative amounts of electric energy 2 (normal and reverse directions)"
        # 0xED: _0288ED, #"Day for which the historical data of measured cumulative amounts of electric energy is to be retrieved 2"
    }

    def __init__(self, host, api_connector, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x88
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
