from pychonet.EchonetInstance import EchonetInstance

ENL_OPENSTATE = 0xE0


def _0260EO(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "open", 0x42: "close", 0x43: "stop"}
    return values.get(op_mode, "invalid_setting")


# TODO - complete class definitions
# 			0x80: 'Operation status',
# 			0x89: 'Fault description (Recoverable faults)',
# 			0x90: 'Timer operation setting',
# 			0xC2: 'Wind detection status',
# 			0xC3: 'Sunlight detection status',
# 			0xD0: 'Opening (extension) speed setting',
# 			0xD1: 'Closing (retraction) speed setting',
# 			0xD2: 'Operation time',
# 			0xD4: 'Automatic operation setting',
# 			0xE1: 'Degree-of-opening level',
# 			0xE2: 'Shade angle setting ',
# 			0xE3: 'Open/close (extension/retraction) speed',
# 			0xE5: 'Electric lock setting',
# 			0xE8: 'Remote operation setting status',
# 			0xE9: 'Selective opening (extension) operation setting',
# 			0xEA: 'Open/closed (extended/retracted) status',
# 			0xEE: 'One-time opening (extension) speed setting',
# 			0xEF: 'One-time closing (retraction) speed setting'


"""Class for Electric Blind/Shade Objects"""


class ElectricBlind(EchonetInstance):

    EPC_FUNCTIONS = {0xE0: _0260EO}

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02  # Housing/facility-related device group
        self._eojcc = 0x60  # Electrically operated blind/shade
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    """
    getOpenCloseSetting get the status of the blind.

    return: A string representing the blind/shade state
    """

    def getOpenCloseSetting(self):
        return self.getMessage(ENL_OPENSTATE)
