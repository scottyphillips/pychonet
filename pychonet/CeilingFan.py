from typing import Dict
from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.GeneralLighting import ENL_BRIGHTNESS, ENL_COLOR_TEMP
from pychonet.lib.const import EFFECT_OFF, ENL_OFF, ENL_ON, ENL_SETMAP, ENL_STATUS
from pychonet.lib.epc_functions import DICT_30_ON_OFF, DICT_30_TRUE_FALSE
from pychonet.lib.epc_functions import _int, _swap_dict

ENL_FANSPEED_PERCENT = 0xF0
ENL_FAN_DIRECTION = 0xF1
ENL_FAN_OSCILLATION = 0xF2
ENL_FAN_LIGHT_STATUS = 0xF3
ENL_FAN_LIGHT_MODE = 0xF4
ENL_FAN_LIGHT_BRIGHTNESS = 0xF5
ENL_FAN_LIGHT_COLOR_TEMP = 0xF6
ENL_FAN_LIGHT_NIGHT_BRIGHTNESS = 0xF7
ENL_BUZZER = 0xFC

DICT_FAN_DIRECTION = {0x41: "forward", 0x42: "reverse"}
DICT_FAN_LIGHT_EFFECTS = {
    0x00: EFFECT_OFF,
    0x01: "night_low",
    0x32: "night_medium",
    0x64: "night_high",
}

FAN_DIRECTION = _swap_dict(DICT_FAN_DIRECTION)

FAN_OSCILLATION = _swap_dict(DICT_30_TRUE_FALSE)

FAN_LIGHT_EFFECTS = _swap_dict(DICT_FAN_LIGHT_EFFECTS)


