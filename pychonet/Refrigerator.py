from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DICT_41_EMPTY_OR_NOT,
    DICT_41_ENABLED_DISABLED,
    DICT_41_ENABLED_DISABLED_TEMPDISABLED,
    DICT_41_OPEN_CLOSED,
    DICT_41_ON_OFF,
    DICT_41_NORMAL_QUICK_STANDBY,
    DICT_41_YES_NO,
    _int,
    _signed_int,
)


def _03B7E0(edt):
    # First byte: Refrigerator compartment
    # Second byte: Freezer compartment
    # Third byte: Ice compartment
    # Fourth byte: Vegetable compartment
    # Fifth byte: Multi-refrigerating mode compartment
    # Sixth to eighth bytes: Reserved forfuture use.
    refrigerator = _int(edt[0:1])
    freezer = _int(edt[1:2])
    ice = _int(edt[2:3])
    vegetable = _int(edt[3:4])
    multi_refrigerating = _int(edt[4:5])
    # reserved_forfuture_use = _int(edt[5:8])
    return {
        "refrigerator": refrigerator if refrigerator else None,
        "freezer": freezer if freezer else None,
        "ice": ice if ice else None,
        "vegetable": vegetable if vegetable else None,
        "multi_refrigerating": multi_refrigerating if multi_refrigerating else None,
        # "reserved_forfuture_use": reserved_forfuture_use
        # if reserved_forfuture_use
        # else None,
    }


def _03B7D8(edt):
    # First byte: Maximum rotation speed L (0x01–0xFF (1–255))
    # Second byte: Rotation speed of the actual compressor: 0x00 to L (zero speed to highest speed)
    maximum_rotation_speed = _int(edt[0:1])
    rotation_speed = _int(edt[1:2])
    return {
        "maximum_rotation_speed": maximum_rotation_speed,
        "rotation_speed": rotation_speed,
    }


class Refrigerator(EchonetInstance):
    EOJGC = 0x03
    EOJCC = 0xB7

    EPC_FUNCTIONS = {
        0xB0: [_int, DICT_41_OPEN_CLOSED],  # "Door open/close status",
        0xB1: [_int, DICT_41_YES_NO],  # "Door open warning",
        0xB2: [_int, DICT_41_OPEN_CLOSED],  # "Refrigerator compartment door status",
        0xB3: [_int, DICT_41_OPEN_CLOSED],  # "Freezer compartment door status",
        0xB4: [_int, DICT_41_OPEN_CLOSED],  # "Ice compartment door status",
        0xB5: [_int, DICT_41_OPEN_CLOSED],  # "Vegetable compartment door status",
        0xB6: [
            _int,
            DICT_41_OPEN_CLOSED,
        ],  # "Multi-refrigera-ting mode compartment door",
        0xE0: _03B7E0,  # "Maximum allowable temperature setting level",
        0xE2: _signed_int,  # "Refrigerator compartment temperature setting",
        0xE3: _signed_int,  # "Freezer compartment temperature setting",
        0xE4: _signed_int,  # "Ice temperature setting",
        0xE5: _signed_int,  # "Vegetable compartment temperature setting",
        0xE6: _signed_int,  # "Multi-refrigera-ting mode compartment temperature setting",
        0xE9: _int,  # "Refrigerator compartment temperature level setting",
        0xEA: _int,  # "Freezer compartment temperature level setting",
        0xEB: _int,  # "ice compartment temperature level setting",
        0xEC: _int,  # "Vegetable compartment temperature level setting",
        0xED: _int,  # "Multi-refrigera-ting mode compartment temperature level setting",
        0xD1: _signed_int,  # "Measured refrigerator compartment temperature",
        0xD2: _signed_int,  # "Measured freezer compartment temperature",
        0xD3: _signed_int,  # "Measured subzero-fresh compartment temperature",
        0xD4: _signed_int,  # "Measured vegetable compartment temperature",
        0xD5: _signed_int,  # "Measured multi-refrigeratin g mode compartment temperature",
        0xD8: _03B7D8,  # "Compressor rotation speed",
        0xDA: _int,  # "Measured electric current consumption",
        0xDC: _int,  # "Rated power consumption",
        0xA0: [_int, DICT_41_NORMAL_QUICK_STANDBY],  # "Quick freeze function setting",
        0xA1: [
            _int,
            DICT_41_NORMAL_QUICK_STANDBY,
        ],  # "Quick refrigeration function setting",
        0xA4: [_int, DICT_41_ENABLED_DISABLED_TEMPDISABLED],  # "Icemaker setting",
        0xA5: [_int, DICT_41_ENABLED_DISABLED],  # "Icemaker operation status",
        0xA6: [_int, DICT_41_EMPTY_OR_NOT],  # "Icemaker tank status",
        0xA8: [
            _int,
            DICT_41_ON_OFF,
        ],  # "Refrigerator compartment humidification function setting",
        0xA9: [
            _int,
            DICT_41_ON_OFF,
        ],  # "Vegetable compartment humidification function setting",
        0xAD: [_int, DICT_41_ON_OFF],  # "Deodorization function setting",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        EchonetInstance.__init__(
            self, host, self.EOJGC, self.EOJCC, instance, api_connector
        )
