from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DICT_41_AUTO_8_SPEEDS,
    DICT_41_ON_OFF,
    DICT_41_YES_NO,
    _int,
    _swap_dict,
)

FAN_SPEED = _swap_dict(DICT_41_AUTO_8_SPEEDS)

PHOTOCATALYST_STATUS = _swap_dict(DICT_41_YES_NO)


# ----- Air Cleaner Class -------
# filter change status notify
@deprecated(reason="Scheduled for removal.")
def _0135E1(edt):
    return _int(edt, DICT_41_YES_NO)


# air volume 0x41 for auto
@deprecated(reason="Scheduled for removal.")
def _0135A0(edt):
    return _int(edt, DICT_41_AUTO_8_SPEEDS)


# cigarette sensor status
@deprecated(reason="Scheduled for removal.")
def _0135C1(edt):
    return _int(edt, DICT_41_ON_OFF)


# Photocatalyst setting
@deprecated(reason="Scheduled for removal.")
def _0135C2(edt):
    return _int(edt, DICT_41_ON_OFF)


# air pollution status
@deprecated(reason="Scheduled for removal.")
def _0135C0(edt):
    return _int(edt, {0x41: "pollution", 0x42: "fresh"})


"""Class for Air Cleaner Objects"""


class HomeAirCleaner(EchonetInstance):
    EPC_FUNCTIONS = {
        0xE1: [_int, DICT_41_YES_NO],
        0xA0: [_int, DICT_41_AUTO_8_SPEEDS],
        0xC0: [
            _int,
            {
                0x41: "pollution",
                0x42: "fresh",
            },
        ],
        0xC1: [_int, DICT_41_YES_NO],
        0xC2: [_int, DICT_41_ON_OFF],
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x01  # Air conditioner-related device group
        self._eojcc = 0x35  # Air Cleaner
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    """
    getFilterChangeStatus get the status of filter status.

    return: A string representing the lock status
    """

    def getFilterChangeStatus(self):
        return self.getMessage(0xE1)

    """
    setFanSpeed set the desired fan speed (e.g Low, Medium, High etc)

    param fans_speed: A string representing the fan speed
    """

    def setFanSpeed(self, fan_speed):
        return self.setMessage(0xA0, FAN_SPEED[fan_speed])

    """
    GetFanSpeed gets the current fan speed (e.g Low, Medium, High etc)
    Refer EPC code 0xA0: ('Air flow rate setting')

    return: A string representing the fan speed
    """

    def getFanSpeed(self):  # 0xA0
        return self.getMessage(0xA0)

    """
    getCigaretteSensorStatus get the status of cigarette sensor status.

    return: A string representing the lock status
    """

    def getCigaretteSensorStatus(self):
        return self.getMessage(0xC1)

    """
    getAirPollutionStatus get the status of air pollution status.

    return: A string representing the lock status
    """

    def getAirPollutionStatus(self):
        return self.getMessage(0xC0)

    """
    getPhotocatalystStatus get the status of Photocatalyst status.

    return: A string representing the lock status
    """

    def getPhotocatalystStatus(self):
        return self.getMessage(0xC2)

    """
    setPhotocatalyst set the Photocatalyst status

    param photocatalyst_status: A string representing the Photocatalyst speed
    """

    def setPhotocatalyst(self, photocatalyst_status):
        return self.setMessage(0xC2, PHOTOCATALYST_STATUS[photocatalyst_status])
