from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DATA_STATE_OFF,
    DATA_STATE_ON,
    DICT_30_ON_OFF,
    DICT_30_TRUE_FALSE,
)
from pychonet.lib.epc_functions import _int, _swap_dict

ENL_FANSPEED_PERCENT = 0xF0
ENL_FAN_DIRECTION = 0xF1
ENL_FAN_OSCILLATION = 0xF2
ENL_BUZZER = 0xFC
ENL_FAN_POWER = 0x80
ENL_FAN_LIGHT_STATUS = 0xF3
ENL_FAN_LIGHT_BRIGHTNESS = 0xF5
ENL_FAN_LIGHT_COLOR_TEMP = 0xF6

DICT_FAN_DIRECTION = {0x41: "forward", 0x42: "reverse"}

FAN_DIRECTION = _swap_dict(DICT_FAN_DIRECTION)

FAN_OSCILLATION = _swap_dict(DICT_30_TRUE_FALSE)


# ----- Ceiling Fan Class -------
# Fan speed in percentage
def _013AF0(edt):
    op_mode = int.from_bytes(edt, "big")
    fan_speed_percentage = int((op_mode - 0x30) * 0x0A)
    return fan_speed_percentage


# Fan Direction
@deprecated(reason="Scheduled for removal.")
def _013AF1(edt):
    return _int(edt, DICT_FAN_DIRECTION)


# Fan Fluctuation
@deprecated(reason="Scheduled for removal.")
def _013AF2(edt):
    return _int(edt, DICT_30_TRUE_FALSE)


# Fan Buzzer
@deprecated(reason="Scheduled for removal.")
def _013AFC(edt):
    return _int(edt, DICT_30_TRUE_FALSE)


"""Class for Celing Fan Objects"""


class CeilingFan(EchonetInstance):
    EPC_FUNCTIONS = {
        0xF0: _013AF0,
        0xF1: [_int, DICT_FAN_DIRECTION],
        0xF2: [_int, DICT_30_TRUE_FALSE],
        0xFC: [_int, DICT_30_TRUE_FALSE],
        0xF3: [_int, DICT_30_ON_OFF],
        0xF4: [_int, {0x42: "normal", 0x43: "night"}],
        0xF5: _int,
        0xF6: _int,
        0xF7: [_int, {0x01: "low", 0x32: "medium", 0x64: "high"}],
    }
    SPEED_COUNT = 10
    LIGHT_ON_OFF = _swap_dict(DICT_30_ON_OFF)

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

    async def setFanSpeedPercent(self, fan_speed_percent):
        return await self.setMessages(
            [
                {"EPC": ENL_FAN_POWER, "PDC": 0x01, "EDT": 0x30},
                {"EPC": ENL_BUZZER, "PDC": 0x01, "EDT": 0x30},
                {
                    "EPC": ENL_FANSPEED_PERCENT,
                    "PDC": 0x01,
                    "EDT": round(fan_speed_percent / 10) + 0x30,
                },
            ]
        )

    """
    GetFanSpeedPercent gets the current fan speed percentage
    Refer EPC code 0xF0: ('Fan Speed')

    return: A string representing the fan speed
    """

    async def getFanSpeedPercent(self):  # 0xF0
        return await self.getMessage(ENL_FANSPEED_PERCENT)

    """
    setFanDirection set the fan direction 

    param fan_direction: An string representing the fan direction
                            e.g: 'forward', 'reverse'.
    """

    async def setFanDirection(self, fan_direction):
        return await self.setMessages(
            [
                {"EPC": ENL_FAN_POWER, "PDC": 0x01, "EDT": 0x30},
                {"EPC": ENL_BUZZER, "PDC": 0x01, "EDT": 0x30},
                {
                    "EPC": ENL_FAN_DIRECTION,
                    "PDC": 0x01,
                    "EDT": FAN_DIRECTION[fan_direction],
                },
            ]
        )

    """
    getFanDirection gets the current fan direction
    Refer EPC code 0xF1: ('Fan Direction')

    return: A string representing the fan direction
    """

    async def getFanDirection(self):  # 0xF1
        return await self.getMessage(ENL_FAN_DIRECTION)

    """
    setFanOscillation set the fan oscillation

    param fan_oscillation: A boolean representing the fan oscillation status
                            e.g: 'True', 'False'.
    """

    async def setFanOscillation(self, fan_oscillation):
        return await self.setMessages(
            [
                {"EPC": ENL_FAN_POWER, "PDC": 0x01, "EDT": 0x30},
                {"EPC": ENL_BUZZER, "PDC": 0x01, "EDT": 0x30},
                {
                    "EPC": ENL_FAN_OSCILLATION,
                    "PDC": 0x01,
                    "EDT": FAN_OSCILLATION[fan_oscillation],
                },
            ]
        )

    """
    getFanOscillation gets the fan oscillation status
    Refer EPC code 0xF2: ('Fan Oscillation')

    return: A boolean representing the fan oscillation status
    """

    async def getFanOscillation(self):  # 0xF2
        return await self.getMessage(ENL_FAN_OSCILLATION)

    """
    Light On sets the node to ON.

    """

    async def light_on(self):  # EPC 0xF3
        return await self.setMessage(
            ENL_FAN_LIGHT_STATUS, self.LIGHT_ON_OFF[DATA_STATE_ON]
        )

    """
    Light Off sets the node to OFF.

    """

    async def light_off(self):  # EPC 0xF3
        return await self.setMessage(
            ENL_FAN_LIGHT_STATUS, self.LIGHT_ON_OFF[DATA_STATE_OFF]
        )

    """
    getBrightness get the brightness that has been set in the light

    return: A string representing the configured brightness.
    """

    def getBrightness(self):
        return self.getMessage(ENL_FAN_LIGHT_BRIGHTNESS)  # ['brightness']

    """
    setBrightness set the brightness of the light

    param temperature: A string representing the desired brightness.
    """

    def setBrightness(self, brightness):
        return self.setMessage(ENL_FAN_LIGHT_BRIGHTNESS, int(brightness))

    """
    getColorTemp get the color temperature that has been set in the light

    return: A string representing the configured color temperature.
    """

    def getColorTemperature(self):
        # return self.getMessage(ENL_FAN_LIGHT_COLOR_TEMP)  # ['color_temperature']
        # calculate some helper
        return self.getMessage(ENL_FAN_LIGHT_COLOR_TEMP)

    """
    setColorTemperature set the temperature of the light

    param temperature: A string representing the desired temperature.
    """

    def setColorTemperature(self, color_temperature):
        return self.setMessage(ENL_FAN_LIGHT_COLOR_TEMP, color_temperature)
