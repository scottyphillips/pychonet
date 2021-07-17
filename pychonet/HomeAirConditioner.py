from pychonet.EchonetInstance import EchonetInstance

MODES = {
	'auto':  	0x41,
	'cool':  	0x42,
	'heat':  	0x43,
	'dry':  	0x44,
	'fan_only':	0x45,
	'other': 	0x40,
    'off'   :   0xFF
}

FAN_SPEED = {
	'auto':	        0x41,
	'minimum':  	0x31,
	'low':  		0x32,
	'medium-low': 	0x33,
	'medium':		0x34,
	'medium-high': 	0x35,
	'high':			0x36,
	'very-high':    0x37,
	'max':			0x38
}

AIRFLOW_HORIZ = {
    'rc-right':             0x41,
    'left-lc':              0x42,
    'lc-center-rc':         0x43,
    'left-lc-rc-right':     0x44,
    'right':                0x51,
    'rc':                   0x52,
    'center':               0x54,
    'center-right':         0x55,
    'center-rc':            0x56,
    'center-rc-right':      0x57,
    'lc':                   0x58,
    'lc-right':             0x59,
    'lc-rc':                0x5A,
    'left':                 0x60,
    'left-right':           0x61,
    'left-rc':              0x62,
    'left-rc-right':        0x63,
    'left-center':          0x64,
    'left-center-right':    0x65,
    'left-center-rc':       0x66,
    'left-center-rc-right': 0x67,
    'left-lc-right':        0x69,
    'left-lc-rc':           0x6A
}

AIRFLOW_VERT = {
    'upper':            0x41,
    'upper-central':    0x44,
    'central':          0x43,
    'lower-central':    0x45,
    'lower':            0x42
}

AUTO_DIRECTION = {
    'auto':         0x41,
    'non-auto':     0x42,
    'auto-vert':    0x43,
    'auto-horiz':   0x44
}

    # Automatic swing of air flow direction setting

SWING_MODE = {
    'not-used':     0x31,
    'vert':         0x41,
    'horiz':        0x42,
    'vert-horiz':   0x43
}

ENL_STATUS = 0x80
ENL_FANSPEED = 0xA0
ENL_AUTO_DIRECTION = 0xA1
ENL_SWING_MODE = 0xA3
ENL_AIR_VERT = 0xA4
ENL_AIR_HORZ = 0xA5
ENL_HVAC_MODE = 0xB0
ENL_HVAC_SET_TEMP = 0xB3
ENL_HVAC_ROOM_TEMP = 0xBB
ENL_HVAC_OUT_TEMP = 0xBE


