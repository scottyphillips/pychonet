from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DATA_STATE_CLOSE,
    DATA_STATE_OPEN,
    DATA_STATE_STOP,
    _int,
)

ENL_OPENSTATE = 0xE0

DICT_41_OPEN_CLOSE_STOP = {
    0x41: DATA_STATE_OPEN,
    0x42: DATA_STATE_CLOSE,
    0x43: DATA_STATE_STOP,
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
