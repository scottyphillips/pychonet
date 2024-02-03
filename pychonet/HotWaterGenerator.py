from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DICT_30_ON_OFF,
    DICT_41_HEATING_NOT_HEATING,
    DICT_41_ON_OFF,
    _int,
    _hh_mm,
)

# ----- Hot Water Generator -------


@deprecated(reason="Scheduled for removal.")
def _0272D0E2(edt):
    return _int(edt, DICT_41_HEATING_NOT_HEATING)


@deprecated(reason="Scheduled for removal.")
def _0272D2(edt):
    return _int(
        edt,
        {
            0x41: "Hot water warmer operation",
            0x42: "Hot water warmer operation resetting",
        },
    )


@deprecated(reason="Scheduled for removal.")
def _0272EX(edt):
    return _int(edt, DICT_41_ON_OFF)


@deprecated(reason="Scheduled for removal.")
def _0272D7(edt):
    return _int(edt, DICT_30_ON_OFF)


@deprecated(reason="Scheduled for removal.")
def _0272E8(edt):
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


def _0272DA(edt):  # Duration of automatic operation setting
    if edt == 0xFFFF:
        return "Limitless"
    hh = int.from_bytes(edt[0:1], "big")
    mm = str(int.from_bytes(edt[1:2], "big")).zfill(2)
    return f"{hh}:{mm}"


def _0272DB(edt):  # Remaining automatic operation time
    if edt == 0xFFFF:
        return "Infinite"
    hh = int.from_bytes(edt[0:1], "big")
    mm = str(int.from_bytes(edt[1:2], "big")).zfill(2)
    return f"{hh}:{mm}"


@deprecated(reason="Scheduled for removal.")
def _0272EF(edt):  # "Bath operation status monitor",
    return _int(
        edt,
        {
            0x41: "Supplying Hot Water",
            0x43: "Keeping Bath Temperature",
            0x42: "Stopped",
        },
    )


class HotWaterGenerator(EchonetInstance):
    EPC_FUNCTIONS = {
        0xD0: [
            _int,
            DICT_41_HEATING_NOT_HEATING,
        ],  # Hot water heating status
        0xD1: _int,  # Set value of hot water temperature
        0xD2: [
            _int,
            {
                0x41: "Hot water warmer operation",
                0x42: "Hot water warmer operation resetting",
            },
        ],  # Hot water warmer setting
        0xDA: _0272DA,  # Duration of automatic operation setting
        0xDB: _0272DB,  # Remaining automatic operation time
        0xE1: _int,  # Set value of bath of the bath temperature in degrees C
        0xE2: [
            _int,
            DICT_41_HEATING_NOT_HEATING,
        ],  # Bath water heater status
        0xE3: [_int, DICT_41_ON_OFF],  # Bath automatic mode setting
        0xE4: [_int, DICT_41_ON_OFF],  # Bath additional boil-up operation setting
        0xE5: [_int, DICT_41_ON_OFF],  # Bath adding hot water operation setting
        0xE6: [
            _int,
            DICT_41_ON_OFF,
        ],  # Bath water temperature lowering operation setting
        0xE7: _int,  # Bath hot water volume setting 1
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
        ],  # Bath hot water volume setting 2
        0xEE: _int,  # Bath hot water volume setting 3
        0xD4: _int,  # Bath hot water volume setting 4
        0xD5: _int,  # Bath hot water volume setting 4 - Maximum settable level
        0xE9: [_int, DICT_41_ON_OFF],  # "Bathroom priority setting",
        0xEA: [_int, DICT_41_ON_OFF],  # "Shower hot water supply status",
        0xEB: [_int, DICT_41_ON_OFF],  # "Kitchen hot water supply status",
        0xEC: [
            _int,
            DICT_41_ON_OFF,
        ],  # "Hot water warmer ON timer reservation setting",
        0xED: _hh_mm,  # "Set value of hot water warmer ON timer time",
        0xEF: [
            _int,
            {
                0x41: "Supplying Hot Water",
                0x43: "Keeping Bath Temperature",
                0x42: "Stopped",
            },
        ],  # "Bath operation status monitor",
        0x90: [_int, DICT_41_ON_OFF],  # "ON timer reservation setting",
        0x91: _hh_mm,  # "Set value of ON timer time",
        0x92: _hh_mm,  # "Set value of ON timer relative time",
        0xD6: _int,  # "Volume setting",
        0xD7: [_int, DICT_30_ON_OFF],  # "Mute setting",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x72
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