"""Class for Home AirConditioner Objects"""
class HomeAirConditioner(EchonetInstance):

    """
    Construct a new 'HomeAirConditioner' object.
    In theory this would work for any ECHONET enabled domestic AC.

    :param instance: Instance ID
    :param netif: IP address of node
    """
    def __init__(self, netif, instance = 0x1):
        self.eojgc = 0x01 #	Air conditioner-related device group
        self.eojcc = 0x30 # Home air conditioner class
        EchonetInstance.__init__(self, self.eojgc, self.eojcc, instance, netif)

    """
    GetOperationaTemperature get the temperature that has been set in the HVAC

    return: A string representing the configured temperature.
    """
    def getOperationalTemperature(self):
        return self.update(ENL_HVAC_SET_TEMP)


    """
    getRoomTemperature get the HVAC's room temperature.

    return: A integer representing the room temperature.
    """
    def getRoomTemperature(self):
        return self.update(ENL_HVAC_ROOM_TEMP)


    """
    getOutdoorTemperature get the outdoor temperature that has been set in the HVAC

    return: An integer representing the configured outdoor temperature.
    """
    def getOutdoorTemperature(self):
         return self.update(ENL_HVAC_OUT_TEMP)

    """
    setOperationalTemperature get the temperature that has been set in the HVAC

    param temperature: A string representing the desired temperature.
    """
    def setOperationalTemperature(self, temperature):
        return self.setMessage([{'EPC': ENL_HVAC_SET_TEMP, 'PDC': 0x01, 'EDT': int(temperature)}])

    """
    GetMode returns the current configured mode (e.g Heating, Cooling, Fan etc)

    return: A string representing the configured mode.
    """
    def getMode(self):
        return self.update(ENL_HVAC_MODE)

    """
    setMode set the desired mode (e.g Heating, Cooling, Fan etc)
    Home Assistant compatabile with 'off' as valid option.
    If HVAC is OFF, setting a mode will switch it on.

    param mode: A string representing the desired mode.
    """
    def setMode(self, mode):
        if mode == 'off':
            return self.setMessage([{'EPC': ENL_STATUS, 'PDC': 0x01, 'EDT': 0x31}])
        #
        return self.setMessage([{'EPC': ENL_STATUS, 'PDC': 0x01, 'EDT': 0x30},{'EPC': ENL_HVAC_MODE, 'PDC': 0x01, 'EDT': MODES[mode]}])

    """
    GetFanSpeed gets the current fan speed (e.g Low, Medium, High etc)
    Refer EPC code 0xA0: ('Air flow rate setting')

    return: A string representing the fan speed
    """
    def getFanSpeed(self): #0xA0
        return self.update(ENL_FANSPEED)


    """
    setFanSpeed set the desired fan speed (e.g Low, Medium, High etc)

    param fans_speed: A string representing the fan speed
    """
    def setFanSpeed(self, fan_speed):
        return self.setMessage([{'EPC': ENL_FANSPEED, 'PDC': 0x01, 'EDT': FAN_SPEED[fan_speed]}])

    """
    setSwingMode sets the automatic swing mode function

    params swing_mode: A string representing automatic swing mode
                       e.g: 'not-used', 'vert', 'horiz', 'vert-horiz'
    """
    def setSwingMode(self, swing_mode):
        return self.setMessage([{'EPC': ENL_SWING_MODE, 'PDC': 0x01, 'EDT': SWING_MODE[swing_mode]}])

    """
    getSwingMode gets the swing mode that has been set in the HVAC

    return: A string representing the configured swing mode.
    """
    def getSwingMode(self): #0xA3
        return self.update(ENL_SWING_MODE)

    """
    setAutoDirection sets the automatic direction mode function

    params auto_direction: A string representing automatic direction mode
                           e.g: 'auto', 'non-auto', 'auto-horiz', 'auto-vert'
    """
    def setAutoDirection (self, auto_direction):
        return self.setMessage([{'EPC': ENL_AUTO_DIRECTION, 'PDC': 0x01, 'EDT': AUTO_DIRECTION[auto_direction]}])

    """
    getAutoDirection get the direction mode that has been set in the HVAC

    return: A string representing the configured temperature.
    """
    def getAutoDirection(self): #0xA1
        return self.update(ENL_AUTO_DIRECTION)

    """
    setAirflowVert sets the vertical vane setting

    params airflow_vert: A string representing vertical airflow setting
                         e.g: 'upper', 'upper-central', 'central',
                         'lower-central', 'lower'
    """
    def setAirflowVert (self, airflow_vert):
        return self.setMessage([{'EPC': ENL_AIR_VERT, 'PDC': 0x01, 'EDT': AIRFLOW_VERT[airflow_vert]}])

    """
    getAirflowVert get the vertical vane setting that has been set in the HVAC

    return: A string representing vertical airflow setting
    """
    def getAirflowVert(self): #0xA4
        return self.update(ENL_AIR_VERT)


    """
    setAirflowHoriz sets the horizontal vane setting

    params airflow_horiz: A string representing horizontal airflow setting
                         e.g: 'left', 'lc', 'center', 'rc', 'right'
    """
    def setAirflowHoriz (self, airflow_horiz):
        return self.setMessage([{'EPC': ENL_AIR_HORZ, 'PDC': 0x01, 'EDT': AIRFLOW_HORIZ[airflow_horiz]}])

    """
    getAirflowHoriz get the horizontal vane setting that has been set in the HVAC

    return: A string representing vertical airflow setting e.g: 'left', 'lc', 'center', 'rc', 'right'
    """
    def getAirflowHoriz(self): #0xA5
        return self.update(ENL_AIR_HORZ)
