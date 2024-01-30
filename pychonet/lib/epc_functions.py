from typing import Any, ByteString
from pychonet.lib.const import MANUFACTURERS

# Data States
DATA_STATE_ON = "on"
DATA_STATE_OFF = "off"
DATA_STATE_LOCK = "locked"
DATA_STATE_UNLOCK = "unlocked"
DATA_STATE_OPEN = "open"
DATA_STATE_CLOSE = "closed"
DATA_STATE_STOP = "stop"

# Like switch type
DICT_41_ON_OFF = {0x41: DATA_STATE_ON, 0x42: DATA_STATE_OFF}
DICT_41_YES_NO = {0x41: "yes", 0x42: "no"}
DICT_41_AUTO_NONAUTO = {0x41: "auto", 0x42: "non-auto"}
DICT_41_UNLOCK_LOCK = {0x42: DATA_STATE_UNLOCK, 0x41: DATA_STATE_LOCK}
DICT_41_OPEN_CLOSED = {0x41: DATA_STATE_OPEN, 0x42: DATA_STATE_CLOSE}
DICT_41_ENABLED_DISABLED = {0x41: "enabled", 0x42: "disabled"}
DICT_41_AVAILABLE_NOT_AVAILABLE = {0x41: "available", 0x42: "not available"}
DICT_41_HEATING_NOT_HEATING = {0x41: "heating", 0x42: "not heating"}
DICT_41_PERMITTED_PROHIBITED = {0x41: "permitted", 0x42: "prohibited"}
DICT_30_TRUE_FALSE = {0x30: True, 0x31: False}
DICT_30_ON_OFF = {0x30: DATA_STATE_ON, 0x31: DATA_STATE_OFF}
DICT_30_OPEN_CLOSED = {0x30: DATA_STATE_OPEN, 0x31: DATA_STATE_CLOSE}

# Like select type
DICT_41_AUTO_8_SPEEDS = {
    0x41: "auto",
    0x31: "minimum",
    0x32: "low",
    0x33: "medium-low",
    0x34: "medium",
    0x35: "medium-high",
    0x36: "high",
    0x37: "very-high",
    0x38: "max",
}


def _swap_dict(d: dict):
    return {v: k for k, v in d.items()}


# ------------ EPC GENERIC FUNCTIONS -------
def _int(edt, values: dict = {}, non_value: Any = "Invalid setting"):  # unsigned int
    data_int = int.from_bytes(edt, "big")
    if len(values):
        return values.get(data_int, non_value)
    else:
        return int.from_bytes(edt, "big")


def _call_int(data: bytes | list):
    if type(data) == list:
        if len(data) == 3:
            return _int(data[0], data[1], data[2])
        elif len(data) == 2:
            return _int(data[0], data[1])
        else:
            return _int(data[0])
    else:
        return _int(data)


def _signed_int(edt):  # signed ints
    return int.from_bytes(edt, byteorder="big", signed=True)


def _hh_mm(edt):  # basic time unit
    hh = int.from_bytes(edt[0:1], "big")
    mm = str(int.from_bytes(edt[1:2], "big")).zfill(2)
    return f"{hh}:{mm}"


def _yyyy_mm_dd(edt):  # basic year unit
    yyyy = str(int.from_bytes(edt[0:4], "big")).zfill(4)
    mm = str(int.from_bytes(edt[4:6], "big")).zfill(2)
    dd = str(int.from_bytes(edt[6:8], "big")).zfill(2)
    return f"{yyyy}:{mm}:{dd}"


def _to_string(edt):
    return edt.decode("utf-8")


def _null_padded_optional_string(edt):
    return (
        edt.decode("utf-8").rstrip("\0") if edt is not None and len(edt) > 0 else None
    )


# Check status of Echonnet Instance
# ----------------- EPC SUPER FUNCTIONS -----------------------------
def _0080(edt):
    return _int(edt, DICT_30_ON_OFF)


def _009X(edt):
    payload = []
    if len(edt) < 17:
        for i in range(1, len(edt)):
            payload.append(edt[i])
        return payload

    for i in range(1, len(edt)):
        code = i - 1
        binary = "{0:08b}".format(edt[i])[::-1]
        for j in range(0, 8):
            if binary[j] == "1":
                EPC = (j + 8) * 0x10 + code
                payload.append(EPC)
    return payload


def _0083(edt, host=None):  # UID
    if edt is not None:
        if len(edt) > 1:
            ops_value = edt[1:].hex()
        else:
            if host is not None:
                digits = host.split(".")
                ops_value = digits[2].zfill(3) + digits[3].zfill(3)
            else:
                ops_value = None
        return ops_value
    return None


def _008A(edt):  # manufacturer
    id = int.from_bytes(edt, "big")
    if id in MANUFACTURERS.keys():
        return MANUFACTURERS[id]
    return id


def _009A(edt):  # cumulative runtime
    if len(edt) > 1:
        value = int.from_bytes(edt[1:], "big")
        time_period_multiplier = 0
        if edt[0] == 0x41:
            time_period_multiplier = 1  # measurement is in seconds
        elif edt[0] == 0x42:
            time_period_multiplier = 60  # measurement is in minutes
        elif edt[0] == 0x43:
            time_period_multiplier = 3600  # measurement is in hours
        elif edt[0] == 0x44:
            time_period_multiplier = 3600 * 24  # measurement is in days
        return value * time_period_multiplier
    return None


EPC_SUPER_FUNCTIONS = {
    0x80: _0080,
    0x83: _0083,
    0x84: _int,
    0x85: _int,
    0x8A: _008A,
    0x8C: _null_padded_optional_string,
    0x9A: _009A,
    0x9D: _009X,
    0x9E: _009X,
    0x9F: _009X,
}
