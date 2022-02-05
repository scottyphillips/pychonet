from pychonet.EchonetInstance import EchonetInstance

FAN_SPEED = {
    "auto": 0x41,
    "minimum": 0x31,
    "low": 0x32,
    "medium-low": 0x33,
    "medium": 0x34,
    "medium-high": 0x35,
    "high": 0x36,
    "very-high": 0x37,
    "max": 0x38,
}

PHOTOCATALYST_STATUS = {"yes": 0x41, "no": 0x42}


# ----- Air Cleaner Class -------
# filter change status notify
def _0135E1(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {
        0x41: "yes",
        0x42: "no",
    }
    return values.get(op_mode, "invalid_setting")


# air volume 0x41 for auto
def _0135A0(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {
        0x41: "auto",
        0x31: "minimum",
        0x32: "low",
        0x33: "medium-low",
        0x34: "medium",
        0x35: "medium-high",
        0x36: "high",
        0x37: "very-high",
        0x38: "max",
    }
    return values.get(op_mode, "invalid_setting")


# cigarette sensor status
def _0135C1(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "yes", 0x42: "no"}
    return values.get(op_mode, "invalid_setting")


# Photocatalyst setting
def _0135C2(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "on", 0x42: "off"}
    return values.get(op_mode, "invalid_setting")


# air pollution status
def _0135C0(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "pollution", 0x42: "fresh"}
    return values.get(op_mode, "invalid_setting")


"""Class for Air Cleaner Objects"""


class HomeAirCleaner(EchonetInstance):

    EPC_FUNCTIONS = {
        0xE1: _0135E1,
        0xA0: _0135A0,
        0xC0: _0135C0,
        0xC1: _0135C1,
        0xC2: _0135C1,
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