# ----- Ceiling Fan Class -------
# Fan speed in percentage
def _013AF0(edt):
    op_mode = _int(edt)
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
        0xF3: [_int, DICT_30_ON_OFF],
        0xF4: [_int, {0x42: "normal", 0x43: "night"}],
        0xF5: _int,
        0xF6: _int,
        0xF7: [_int, {0x01: "low", 0x32: "medium", 0x64: "high"}],
        0xFC: [_int, DICT_30_TRUE_FALSE],
    }
    SPEED_COUNT = 10

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x01  # Air conditioner-related device group
        self._eojcc = 0x3A  # Ceiling Fan
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    """
    setMessage is used to fire ECHONET set messages to set Node information
    Assumes one OPC is sent per message.

    :param tx_epc: EPC byte code for the request.
    :param tx_edt: EDT data relevant to the request.
    :return: True if sucessful, false if request message failed
    """

    async def setMessage(self, epc, edt, pdc=0x01):
        response = await self.setMessages(
            [
                {"EPC": ENL_STATUS, "PDC": 0x01, "EDT": ENL_ON},
                {"EPC": ENL_BUZZER, "PDC": 0x01, "EDT": ENL_ON},
                {"EPC": epc, "PDC": pdc, "EDT": edt},
            ]
        )
        if not response:
            return False
        return True

    """
    On sets the node to ON.

    """

    async def on(self):  # EPC 0x80
        return await super().setMessage(ENL_STATUS, ENL_ON)

    """
    Off sets the node to OFF.

    """

    async def off(self):  # EPC 0x80
        return await super().setMessage(ENL_STATUS, ENL_OFF)

    """
    setFanSpeedPercent set the desired fan speed in percentage. Will be rounded to the nearest 10% value. 

    param fans_speed: An int representing the fan speed.
    """

    async def setFanSpeedPercent(self, fan_speed_percent):
        return await self.setMessage(
            ENL_FANSPEED_PERCENT, round(fan_speed_percent / 10) + 0x30
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
        return await self.setMessage(ENL_FAN_DIRECTION, FAN_DIRECTION[fan_direction])

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
        return await self.setMessage(
            ENL_FAN_OSCILLATION, FAN_OSCILLATION[fan_oscillation]
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
        return await self.setLightStates({"status": ENL_ON})

    """
    Light Off sets the node to OFF.

    """

    async def light_off(self):  # EPC 0xF3
        return await super().setMessage(ENL_FAN_LIGHT_STATUS, ENL_OFF)

    """
    getBrightness get the brightness that has been set in the light

    return: A string representing the configured brightness.
    """

    async def getBrightness(self):
        return await self.getMessage(ENL_FAN_LIGHT_BRIGHTNESS)  # ['brightness']

    """
    setBrightness set the brightness of the light

    param temperature: A string representing the desired brightness.
    """

    async def setBrightness(self, brightness):
        return await self.setLightStates({"brightness": int(brightness)})

    """
    getColorTemp get the color temperature that has been set in the light

    return: A string representing the configured color temperature.
    """

    async def getColorTemperature(self):
        # return self.getMessage(ENL_FAN_LIGHT_COLOR_TEMP)  # ['color_temperature']
        # calculate some helper
        return await self.getMessage(ENL_FAN_LIGHT_COLOR_TEMP)

    """
    setColorTemperature set the temperature of the light

    param temperature: A string representing the desired temperature.
    """

    async def setColorTemperature(self, color_temperature):
        return await self.setLightStates({"color_temperature": int(color_temperature)})

    """
    setLightStates set the light states

    param status: A Dict any light states
    """

    async def setLightStates(self, states: Dict):
        # Not specified, but implemented based on user reports
        # see https://github.com/scottyphillips/echonetlite_homeassistant/issues/142#issuecomment-2344285168
        epc_codes = {
            ENL_STATUS: None,  # 0x80
            ENL_FANSPEED_PERCENT: None,  # 0xF0
            ENL_FAN_DIRECTION: None,  # 0xF1
            ENL_FAN_OSCILLATION: None,  # 0xF2
            ENL_FAN_LIGHT_STATUS: "status",  # 0xF3
            ENL_FAN_LIGHT_MODE: None,  # 0xF4
            ENL_FAN_LIGHT_BRIGHTNESS: "brightness",  # 0xF5
            ENL_FAN_LIGHT_COLOR_TEMP: "color_temperature",  # 0xF6
        }

        # Check effect for F7 Nightlight Brightness
        effect_value = None  # or "night_low", "night_medium", "night_high"
        if "effect" in states:
            if states["effect"] in ["night_low", "night_medium", "night_high"]:
                effect_value = states["effect"]
                self._epc_data[ENL_FAN_LIGHT_MODE] = 0x43.to_bytes(1)
            else:
                self._epc_data[ENL_FAN_LIGHT_MODE] = 0x42.to_bytes(1)
        night_mode = (
            _int(self._epc_data.get(ENL_FAN_LIGHT_MODE, 0x0.to_bytes(1))) == 0x43
        )

        opc = list()
        for epc, name in epc_codes.items():
            if name:
                if value := states.get(name):
                    opc.append({"EPC": epc, "PDC": 0x01, "EDT": int(value)})
                    continue
            if epc in self._epc_data:
                opc.append(
                    {"EPC": epc, "PDC": 0x01, "EDT": _int(self._epc_data.get(epc))}
                )

        # Add F7 Nightlight Brightness
        if night_mode:
            night_brightness_int = (
                FAN_LIGHT_EFFECTS[effect_value]
                if effect_value
                else _int(
                    self._epc_data.get(
                        ENL_FAN_LIGHT_NIGHT_BRIGHTNESS,
                        FAN_LIGHT_EFFECTS["night_high"].to_bytes(1),
                    )
                )
            )
            opc.append(
                {
                    "EPC": ENL_FAN_LIGHT_NIGHT_BRIGHTNESS,
                    "PDC": 0x01,
                    "EDT": night_brightness_int,
                }
            )

        # Add 0xFC Buzzer
        opc.append({"EPC": ENL_BUZZER, "PDC": 0x01, "EDT": ENL_ON})

        return await self.setMessages(opc)

    def getEffectList(self):
        """Get Effect List

        Returns:
            list|None: Effect list or None
        """
        if (
            ENL_FAN_LIGHT_MODE in self._epc_data[ENL_SETMAP]
            and ENL_FAN_LIGHT_NIGHT_BRIGHTNESS in self._epc_data[ENL_SETMAP]
        ):
            return list(DICT_FAN_LIGHT_EFFECTS.values())
        return None

    def getEffect(self):
        """Get Current Effect

        Returns:
            string: Value of current effect
        """
        if (
            ENL_FAN_LIGHT_MODE in self._epc_data
            and ENL_FAN_LIGHT_NIGHT_BRIGHTNESS in self._epc_data
        ):
            if _int(self._epc_data[ENL_FAN_LIGHT_MODE]) != 0x43:
                return EFFECT_OFF

            return DICT_FAN_LIGHT_EFFECTS.get(
                _int(
                    self._epc_data.get(ENL_FAN_LIGHT_NIGHT_BRIGHTNESS, 0x0.to_bytes(1))
                ),
                EFFECT_OFF,
            )
        return EFFECT_OFF
