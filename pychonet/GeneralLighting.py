from typing import Dict
from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int

ENL_STATUS = 0x80
ENL_BRIGHTNESS = 0xB0
ENL_COLOR_TEMP = 0xB1

# ----- General lighting class -------


@deprecated(reason="Scheduled for removal.")
def _0290B1(edt):
    return _int(
        edt,
        {
            0x40: "other",
            0x41: "incandescent_lamp_color",
            0x42: "white",
            0x43: "daylight_white",
            0x44: "daylight_color",
        },
    )


# TODO - implemenet FUNCTIONS
#   0xB0: 'Illuminance level',
#   0xB2: 'Illuminance level step setting',
#   0xB3: 'Light color step setting',
#   0xB4: 'Maximum specifiable values',
#   0xB5: 'Maximum value of settable level for night lighting',
#   0xB6: 'Lighting mode setting',
#   0xB7: 'Illuminance level setting for main lighting',
#   0xB8: 'Illuminance level step setting for main lighting',
#   0xB9: 'Illuminance level setting for night lighting',
#   0xBA: 'Illuminance level step setting for night lighting',
#   0xBB: 'Light color setting for main lighting',
#   0xBC: 'Light color level step setting for main lighting',
#   0xBD: 'Light color setting for night lighting',
#   0xBE: 'Light color level step setting for night lighting',
#   0xBF: 'Lighting mode status in auto mode',
#   0xC0: 'RGB setting for color lighting',
#   0x90: 'ON timer reservation setting',
#   0x91: 'ON timer setting',
#   0x94: 'OFF timer reservation setting',
#   0x95: 'OFF timer setting'


"""Class for General Lighting Objects"""


class GeneralLighting(EchonetInstance):
    EPC_FUNCTIONS = {
        0xB0: _int,  # Illuminance level
        0xB1: [  # Light color setting
            _int,
            {
                0x40: "other",
                0x41: "incandescent_lamp_color",
                0x42: "white",
                0x43: "daylight_white",
                0x44: "daylight_color",
            },
        ],
        # 0xB2: "Illuminance level step setting",
        # 0xB3: "Light color step setting",
        # 0xB4: "Maximum specifiable values",
        # 0xB5: "Maximum value of settable level for night lighting",
        # 0xB6: "Lighting mode setting",
        # 0xB7: "Illuminance level setting for main lighting",
        # 0xB8: "Illuminance level step setting for main lighting",
        # 0xB9: "Illuminance level setting for night lighting",
        # 0xBA: "Illuminance level step setting for night lighting",
        # 0xBB: "Light color setting for main lighting",
        # 0xBC: "Light color level step setting for main lighting",
        # 0xBD: "Light color setting for night lighting",
        # 0xBE: "Light color level step setting for night lighting",
        # 0xBF: "Lighting mode status in auto mode",
        # 0xC0: "RGB setting for color lighting",
        # 0x90: "ON timer reservation setting",
        # 0x91: "ON timer setting",
        # 0x94: "OFF timer reservation setting",
        # 0x95: "OFF timer setting",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02  # Housing/facility-related device group
        self._eojcc = 0x90  # General Lighting class
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    """
    getBrightness get the brightness that has been set in the light

    return: A string representing the configured brightness.
    """

    async def getBrightness(self):
        return await self.getMessage(ENL_BRIGHTNESS)  # ['brightness']

    """
    setBrightness set the temperature of the light

    param temperature: A string representing the desired temperature.
    """

    async def setBrightness(self, brightness):
        return await self.setMessage(ENL_BRIGHTNESS, int(brightness))

    """
    getColorTemp get the color temperature that has been set in the light

    return: A string representing the configured color temperature. # 68 67 66 64 65 coolest to warmest
    """

    async def getColorTemperature(self):
        return await self.getMessage(ENL_COLOR_TEMP)  # ['color_temperature']

    """
    setColorTemperature set the temperature of the light

    param temperature: A string representing the desired temperature. # 68 67 66 64 65 coolest to warmest
    """

    async def setColorTemperature(self, color_temperature):
        return await self.setMessage(ENL_COLOR_TEMP, color_temperature)

    """
    setLightStates set the light states

    param status: A Dict any light states
    """

    async def setLightStates(self, states: Dict):
        status = states.get("status")
        brightness = states.get("brightness")
        color_temperature = states.get("color_temperature")

        opc = list()

        if status is not None:
            opc.append({"EPC": ENL_STATUS, "PDC": 0x01, "EDT": int(status)})
        if brightness is not None:
            opc.append({"EPC": ENL_BRIGHTNESS, "PDC": 0x01, "EDT": int(brightness)})
        if color_temperature is not None:
            opc.append(
                {"EPC": ENL_COLOR_TEMP, "PDC": 0x01, "EDT": int(color_temperature)}
            )

        return await self.setMessages(opc)
