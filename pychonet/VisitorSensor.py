from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_31_8_LEVELS, DICT_41_ON_OFF


class VisitorSensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # Visitor sensor class
        0xB0: [_int, DICT_31_8_LEVELS],  # "Detection threshold level",
        0xB1: [_int, DICT_41_ON_OFF],  # "Visitor detection status",
        0xBE: _int,  # "Visitor detection holding time",
    }

    def __init__(self, host, api_connector, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x08
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
