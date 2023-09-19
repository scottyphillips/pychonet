from pychonet.EchonetInstance import EchonetInstance

ENL_FANSPEED_PERCENT = 0xF0
ENL_FAN_DIRECTION = 0xF1
ENL_OSCILLATION = 0xF2

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

"""Class for Celing Fan Objects"""
class CeilingFan(EchonetInstance):

    EPC_FUNCTIONS = {
        0xF0: _013AF0,
        0xA0: _013AF1,
        0xC0: _013AF2,
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
        return self.setMessage(0xF0, round(fan_speed_percent/10) + 0x30)

    """
    GetFanSpeedPercent gets the current fan speed percentage
    Refer EPC code 0xF0: ('Fan Speed')

    return: A string representing the fan speed
    """

    def getFanSpeedPercent(self):  # 0xF0
        return self.getMessage(0xF0)

