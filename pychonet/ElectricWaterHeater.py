from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DICT_41_HEATING_NOT_HEATING,
    DICT_41_ON_OFF,
    _int,
    _hh_mm,
)


# 0xB0 - Automatic water heating setting
# 0xB1 - Automatic water temperature control setting
# 0xB2 - Water heating status
# 0xB5 Relative time setting value for manual water heating OFF
# 0xB6 - Tank Operation mode setting
# 0xC0 - Daytime reheating permission setting


# 0xC2 - Alarm Status
def _026BC2(edt):
    alarm_status_bin = int.from_bytes(edt, "big")
    alarm_status = {
        "Out of Hot Water": "Normal",
        "Water leaking": "Normal",
        "Water frozen": "Normal",
    }
    if alarm_status_bin & 0b001:
        alarm_status["Out of Hot Water"] = "Alarm"
    if alarm_status_bin & 0b010:
        alarm_status["Water leaking"] = "Alarm"
    if alarm_status_bin & 0b100:
        alarm_status["Water Frozen"] = "Alarm"
    return alarm_status


# 0xC3 - Hot water supply status
# 0xC4 Relative time setting for keeping bath temperature
# 0xE1 - Measured amount of hot water remaining in tank
# 0xE2 - Tank Capacity
# 0xE3 - Automatic bath water heater mode setting
# 0xE9 - Bathroom Priority setting
# 0xEA - Bath operation status monitor
# 0xE4 - Manual bath reheating function setting
# 0xE5 - Manual bath hot water addition function setting
# 0xE6 - Manual lukewarm water temperature lowering function setting
# 0xE7 - Bath Volume water setting one
# 0xE8 - Bath Volume water setting two
# 0xEE - Bath Volume water setting three
# 0xD4 - Bath Volume water setting four
# 0xD5 - Bath Volume water setting four maximum settable level
# 0x90 - ON timer reservation setting
# 0x91 - ON timer setting
# 0xD6 - Sound Volume Setting
# 0xD7 - Mute Setting
# 0xD8 - Remaining Hot Water volume
# 0xD9 - Surplus electric energy prediction value


def _026BD9(edt):
    starting_MM = str(int.from_bytes(edt[0:1], "big")).zfill(2)
    starting_DD = str(int.from_bytes(edt[1:2], "big")).zfill(2)
    starting_hh_raw = int.from_bytes(edt[2:3], "big")
    starting_hh = str(starting_hh_raw).zfill(2)
    predicted_values_raw = edt[3:]
    predicted_values = {}
    it = iter(predicted_values_raw)
    for x in it:
        chunk = [x, next(it)]
        predicted_values[f"{str(starting_hh_raw).zfill(2)}:00"] = int.from_bytes(
            chunk, "big"
        )
        starting_hh_raw = starting_hh_raw + 1
        if starting_hh_raw == 24:
            starting_hh_raw = 0
    return {
        "start_month": starting_MM,
        "start_day": starting_DD,
        "start_hour": f"{starting_hh}:00",
        "predicted_values": predicted_values,
    }


# 0xDB - Rated power consumptions of H/P unit in winter time
# 0xDC - Rated power consumptions of H/P unit in between seasons
# 0xDD - Rated power consumptions of H/P unit in summer time


# 0xCB - Expected electric energy at daytime heating shift time 1
def _026BCB(edt):
    # 0x00000000-0xFFFFFFFD (0-4,294,967,293 W)
    # 10:00, 13:00, 15:00, 17:00
    # unsigned long x 4 16 byts Wh
    if len(edt) == 16:
        v1 = int.from_bytes(edt[0:4], "big")
        v2 = int.from_bytes(edt[4:8], "big")
        v3 = int.from_bytes(edt[8:12], "big")
        v4 = int.from_bytes(edt[12:16], "big")
    else:
        v1 = v2 = v3 = v4 = None
    return {"10:00": v1, "13:00": v2, "15:00": v3, "17:00": v4}


# 0xCC - Consumption of electric energy per hour 1
def _026BCC(edt):
    # 0x0000-0xFFFD (0-65,533 W)
    # When shifting at 10:00, 13:00, 15:00, and 17:00
    # 0x0000: cleared
    # unsigned short x 4 8 bytes Wh
    if len(edt) == 8:
        v1 = int.from_bytes(edt[0:2], "big")
        v2 = int.from_bytes(edt[2:4], "big")
        v3 = int.from_bytes(edt[4:6], "big")
        v4 = int.from_bytes(edt[6:8], "big")
    else:
        v1 = v2 = v3 = v4 = None
    return {"10:00": v1, "13:00": v2, "15:00": v3, "17:00": v4}


