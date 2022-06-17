from datetime import datetime, timezone

from pychonet.lib.const import MANUFACTURERS


# ------------ EPC GENERIC FUNCTIONS -------
def _int(edt):  # unsigned int
    return int.from_bytes(edt, "big")


def _signed_int(edt):  # signed ints
    return int.from_bytes(edt, byteorder="big", signed=True)


def _hh_mm(edt):  # basic time unit
    hh = int.from_bytes(edt[0:1], "big")
    mm = str(int.from_bytes(edt[1:2], "big")).zfill(2)
    return f"{hh}:{mm}"

def _to_string(edt):
    return edt.decode('utf-8')

# Check status of Echonnet Instance
# ----------------- EPC SUPER FUNCTIONS -----------------------------
def _0080(edt):
    ops_value = int.from_bytes(edt, "big")
    return "On" if ops_value == 0x30 else "Off"


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


def _0083(edt):
    if edt is not None:
        if len(edt) > 1:
            ops_value = edt[1:].hex()
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
    0x9A: _009A,
    0x9D: _009X,
    0x9E: _009X,
    0x9F: _009X,
}


# ------- EPC FUNCTIONS -------------------------------------------------
# TODO - Move these to their classes
# -----------------------------------------------------------------------


# --- Low voltage smart meter class


def _0288E1(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {
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
    return values.get(op_mode, "invalid_setting")


# ----- Low voltage smart electric energy meter -------
def _0288E7(edt):
    value = int.from_bytes(edt, "big", signed=True)
    return value


def _0288E8(edt):
    r_phase = float(int.from_bytes(edt[0:2], "big", signed=True)) / 10  # R Phase
    t_phase = float(int.from_bytes(edt[2:4], "big", signed=True)) / 10  # T Phase
    return {"r_phase_amps": r_phase, "t_phase_amps": t_phase}


def _0288EA(edt):
    print(edt)
    year = int.from_bytes(edt[0:2], "big")
    month = int.from_bytes(edt[2:3], "big")
    day = int.from_bytes(edt[3:4], "big")
    hour = int.from_bytes(edt[4:5], "big")
    minute = int.from_bytes(edt[5:6], "big")
    second = int.from_bytes(edt[6:7], "big")
    culmative = int.from_bytes(edt[7:], "big")
    time = datetime(year, month, day, hour, minute, second)
    return {
        "time": datetime(year, month, day, hour, minute, second).isoformat(),
        "culmative_value": culmative,
    }
