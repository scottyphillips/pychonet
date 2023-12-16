from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int


# 0xB0 - Automatic water heating setting
def _026BB0(edt):
    op_mode = int.from_bytes(edt, "big")
    AUTOMATIC_WATER_HEATING_STATES = {
        0x41: "Automatic",
        0x42: "Manual",
        0x43: "Stop",
    }
    return AUTOMATIC_WATER_HEATING_STATES.get(op_mode, "Invalid setting")


# 0xB1 - Automatic water temperature control setting
def _026BB1(edt):
    op_mode = int.from_bytes(edt, "big")
    AUTOMATIC_WATER_TEMP_CONTROL = {
        0x41: "On",
        0x42: "Off",
    }
    return AUTOMATIC_WATER_TEMP_CONTROL.get(op_mode, "Invalid setting")


# 0xB2 - Water heating status
def _026BB2(edt):
    op_mode = int.from_bytes(edt, "big")
    WATER_HEATING_STATUS = {
        0x41: "Heating",
        0x42: "Not Heating",
    }
    return WATER_HEATING_STATUS.get(op_mode, "Invalid setting")


# 0xB5 Relative time setting value for manual water heating OFF
def _026BB5(edt):
    hh = int.from_bytes(edt[0:1], "big")
    mm = str(int.from_bytes(edt[1:2], "big")).zfill(2)
    return f"{hh}:{mm}"


# 0xB6 - Tank Operation mode setting
def _026BB6(edt):
    op_mode = int.from_bytes(edt, "big")
    WATER_HEATING_STATUS = {0x41: "Standard", 0x42: "Saving", 0x43: "Extra"}
    return WATER_HEATING_STATUS.get(op_mode, "Invalid setting")


# 0xC0 - Daytime reheating permission setting
def _026BC0(edt):
    op_mode = int.from_bytes(edt, "big")
    AUX_SETTING_STATE = {
        0x41: "Permitted",
        0x42: "Not permitted",
    }
    return AUX_SETTING_STATE.get(op_mode, "Invalid setting")


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
def _026BC3(edt):
    op_mode = int.from_bytes(edt, "big")
    HOT_WATER_SUPPLY_STATUS = {
        0x41: "Supplying hot water",
        0x42: "Not supplying hot water",
    }
    return HOT_WATER_SUPPLY_STATUS.get(op_mode, "Invalid setting")


# 0xC4 Relative time setting for keeping bath temperature
def _026BC4(edt):
    hh = int.from_bytes(edt[0:1], "big")
    mm = str(int.from_bytes(edt[1:2], "big")).zfill(2)
    return f"{hh}:{mm}"


# 0xE1 - Measured amount of hot water remaining in tank

# 0xE2 - Tank Capacity


# 0xE3 - Automatic bath water heater mode setting
def _026BE3(edt):
    op_mode = int.from_bytes(edt, "big")
    AUTOMATIC_SETTING = {
        0x41: "On",
        0x42: "Off",
    }
    return AUTOMATIC_SETTING.get(op_mode, "Invalid setting")


# 0xE9 - Bathroom Priority setting
def _026BE9(edt):
    op_mode = int.from_bytes(edt, "big")
    PRIORITY_SETTING = {
        0x41: "On",
        0x42: "Off",
    }
    return PRIORITY_SETTING.get(op_mode, "Invalid setting")


# 0xEA - Bath operation status monitor
def _026BEA(edt):
    op_mode = int.from_bytes(edt, "big")
    OPERATION_STATUS_MONITOR = {
        0x41: "Filling hot water",
        0x42: "Stopped",
        0x43: "Keeping Temperature",
    }
    return OPERATION_STATUS_MONITOR.get(op_mode, "Invalid setting")


# 0xE4 - Manual bath reheating function setting
def _026BE4(edt):
    op_mode = int.from_bytes(edt, "big")
    REHEAT_FUNCTON = {
        0x41: "On",
        0x42: "Off",
    }
    return REHEAT_FUNCTON.get(op_mode, "Invalid setting")


