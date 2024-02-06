from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DICT_41_AUTO_8_SPEEDS,
    _int,
    _signed_int,
    _swap_dict,
)

MODES = {
    "auto": 0x41,
    "cool": 0x42,
    "heat": 0x43,
    "dry": 0x44,
    "fan_only": 0x45,
    "other": 0x40,
    "off": 0xFF,
}
DICT_41_MODES = _swap_dict(MODES)

FAN_SPEED = _swap_dict(DICT_41_AUTO_8_SPEEDS)

SILENT_MODE = {"normal": 0x41, "high-speed": 0x42, "silent": 0x43}

AIRFLOW_HORIZ = {
    "rc-right": 0x41,
    "left-lc": 0x42,
    "lc-center-rc": 0x43,
    "left-lc-rc-right": 0x44,
    "right": 0x51,
    "rc": 0x52,
    "center": 0x54,
    "center-right": 0x55,
    "center-rc": 0x56,
    "center-rc-right": 0x57,
    "lc": 0x58,
    "lc-right": 0x59,
    "lc-rc": 0x5A,
    "left": 0x60,
    "left-right": 0x61,
    "left-rc": 0x62,
    "left-rc-right": 0x63,
    "left-center": 0x64,
    "left-center-right": 0x65,
    "left-center-rc": 0x66,
    "left-center-rc-right": 0x67,
    "left-lc-right": 0x69,
    "left-lc-rc": 0x6A,
}

AIRFLOW_VERT = {
    "upper": 0x41,
    "upper-central": 0x44,
    "central": 0x43,
    "lower-central": 0x45,
    "lower": 0x42,
}

SILENT_MODE = {"normal": 0x41, "high-speed": 0x42, "silent": 0x43}

AUTO_DIRECTION = {"auto": 0x41, "non-auto": 0x42, "auto-vert": 0x43, "auto-horiz": 0x44}

SWING_MODE = {"not-used": 0x31, "vert": 0x41, "horiz": 0x42, "vert-horiz": 0x43}

ENL_STATUS = 0x80
ENL_FANSPEED = 0xA0
ENL_AUTO_DIRECTION = 0xA1
ENL_SWING_MODE = 0xA3
ENL_AIR_VERT = 0xA4
ENL_AIR_HORZ = 0xA5
ENL_HVAC_MODE = 0xB0
ENL_HVAC_SILENT_MODE = 0xB2
ENL_HVAC_SET_TEMP = 0xB3
ENL_HVAC_SET_HUMIDITY = 0xB4
ENL_HVAC_ROOM_HUMIDITY = 0xBA
ENL_HVAC_ROOM_TEMP = 0xBB
ENL_HVAC_OUT_TEMP = 0xBE
ENL_HVAC_HUMIDIFIER_STATE = 0xC1
ENL_HVAC_HUMIDIFIER_VALUE = 0xC4

# ----- Home Air conditioner functions -------


@deprecated(reason="Scheduled for removal.")
def _0130A0(edt):
    return _int(edt, DICT_41_AUTO_8_SPEEDS)


# Automatic control of air flow direction setting
@deprecated(reason="Scheduled for removal.")
def _0130A1(edt):
    return _int(
        edt, {0x41: "auto", 0x42: "non-auto", 0x43: "auto-vert", 0x44: "auto-horiz"}
    )


@deprecated(reason="Scheduled for removal.")
def _0130AA(edt):
    return _int(
        edt,
        {
            0x40: "Normal operation",
            0x41: "Defrosting",
            0x42: "Preheating",
            0x43: "Heat removal",
        },
    )


# Automatic swing of air flow direction setting
@deprecated(reason="Scheduled for removal.")
def _0130A3(edt):
    return _int(
        edt, {0x31: "not-used", 0x41: "vert", 0x42: "horiz", 0x43: "vert-horiz"}
    )


# Air flow direction (vertical) setting
@deprecated(reason="Scheduled for removal.")
def _0130A4(edt):
    return _int(
        edt,
        {
            0x41: "upper",
            0x44: "upper-central",
            0x43: "central",
            0x45: "lower-central",
            0x42: "lower",
        },
    )


# Air flow direction (horiziontal) setting
@deprecated(reason="Scheduled for removal.")
def _0130A5(edt):
    # complies with version 2.01 Release a (page 3-88)
    return _int(
        edt,
        {
            0x41: "rc-right",
            0x42: "left-lc",
            0x43: "lc-center-rc",
            0x44: "left-lc-rc-right",
            0x51: "right",
            0x52: "rc",
            0x54: "center",
            0x55: "center-right",
            0x56: "center-rc",
            0x57: "center-rc-right",
            0x58: "lc",
            0x59: "lc-right",
            0x5A: "lc-rc",
            0x5B: "lc-rc-right",
            0x5C: "lc-center",
            0x5D: "lc-center-right",
            0x5F: "lc-center-rc-right",
            0x60: "left",
            0x61: "left-right",
            0x62: "left-rc",
            0x63: "left-rc-right",
            0x64: "left-center",
            0x65: "left-center-right",
            0x66: "left-center-rc",
            0x67: "left-center-rc-right",
            0x69: "left-lc-right",
            0x6A: "left-lc-rc",
            0x6C: "left-lc-center",
            0x6D: "left-lc-center-right",
            0x6E: "left-lc-center-rc",
            0x6F: "left-lc-center-rc-right",
        },
    )


