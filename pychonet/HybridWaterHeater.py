from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int



# 0xB0 - Automatic water heating setting
def _02A6B0(edt):
    op_mode = int.from_bytes(edt, "big")
    AUTOMATIC_WATER_HEATING_STATES = {
        0x41: "Automatic water heating",
        0x42: "Manual water heating",
        0x43: "Water heating manual stop",
    }
    return AUTOMATIC_WATER_HEATING_STATES.get(op_mode, "Invalid setting")

# 0xB2 - Water heating status
# 0xB3 - Heater status
def _02A6B2B3(edt):
    op_mode = int.from_bytes(edt, "big")
    WATER_HEATING_STATUS = {
        0x41: "Water is heating",
        0x42: "Water is not heating",
    }
    return WATER_HEATING_STATUS.get(op_mode, "Invalid setting")


# 0xB6 - Hot water supply mode setting for auxiliary heat source machine
# 0xB7 - Heater mode setting for auxiliary heat source machine
def _02A6B6B7(edt):
    op_mode = int.from_bytes(edt, "big")
    AUX_SETTING_STATE = {
        0x41: "Set",
        0x42: "No setting",
    }
    return AUX_SETTING_STATE.get(op_mode, "Invalid setting")

# 0xB8 - Linkage mode setting for solar power generation
def _02A6B8(edt):
    op_mode = int.from_bytes(edt, "big")
    SOLAR_POWER_LINKAGE = {
        0x41: "Mode off",
        0x42: "Household consumption",
        0x43: "Prioritizing electricity sales",
        0x44: "Economic efficiency"
    }
    return SOLAR_POWER_LINKAGE.get(op_mode, "Invalid setting")

# 0xB9 - Solar power generations utilization time
def _02A6B9(edt):
    start_hh = int.from_bytes(edt[0:1], "big")
    start_mm = str(int.from_bytes(edt[1:2], "big")).zfill(2)
    end_hh = int.from_bytes(edt[2:3], "big")
    end_mm = str(int.from_bytes(edt[3:4], "big")).zfill(2)
    return { "start_time": f"{start_hh}:{start_mm}", "end_time": f"{end_hh}:{end_mm}" }

# 0xC3 - Hot water supply status
def _02A6C3(edt):
    op_mode = int.from_bytes(edt, "big")
    HOT_WATER_SUPPLY_STATUS = {
        0x41: "Supplying hot water",
        0x42: "Not supplying hot water",
    }
    return HOT_WATER_SUPPLY_STATUS.get(op_mode, "Invalid setting")

# 0xE1 - Measured amount of hot water remaining in tank
# 0xE2 - Tank Capacity

class HybridWaterHeater(EchonetInstance):

    EPC_FUNCTIONS = {
        0xB0: _02A6B0,
        0xB2: _02A6B2B3,
        0xB3: _02A6B2B3,
        0xB6: _02A6B6B7,
        0xB7: _02A6B6B7,
        0xB8: _02A6B8,
        0xB9: _02A6B9,
        0xC3: _02A6C3,
        0xE1: _int,
        0xE2: _int
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0xA6
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
