from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import DICT_41_HEATING_NOT_HEATING, _int, _signed_int


# 0xB0 - Automatic water heating setting
@deprecated(reason="Scheduled for removal.")
def _02A6B0(edt):
    return _int(
        edt,
        {
            0x41: "Automatic water heating",
            0x42: "Manual water heating",
            0x43: "Water heating manual stop",
        },
    )


# 0xB2 - Water heating status
# 0xB3 - Heater status
@deprecated(reason="Scheduled for removal.")
def _02A6B2B3(edt):
    return _int(edt, DICT_41_HEATING_NOT_HEATING)


# 0xB6 - Hot water supply mode setting for auxiliary heat source machine
# 0xB7 - Heater mode setting for auxiliary heat source machine
@deprecated(reason="Scheduled for removal.")
def _02A6B6B7(edt):
    return _int(
        edt,
        {
            0x41: "Set",
            0x42: "No setting",
        },
    )


# 0xB8 - Linkage mode setting for solar power generation
@deprecated(reason="Scheduled for removal.")
def _02A6B8(edt):
    return _int(
        edt,
        {
            0x41: "Mode off",
            0x42: "Household consumption",
            0x43: "Prioritizing electricity sales",
            0x44: "Economic efficiency",
        },
    )


# 0xB9 - Solar power generations utilization time
def _02A6B9(edt):
    start_hh = int.from_bytes(edt[0:1], "big")
    start_mm = str(int.from_bytes(edt[1:2], "big")).zfill(2)
    end_hh = int.from_bytes(edt[2:3], "big")
    end_mm = str(int.from_bytes(edt[3:4], "big")).zfill(2)
    return {"start_time": f"{start_hh}:{start_mm}", "end_time": f"{end_hh}:{end_mm}"}


# 0xC3 - Hot water supply status
@deprecated(reason="Scheduled for removal.")
def _02A6C3(edt):
    return _int(
        edt,
        {
            0x41: "Supplying Hot Water",
            0x42: "Stopped",
        },
    )


# 0xE1 - Measured amount of hot water remaining in tank
# 0xE2 - Tank Capacity


class HybridWaterHeater(EchonetInstance):
    EPC_FUNCTIONS = {
        0xB0: [
            _int,
            {
                0x41: "Automatic water heating",
                0x42: "Manual water heating",
                0x43: "Water heating manual stop",
            },
        ],
        0xB2: [_int, DICT_41_HEATING_NOT_HEATING],
        0xB3: [_int, DICT_41_HEATING_NOT_HEATING],
        0xB6: [
            _int,
            {
                0x41: "Set",
                0x42: "No setting",
            },
        ],
        0xB7: [
            _int,
            {
                0x41: "Set",
                0x42: "No setting",
            },
        ],
        0xB8: [
            _int,
            {
                0x41: "Mode off",
                0x42: "Household consumption",
                0x43: "Prioritizing electricity sales",
                0x44: "Economic efficiency",
            },
        ],
        0xB9: _02A6B9,
        0xC3: [
            _int,
            {
                0x41: "Supplying Hot Water",
                0x42: "Stopped",
            },
        ],
        0xE1: _int,
        0xE2: _int,
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0xA6
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