# Operation mode
@deprecated(reason="Scheduled for removal.")
def _0130B0(edt):
    return _int(edt, DICT_41_MODES)


# Silent mode
@deprecated(reason="Scheduled for removal.")
def _0130B2(edt):
    return _int(
        edt,
        {
            0x41: "normal",
            0x42: "high-speed",
            0x43: "silent",
        },
    )


class HomeAirConditioner(EchonetInstance):
    EPC_FUNCTIONS = {
        0xA0: [_int, DICT_41_AUTO_8_SPEEDS],
        0xA1: [
            _int,
            {0x41: "auto", 0x42: "non-auto", 0x43: "auto-vert", 0x44: "auto-horiz"},
        ],
        0xA3: [
            _int,
            {0x31: "not-used", 0x41: "vert", 0x42: "horiz", 0x43: "vert-horiz"},
        ],
        0xA4: [
            _int,
            {
                0x41: "upper",
                0x44: "upper-central",
                0x43: "central",
                0x45: "lower-central",
                0x42: "lower",
            },
        ],
        0xA5: [
            _int,
            {
                0x41: "rc-right",
                0x42: "left-lc",
                0x43: "lc-center-rc",
                0x44: "left-lc-rc-right",
                0x51: "right",
                0x52: "rc",
                0x54: "center",
                0x55: "center-right",
                0x56: "center-rc",
                0x57: "center-rc-right",
                0x58: "lc",
                0x59: "lc-right",
                0x5A: "lc-rc",
                0x5B: "lc-rc-right",
                0x5C: "lc-center",
                0x5D: "lc-center-right",
                0x5F: "lc-center-rc-right",
                0x60: "left",
                0x61: "left-right",
                0x62: "left-rc",
                0x63: "left-rc-right",
                0x64: "left-center",
                0x65: "left-center-right",
                0x66: "left-center-rc",
                0x67: "left-center-rc-right",
                0x69: "left-lc-right",
                0x6A: "left-lc-rc",
                0x6C: "left-lc-center",
                0x6D: "left-lc-center-right",
                0x6E: "left-lc-center-rc",
                0x6F: "left-lc-center-rc-right",
            },
        ],
        0xAA: [
            _int,
            {
                0x40: "Normal operation",
                0x41: "Defrosting",
                0x42: "Preheating",
                0x43: "Heat removal",
            },
        ],
        0xB0: [_int, DICT_41_MODES],
        0xB2: [
            _int,
            {
                0x41: "normal",
                0x42: "high-speed",
                0x43: "silent",
            },
        ],
        0xBA: _int,
        0xB3: _signed_int,
        0xB4: _signed_int,
        0xBB: _signed_int,
        0xBE: _signed_int,
    }

    """
    Construct a new 'HomeAirConditioner' object.
    In theory this would work for any ECHONET enabled domestic AC.

    :param instance: Instance ID
    :param netif: IP address of node
    """

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x01  # Air conditioner-related device group
        self._eojcc = 0x30  # Home air conditioner class
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    """
    getOperationalTemperature get the temperature that has been set in the HVAC

    return: A integer representing the configured temperature.
    """

    async def getOperationalTemperature(self):
        return await self.getMessage(ENL_HVAC_SET_TEMP)

    """
    getOperationalHumidity get the humidity that has been set in the HVAC

    return: A integer representing the configured humidity.
    """

    async def getOperationalHumidity(self):
        return await self.getMessage(ENL_HVAC_SET_HUMIDITY)

    """
    getRoomHumidity get the HVAC's room humidity.

    return: A integer representing the room humidity.
    """

    async def getRoomHumidity(self):
        return await self.getMessage(ENL_HVAC_ROOM_HUMIDITY)

    """
    getRoomTemperature get the HVAC's room temperature.

    return: A integer representing the room temperature.
    """

    async def getRoomTemperature(self):
        return await self.getMessage(ENL_HVAC_ROOM_TEMP)

    """
    getOutdoorTemperature get the outdoor temperature that has been set in the HVAC

    return: An integer representing the configured outdoor temperature.
    """

    async def getOutdoorTemperature(self):
        return await self.getMessage(ENL_HVAC_OUT_TEMP)

    """
    setOperationalTemperature get the temperature that has been set in the HVAC

    param temperature: A integer representing the desired temperature.
    """

    async def setOperationalTemperature(self, temperature):
        return await self.setMessage(ENL_HVAC_SET_TEMP, int(temperature))

    """
    setOperationalHumidity get the temperature that has been set in the HVAC

    param humidity: A integer representing the desired humidity.
    """

    async def setOperationalHumidity(self, humidity):
        return await self.setMessage(ENL_HVAC_SET_HUMIDITY, int(humidity))

    async def setHeaterHumidifier(self, state, humidity):
        if not state:
            return await self.setMessage(ENL_HVAC_HUMIDIFIER_STATE, 0x42)
        return await self.setMessages(
            [
                {"EPC": ENL_HVAC_HUMIDIFIER_STATE, "PDC": 0x01, "EDT": 0x41},
                {"EPC": ENL_HVAC_HUMIDIFIER_VALUE, "PDC": 0x01, "EDT": humidity},
            ]
        )

    """
    GetMode returns the current configured mode (e.g Heating, Cooling, Fan etc)

    return: A string representing the configured mode.
    """

    async def getMode(self):
        return await self.getMessage(ENL_HVAC_MODE)

    """
    setMode set the desired mode (e.g Heating, Cooling, Fan etc)
    Home Assistant compatabile with 'off' as valid option.
    If HVAC is OFF, setting a mode will switch it on.

    param mode: A string representing the desired mode.
    """

    async def setMode(self, mode):
        if mode == "off":
            return await self.setMessage(ENL_STATUS, 0x31)
        return await self.setMessages(
            [
                {"EPC": ENL_STATUS, "PDC": 0x01, "EDT": 0x30},
                {"EPC": ENL_HVAC_MODE, "PDC": 0x01, "EDT": MODES[mode]},
            ]
        )

    """
    GetFanSpeed gets the current fan speed (e.g Low, Medium, High etc)
    Refer EPC code 0xA0: ('Air flow rate setting')

    return: A string representing the fan speed
    """

    async def getFanSpeed(self):  # 0xA0
        return await self.getMessage(ENL_FANSPEED)

    """
    setFanSpeed set the desired fan speed (e.g Low, Medium, High etc)

    param fans_speed: A string representing the fan speed
    """

    async def setFanSpeed(self, fan_speed):
        return await self.setMessage(ENL_FANSPEED, FAN_SPEED[fan_speed])

    """
    setSwingMode sets the automatic swing mode function

    params swing_mode: A string representing automatic swing mode
                       e.g: 'not-used', 'vert', 'horiz', 'vert-horiz'
    """

    async def setSwingMode(self, swing_mode):
        return await self.setMessage(ENL_SWING_MODE, SWING_MODE[swing_mode])

    """
    getSwingMode gets the swing mode that has been set in the HVAC

    return: A string representing the configured swing mode.
    """

    async def getSwingMode(self):  # 0xA3
        return await self.getMessage(ENL_SWING_MODE)

    """
    setAutoDirection sets the automatic direction mode function

    params auto_direction: A string representing automatic direction mode
                           e.g: 'auto', 'non-auto', 'auto-horiz', 'auto-vert'
    """

    async def setAutoDirection(self, auto_direction):
        return await self.setMessage(ENL_AUTO_DIRECTION, AUTO_DIRECTION[auto_direction])

    """
    getAutoDirection get the direction mode that has been set in the HVAC

    return: A string representing the configured temperature.
    """

    async def getAutoDirection(self):  # 0xA1
        return await self.getMessage(ENL_AUTO_DIRECTION)

    """
    setAirflowVert sets the vertical vane setting

    params airflow_vert: A string representing vertical airflow setting
                         e.g: 'upper', 'upper-central', 'central',
                         'lower-central', 'lower'
    """

    async def setAirflowVert(self, airflow_vert):
        return await self.setMessage(ENL_AIR_VERT, AIRFLOW_VERT[airflow_vert])

    """
    getAirflowVert get the vertical vane setting that has been set in the HVAC

    return: A string representing vertical airflow setting
    """

    async def getAirflowVert(self):  # 0xA4
        return await self.getMessage(ENL_AIR_VERT)

    """
    setAirflowHoriz sets the horizontal vane setting

    params airflow_horiz: A string representing horizontal airflow setting
                          e.g: 'left', 'lc', 'center', 'rc', 'right'
    """

    async def setAirflowHoriz(self, airflow_horiz):
        return await self.setMessage(ENL_AIR_HORZ, AIRFLOW_HORIZ[airflow_horiz])

    """
    getAirflowHoriz get the horizontal vane setting that has been set in the HVAC

    return: A string representing vertical airflow setting e.g: 'left', 'lc', 'center', 'rc', 'right'
    """

    async def getAirflowHoriz(self):  # 0xA5
        return await self.getMessage(ENL_AIR_HORZ)

    """
    setFanMode sets the Fan normal/high-speed/silent operation

    params airflow_mode: A string representing airflow mode setting
                          e.g: 'normal', 'high-speed', 'silent'
    """

    async def setSilentMode(self, mode):  # 0xB2
        return await self.setMessage(ENL_HVAC_SILENT_MODE, SILENT_MODE[mode])

    """
    getFanMode get the Fan normal/high-speed/silent operation

    return: A string representing airflow mode setting e.g: 'normal', 'high-speed', 'silent'
    """

    async def getSilentMode(self):  # 0xB2
        return await self.getMessage(ENL_HVAC_SILENT_MODE)
