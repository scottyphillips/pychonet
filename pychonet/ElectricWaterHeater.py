from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DICT_41_HEATING_NOT_HEATING,
    DICT_41_ON_OFF,
    _int,
    _hh_mm,
)


# 0xB0 - Automatic water heating setting
@deprecated(reason="Scheduled for removal.")
def _026BB0(edt):
    return _int(
        edt,
        {
            0x41: "Automatic",
            0x42: "Manual",
            0x43: "Stop",
        },
    )


# 0xB1 - Automatic water temperature control setting
@deprecated(reason="Scheduled for removal.")
def _026BB1(edt):
    return _int(edt, DICT_41_ON_OFF)


# 0xB2 - Water heating status
@deprecated(reason="Scheduled for removal.")
def _026BB2(edt):
    return _int(edt, DICT_41_HEATING_NOT_HEATING)


# 0xB5 Relative time setting value for manual water heating OFF
@deprecated(reason="Scheduled for removal.")
def _026BB5(edt):
    return _hh_mm(edt)


# 0xB6 - Tank Operation mode setting
@deprecated(reason="Scheduled for removal.")
def _026BB6(edt):
    return _int(edt, {0x41: "Standard", 0x42: "Saving", 0x43: "Extra"})


# 0xC0 - Daytime reheating permission setting
@deprecated(reason="Scheduled for removal.")
def _026BC0(edt):
    return _int(
        edt,
        {
            0x41: "Permitted",
            0x42: "Not permitted",
        },
    )


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


# 0xB9 - Solar power generations utilization time
def _026BB9(edt):
    start_hh = int.from_bytes(edt[0:1], "big")
    start_mm = str(int.from_bytes(edt[1:2], "big")).zfill(2)
    end_hh = int.from_bytes(edt[2:3], "big")
    end_mm = str(int.from_bytes(edt[3:4], "big")).zfill(2)
    return {"start_time": f"{start_hh}:{start_mm}", "end_time": f"{end_hh}:{end_mm}"}


# 0xC3 - Hot water supply status
@deprecated(reason="Scheduled for removal.")
def _026BC3(edt):
    return _int(
        edt,
        {
            0x41: "Supplying hot water",
            0x42: "Stopped",
        },
    )


# 0xC4 Relative time setting for keeping bath temperature
@deprecated(reason="Scheduled for removal.")
def _026BC4(edt):
    return _hh_mm(edt)


# 0xE1 - Measured amount of hot water remaining in tank

# 0xE2 - Tank Capacity


# 0xE3 - Automatic bath water heater mode setting
@deprecated(reason="Scheduled for removal.")
def _026BE3(edt):
    return _int(edt, DICT_41_ON_OFF)


# 0xE9 - Bathroom Priority setting
@deprecated(reason="Scheduled for removal.")
def _026BE9(edt):
    return _int(edt, DICT_41_ON_OFF)


# 0xEA - Bath operation status monitor
@deprecated(reason="Scheduled for removal.")
def _026BEA(edt):
    return _int(
        edt,
        {
            0x41: "Filling hot water",
            0x42: "Stopped",
            0x43: "Keeping Temperature",
        },
    )


# 0xE4 - Manual bath reheating function setting
@deprecated(reason="Scheduled for removal.")
def _026BE4(edt):
    return _int(edt, DICT_41_ON_OFF)


# 0xE5 - Manual bath hot water addition function setting
@deprecated(reason="Scheduled for removal.")
def _026BE5(edt):
    return _int(edt, DICT_41_ON_OFF)


# 0xE6 - Manual lukewarm water temperature lowering function setting
@deprecated(reason="Scheduled for removal.")
def _026BE6(edt):
    return _int(edt, DICT_41_ON_OFF)


# 0xE7 - Bath Volume water setting one


# 0xE8 - Bath Volume water setting two
@deprecated(reason="Scheduled for removal.")
def _026BE8(edt):
    return _int(
        edt,
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
    )


# 0xEE - Bath Volume water setting three

# 0xD4 - Bath Volume water setting four

# 0xD5 - Bath Volume water setting four maximum settable level


# 0x90 - ON timer reservation setting
@deprecated(reason="Scheduled for removal.")
def _026B90(edt):
    return _int(edt, DICT_41_ON_OFF)


# 0x91 - ON timer setting
@deprecated(reason="Scheduled for removal.")
def _026B91(edt):
    return _hh_mm(edt)


# 0xD6 - Sound Volume Setting


# 0xD7 - Mute Setting
@deprecated(reason="Scheduled for removal.")
def _026BD7(edt):
    return _int(edt, DICT_41_ON_OFF)


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
    return "not implemented"


# 0xCC - Consumption of electric energy per hour 1
def _026BCC(edt):
    return "not implemented"


# 0xCE - Expected electric energy at daytime heating shift time 2
def _026BCE(edt):
    return "not implemented"


# 0xCF - Consumption of electric energy per hour 2
def _026BCF(edt):
    return "not implemented"


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
        0xE9: _int,
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
        0xC7: _int,
        0xC8: _int,  # could change
        0xC9: _int,
        0xCA: _int,
        0xCB: _026BCB,  # todo
        0xCC: _026BCC,  # todo
        0xCD: _int,
        0xCE: _026BCB,  # todo
        0xCF: _026BCF,  # todo
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x6B
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
