from pychonet.EchonetInstance import EchonetInstance


# ----- Electric Lock Class -------
def _026FEX(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "lock", 0x42: "unlock"}
    return values.get(op_mode, "invalid_setting")


def _026FE3(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "open", 0x42: "closed"}
    return values.get(op_mode, "invalid_setting")


def _026FE4(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "occupant", 0x42: "non-occupant"}
    return values.get(op_mode, "invalid_setting")


def _026FE5(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {
        0x40: "normal",
        0x41: "break_open",
        0x42: "door_open",
        0x43: "maunal_unlocked",
        0x44: "tampered",
    }
    return values.get(op_mode, "invalid_setting")


def _026FE6(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "on", 0x42: "off"}
    return values.get(op_mode, "invalid_setting")


def _026FE7(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "normal", 0x42: "battery_replacement_notification"}
    return values.get(op_mode, "invalid_setting")


"""Class for Electric Lock Objects"""


class ElectricLock(EchonetInstance):

    EPC_FUNCTIONS = {
        0xE0: _026FEX,
        0xE1: _026FEX,
        0xE2: _026FEX,
        0xE3: _026FE3,
        0xE4: _026FE4,
        0xE5: _026FE5,
        0xE6: _026FE6,
        0xE7: _026FE7,
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02  # Housing/facility-related device group
        self._eojcc = 0x6F  # Electric Lock
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    """
    getLockOneStatus get the status of lock one.

    return: A string representing the lock status
    """

    def getLockOneStatus(self):
        return self.getMessage(0xE1)
