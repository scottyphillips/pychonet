from pychonet.EchonetInstance import EchonetInstance

ENL_FANSPEED_PERCENT = 0xF0
ENL_FAN_DIRECTION = 0xF1
ENL_FAN_OSCILLATION = 0xF2
ENL_BUZZER = 0xFC
ENL_FAN_POWER = 0x80

FAN_DIRECTION = {
    "forward": 0x41,
    "reverse": 0x42
}

FAN_OSCILLATION = {
    True: 0x30,
    False: 0x31
}

# ----- Ceiling Fan Class -------
# Fan speed in percentage
def _013AF0(edt):
    op_mode = int.from_bytes(edt, "big")
    fan_speed_percentage = int((op_mode - 0x30) * 0x0A)
    return fan_speed_percentage

# Fan Direction
def _013AF1(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "forward", 0x42: "reverse"}
    return values.get(op_mode, "invalid_setting")

# Fan Fluctuation
def _013AF2(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x30: True, 0x31: False}
    return values.get(op_mode, "invalid_setting")

# Fan Buzzer
def _013AFC(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x30: True, 0x31: False}
    return values.get(op_mode, "invalid_setting")

"""Class for Celing Fan Objects"""
class CeilingFan(EchonetInstance):

    EPC_FUNCTIONS = {
        0xF0: _013AF0,
        0xF1: _013AF1,
        0xF2: _013AF2,
        0xFC: _013AFC
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x01  # Air conditioner-related device group
        self._eojcc = 0x3A  # Ceiling Fan
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    """
    setFanSpeedPercent set the desired fan speed in percentage. Will be rounded to the nearest 10% value. 

    param fans_speed: An int representing the fan speed.
    """

    def setFanSpeedPercent(self, fan_speed_percent):
        return self.setMessages(
            [
                {"EPC":ENL_FAN_POWER, "PDC": 0x01, "EDT": 0x30},
                {"EPC":ENL_BUZZER, "PDC": 0x01, "EDT": 0x30},
                {"EPC":ENL_FANSPEED_PERCENT, "PDC": 0x01, "EDT": round(fan_speed_percent/10) + 0x30}
            ]
        )

    """
    GetFanSpeedPercent gets the current fan speed percentage
    Refer EPC code 0xF0: ('Fan Speed')

    return: A string representing the fan speed
    """

    def getFanSpeedPercent(self):  # 0xF0
        return self.getMessage(ENL_FANSPEED_PERCENT)

    """
    setFanDirection set the fan direction 

    param fan_direction: An string representing the fan direction
                            e.g: 'forward', 'reverse'.
    """

    def setFanDirection(self, fan_direction):
        return self.setMessages(
            [
                {"EPC":ENL_FAN_POWER, "PDC": 0x01, "EDT": 0x30},
                {"EPC":ENL_BUZZER, "PDC": 0x01, "EDT": 0x30},
                {"EPC":ENL_FAN_DIRECTION, "PDC": 0x01, "EDT": FAN_DIRECTION[fan_direction]}
            ]
        )

    """
    getFanDirection gets the current fan direction
    Refer EPC code 0xF1: ('Fan Direction')

    return: A string representing the fan direction
    """

    def getFanDirection(self):  # 0xF1
        return self.getMessage(ENL_FAN_DIRECTION)

    """
    setFanOscillation set the fan oscillation

    param fan_oscillation: A boolean representing the fan oscillation status
                            e.g: 'True', 'False'.
    """

    def setFanOscillation(self, fan_oscillation):
        return self.setMessages(
            [
                {"EPC":ENL_FAN_POWER, "PDC": 0x01, "EDT": 0x30},
                {"EPC":ENL_BUZZER, "PDC": 0x01, "EDT": 0x30},
                {"EPC":ENL_FAN_OSCILLATION, "PDC": 0x01, "EDT": FAN_OSCILLATION[fan_oscillation]}
            ]
        )

    """
    getFanOscillation gets the fan oscillation status
    Refer EPC code 0xF2: ('Fan Oscillation')

    return: A boolean representing the fan oscillation status
    """

    def getFanOscillation(self):  # 0xF2
        return self.getMessage(ENL_FAN_OSCILLATION)