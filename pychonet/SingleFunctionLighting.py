from pychonet.EchonetInstance import EchonetInstance
from pychonet.GeneralLighting import ENL_BRIGHTNESS

# ----- Single function lighting class -------


# TODO - implemenet FUNCTIONS
# 	0xB0: 'Illuminance level setting',


"""Class for Single Function Lighting Objects"""


class SingleFunctionLighting(EchonetInstance):
    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02  # Housing/facility-related device group
        self._eojcc = 0x91  # Single Function Lighting class
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    """
    getBrightness get the brightness that has been set in the light

    return: A string representing the configured brightness.
    """

    def getBrightness(self):
        return self.getMessage(ENL_BRIGHTNESS)  # ['brightness']

    """
    setBrightness set the temperature of the light

    param temperature: A string representing the desired temperature.
    """

    def setBrightness(self, brightness):
        return self.setMessage(ENL_BRIGHTNESS, int(brightness))