# 0xE5 - Manual bath hot water addition function setting
def _026BE5(edt):
    op_mode = int.from_bytes(edt, "big")
    ADDITION_FUNCTION = {
        0x41: "On",
        0x42: "Off",
    }
    return ADDITION_FUNCTION.get(op_mode, "Invalid setting")


# 0xE6 - Manual lukewarm water temperature lowering function setting
def _026BE6(edt):
    op_mode = int.from_bytes(edt, "big")
    LUKEWARM = {
        0x41: "On",
        0x42: "Off",
    }
    return LUKEWARM.get(op_mode, "Invalid setting")


# 0xE7 - Bath Volume water setting one


# 0xE8 - Bath Volume water setting two
def _026BE8(edt):
    op_mode = int.from_bytes(edt, "big")
    VOLUME = {
        0x31: "Level 1",
        0x32: "Level 2",
        0x33: "Level 3",
        0x34: "Level 4",
        0x35: "Level 5",
        0x36: "Level 6",
        0x37: "Level 7",
        0x38: "Level 8",
    }
    return VOLUME.get(op_mode, "Invalid setting")


# 0xEE - Bath Volume water setting three

# 0xD4 - Bath Volume water setting four

# 0xD5 - Bath Volume water setting four maximum settable level


# 0x90 - ON timer reservation setting
def _026B90(edt):
    op_mode = int.from_bytes(edt, "big")
    RESERVATION_SETTING = {
        0x41: "On",
        0x42: "Off",
    }
    return RESERVATION_SETTING.get(op_mode, "Invalid setting")


# 0x91 - ON timer setting
def _026B91(edt):
    hh = int.from_bytes(edt[0:1], "big")
    mm = str(int.from_bytes(edt[1:2], "big")).zfill(2)
    return {"time": f"{hh}:{mm}"}

# 0xD6 - Sound Volume Setting

# 0xD7 - Mute Setting
def _026BD7(edt):
    op_mode = int.from_bytes(edt, "big")
    MUTE_SETTING = {
        0x41: "On",
        0x42: "Off",
    }
    return MUTE_SETTING.get(op_mode, "Invalid setting")

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
    return("not implemented")

# 0xCC - Consumption of electric energy per hour 1
def _026BCC(edt):
    return("not implemented")

# 0xCE - Expected electric energy at daytime heating shift time 2
def _026BCE(edt):
    return("not implemented")

# 0xCF - Consumption of electric energy per hour 2
def _026BCF(edt):
    return("not implemented")


class ElectricWaterHeater(EchonetInstance):
    EPC_FUNCTIONS = {
        0xB0: _026BB0,
        0xB1: _026BB1,
        0xB2: _026BB2,
        0xB3: _int,
        0xB4: _int,
        0xB5: _026BB5,
        0xB6: _026BB6,
        0xC0: _026BC0,
        0xC1: _int,
        0xC2: _026BC2,
        0xC3: _026BC3,
        0xC4: _026BC4,
        0xD1: _int,
        0xD3: _int,
        0xE0: _int,
        0xE1: _int,
        0xE2: _int,
        0xE3: _026BE3,
        0xE9: _026BE9,
        0xEA: _026BEA,
        0xE4: _026BE4,
        0xE5: _026BE5,
        0xE6: _026BE6,
        0xE7: _int,
        0xE8: _026BE8,
        0xE9: _int,
        0xEE: _int,
        0xD4: _int,
        0xD5: _int,
        0x90: _026B90,
        0x91: _026B91,
        0xD6: _int,
        0xD7: _026BD7,
        0xD8: _int,
        0xD9: _026BD9,
        0xDB: _int,
        0xDC: _int,
        0xDD: _int,
        0xC7: _int,
        0xC8: _int, # could change
        0xC9: _int,
        0xCA: _int,
        0xCB: _026BCB, #todo
        0xCC: _026BCC, #todo
        0xCD: _int,
        0xCE: _026BCB, #todo
        0xCF: _026BCF #todo
        
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x6B
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
