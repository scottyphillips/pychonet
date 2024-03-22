from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DATA_STATE_CLOSE,
    DATA_STATE_CLOSING,
    DATA_STATE_FULLY_OPEN,
    DATA_STATE_OPEN,
    DATA_STATE_OPENING,
    DATA_STATE_STOP,
    DICT_41_LOW_MID_HIGH,
    DICT_41_ON_OFF,
    DICT_41_UNLOCK_LOCK,
    DICT_41_YES_NO,
    _int,
)

ENL_OPENSTATE = 0xE0
ENL_OPENING_LEVEL = 0xE1
ENL_BLIND_ANGLE = 0xE2
ENL_OPENCLOSE_STATUS = 0xEA

DICT_41_OPEN_CLOSE_STOP = {
    0x41: DATA_STATE_OPEN,
    0x42: DATA_STATE_CLOSE,
    0x43: DATA_STATE_STOP,
}

DICT_41_COVER_STATE = {
    0x41: DATA_STATE_FULLY_OPEN,
    0x42: DATA_STATE_CLOSE,
    0x43: DATA_STATE_OPENING,
    0x44: DATA_STATE_CLOSING,
    0x45: DATA_STATE_STOP,
}

DICT_41_COVER_STOP_BY = {
    0x41: "Degree-of-setting position: Open",
    0x42: "Operation time setting value: Open",
    0x43: "Operation time setting value: Close",
    0x44: "Local setting position",
    0x45: "User setting 1",
    0x46: "User setting 2",
    0x47: "User setting 3",
    0x48: "User setting 4",
    0x49: "User setting 5",
    0x4A: "User setting 6",
    0x4B: "User setting 7",
    0x4C: "User setting 8",
    0x4D: "User setting 9",
    0x4E: "User setting 10",
}


@deprecated(reason="Scheduled for removal.")
def _0260EO(edt):
    return _int(edt, DICT_41_OPEN_CLOSE_STOP)


# TODO - complete class definitions
#           0x80: 'Operation status',
#           0x89: 'Fault description (Recoverable faults)',
#           0x90: 'Timer operation setting',
#           0xC2: 'Wind detection status',
#           0xC3: 'Sunlight detection status',
#           0xD0: 'Opening (extension) speed setting',
#           0xD1: 'Closing (retraction) speed setting',
#           0xD2: 'Operation time',
#           0xD4: 'Automatic operation setting',
#           0xE1: 'Degree-of-opening level',
#           0xE2: 'Shade angle setting ',
#           0xE3: 'Open/close (extension/retraction) speed',
#           0xE5: 'Electric lock setting',
#           0xE8: 'Remote operation setting status',
#           0xE9: 'Selective opening (extension) operation setting',
#           0xEA: 'Open/closed (extended/retracted) status',
#           0xEE: 'One-time opening (extension) speed setting',
#           0xEF: 'One-time closing (retraction) speed setting'


"""Class for Electric Blind/Shade Objects"""


class ElectricBlind(EchonetInstance):
    EOJGC = 0x02  # Housing/facility-related device group
    EOJCC = 0x60  # Electrically operated blind/shade

    EPC_FUNCTIONS = {
        0xE0: [_int, DICT_41_OPEN_CLOSE_STOP],
        0xC2: [_int, DICT_41_YES_NO],
        0xC3: [_int, DICT_41_YES_NO],
        0xD0: [_int, DICT_41_LOW_MID_HIGH],
        0xD1: [_int, DICT_41_LOW_MID_HIGH],
        0xD2: _int,
        0xD4: [_int, DICT_41_ON_OFF],
        0xE1: _int,
        0xE2: _int,
        0xE3: [_int, DICT_41_LOW_MID_HIGH],
        0xE5: [_int, DICT_41_UNLOCK_LOCK],
        0xE8: [_int, DICT_41_ON_OFF],
        0xE9: [_int, DICT_41_COVER_STOP_BY],
        0xEA: [_int, DICT_41_COVER_STATE],
        0xEE: [_int, DICT_41_LOW_MID_HIGH],
        0xEF: [_int, DICT_41_LOW_MID_HIGH],
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        EchonetInstance.__init__(
            self, host, self.EOJGC, self.EOJCC, instance, api_connector
        )

    """
    getOpenCloseSetting get the status of the blind.

    return: A string representing the blind/shade state
    """

    def getOpenCloseSetting(self):
        return self.getMessage(ENL_OPENSTATE)
