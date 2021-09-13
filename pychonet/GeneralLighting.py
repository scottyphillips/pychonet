from pychonet.EchonetInstance import EchonetInstance

ENL_LIGHTCOLORSETTING = 0xB1

# ----- General lighting class -------
def _0290B1(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
       0x40: 'other',
       0x41: 'incandescent_lamp_color',
       0x42: 'white',
       0x43: 'daylight_white',
       0x43: 'daylight_color',
    }
    return values.get(op_mode, "invalid_setting")

# TODO - implemenet FUNCTIONS		
		# 	0xB0: 'Illuminance level',
		# 	0xB2: 'Illuminance level step setting',
		# 	0xB3: 'Light color step setting',
		# 	0xB4: 'Maximum specifiable values',
		# 	0xB5: 'Maximum value of settable level for night lighting',
		# 	0xB6: 'Lighting mode setting',
		# 	0xB7: 'Illuminance level setting for main lighting',
		# 	0xB8: 'Illuminance level step setting for main lighting',
		# 	0xB9: 'Illuminance level setting for night lighting',
		# 	0xBA: 'Illuminance level step setting for night lighting',
		# 	0xBB: 'Light color setting for main lighting',
		# 	0xBC: 'Light color level step setting for main lighting',
		# 	0xBD: 'Light color setting for night lighting',
		# 	0xBE: 'Light color level step setting for night lighting',
		# 	0xBF: 'Lighting mode status in auto mode',
		# 	0xC0: 'RGB setting for color lighting',
		# 	0x90: 'ON timer reservation setting',
		# 	0x91: 'ON timer setting',
		# 	0x94: 'OFF timer reservation setting',
		# 	0x95: 'OFF timer setting'


"""Class for General Lighting Objects"""
class GeneralLighing(EchonetInstance):

    EPC_FUNCTIONS = {
        0xB1: _0290B1
    }

    def __init__(self, host, api_connector = None, instance = 0x1):
        self._eojgc = 0x02 # Housing/facility-related device group
        self._eojcc = 0x90 # General Lighting class
        EchonetInstance.__init__(self, host, self._eojgc, self._eojcc, instance, api_connector)

    """
    getOpenCloseSetting get the status of the blind.

    return: A string representing the blind/shade state
    """
    def getLightColorSetting(self):
        return self.getMessage(ENL_LIGHTCOLORSETTING)