# 0xCE - Expected electric energy at daytime heating shift time 2
def _026BCE(edt):
    # 0x00000000-0xFFFFFFFD (0-4,294,967,293 W)
    # 13:00, 15:00, 17:00
    # unsigned long x 3 12 bytes Wh
    if len(edt) == 12:
        v1 = int.from_bytes(edt[0:4], "big")
        v2 = int.from_bytes(edt[4:8], "big")
        v3 = int.from_bytes(edt[8:12], "big")
    else:
        v1 = v2 = v3 = None
    return {"13:00": v1, "15:00": v2, "17:00": v3}


# 0xCF - Consumption of electric energy per hour 2
def _026BCF(edt):
    # 0x0000-0xFFFD (0-65,533W)
    # When shifting at 13:00, 15:00, and 17:00
    # 0x0000: cleared
    # unsigned short x 3 6 bytes Wh
    if len(edt) == 6:
        v1 = int.from_bytes(edt[0:2], "big")
        v2 = int.from_bytes(edt[2:4], "big")
        v3 = int.from_bytes(edt[4:6], "big")
    else:
        v1 = v2 = v3 = None
    return {"13:00": v1, "15:00": v2, "17:00": v3}


class ElectricWaterHeater(EchonetInstance):
    EPC_FUNCTIONS = {
        0xB0: [
            _int,
            {
                0x41: "Automatic",
                0x42: "Manual",
                0x43: "Stop",
            },
        ],
        0xB1: [_int, DICT_41_ON_OFF],
        0xB2: [_int, DICT_41_HEATING_NOT_HEATING],
        0xB3: _int,
        0xB4: _int,
        0xB5: _hh_mm,
        0xB6: [
            _int,
            {
                0x41: "Standard",
                0x42: "Saving",
                0x43: "Extra",
            },
        ],
        0xC0: [
            _int,
            {
                0x41: "Permitted",
                0x42: "Not permitted",
            },
        ],
        0xC1: _int,
        0xC2: _026BC2,
        0xC3: [
            _int,
            {
                0x41: "Supplying hot water",
                0x42: "Stopped",
            },
        ],
        0xC4: _hh_mm,
        0xD1: _int,
        0xD3: _int,
        0xE0: _int,
        0xE1: _int,
        0xE2: _int,
        0xE3: [_int, DICT_41_ON_OFF],
        0xE9: [_int, DICT_41_ON_OFF],
        0xEA: [
            _int,
            {
                0x41: "Filling hot water",
                0x42: "Stopped",
                0x43: "Keeping Temperature",
            },
        ],
        0xE4: [_int, DICT_41_ON_OFF],
        0xE5: [_int, DICT_41_ON_OFF],
        0xE6: [_int, DICT_41_ON_OFF],
        0xE7: _int,
        0xE8: [
            _int,
            {
                0x31: "Level 1",
                0x32: "Level 2",
                0x33: "Level 3",
                0x34: "Level 4",
                0x35: "Level 5",
                0x36: "Level 6",
                0x37: "Level 7",
                0x38: "Level 8",
            },
        ],
        0xEE: _int,
        0xD4: _int,
        0xD5: _int,
        0x90: [_int, DICT_41_ON_OFF],
        0x91: _hh_mm,
        0xD6: _int,
        0xD7: [_int, DICT_41_ON_OFF],
        0xD8: _int,
        0xD9: _026BD9,
        0xDB: _int,
        0xDC: _int,
        0xDD: _int,
        0xC7: [_int, {0x01: "yes", 0x00: "no"}],
        0xC8: [
            _int,
            {
                0x14: "20:00",
                0x15: "21:00",
                0x16: "22:00",
                0x17: "23:00",
                0x18: "24:00",
                0x01: "01:00",
            },
        ],
        0xC9: _int,
        0xCA: [
            _int,
            {
                0x09: "9:00",
                0x0A: "10:00",
                0x0B: "11:00",
                0x0C: "12:00",
                0x0D: "13:00",
                0x0E: "14:00",
                0x0F: "15:00",
                0x10: "16:00",
                0x11: "17:00",
                0x00: "cleared",
            },
        ],
        0xCB: _026BCB,
        0xCC: _026BCC,
        0xCD: [
            _int,
            {
                0x0A: "10:00",
                0x0B: "11:00",
                0x0C: "12:00",
                0x0D: "13:00",
                0x0E: "14:00",
                0x0F: "15:00",
                0x10: "16:00",
                0x11: "17:00",
                0x00: "cleared",
            },
        ],
        0xCE: _026BCE,
        0xCF: _026BCF,
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x6B
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
