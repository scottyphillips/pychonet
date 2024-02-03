import asyncio
from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DATA_STATE_OFF,
    DATA_STATE_ON,
    DICT_41_ON_OFF,
    DICT_41_OPEN_CLOSED,
    DICT_41_UNLOCK_LOCK,
    _int,
)


# ----- Electric Lock Class -------
@deprecated(reason="Scheduled for removal.")
def _026FEX(edt):
    return _int(edt, DICT_41_UNLOCK_LOCK)


@deprecated(reason="Scheduled for removal.")
def _026FE3(edt):
    return _int(edt, DICT_41_OPEN_CLOSED)


@deprecated(reason="Scheduled for removal.")
def _026FE4(edt):
    return _int(edt, {0x41: "occupant", 0x42: "non-occupant"})


@deprecated(reason="Scheduled for removal.")
def _026FE5(edt):
    return _int(
        edt,
        {
            0x40: "normal",
            0x41: "break_open",
            0x42: "door_open",
            0x43: "maunal_unlocked",
            0x44: "tampered",
        },
    )


@deprecated(reason="Scheduled for removal.")
def _026FE6(edt):
    return _int(edt, DICT_41_ON_OFF)


@deprecated(reason="Scheduled for removal.")
def _026FE7(edt):
    return _int(edt, {0x41: "normal", 0x42: "battery_replacement_notification"})


"""Class for Electric Lock Objects"""


class ElectricLock(EchonetInstance):
    EPC_FUNCTIONS = {
        0xE0: [_int, DICT_41_UNLOCK_LOCK],
        0xE1: [_int, DICT_41_UNLOCK_LOCK],
        0xE2: [_int, DICT_41_UNLOCK_LOCK],
        0xE3: [_int, DICT_41_OPEN_CLOSED],
        0xE4: [_int, {0x41: "occupant", 0x42: "non-occupant"}],
        0xE5: [
            _int,
            {
                0x40: "normal",
                0x41: "break_open",
                0x42: "door_open",
                0x43: "maunal_unlocked",
                0x44: "tampered",
            },
        ],
        0xE6: [_int, DICT_41_ON_OFF],
        0xE7: [_int, {0x41: "normal", 0x42: "battery_replacement_notification"}],
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

    async def getLockOneStatus(self):
        return await self.getMessage(0xE1)
