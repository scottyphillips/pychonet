#TODO fix this ChatGPT created code. 
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _hh_mm, _int

# Static methods for ElectricStorageHeater
def _0155B3(payload):
    return _int(payload)

def _0155B8(payload):
    return _int(payload)

def _0155BB(payload):
    return _int(payload)

def _0155BE(payload):
    return _int(payload)

def _0155A0(payload):
    return _int(payload)

def _0155A1(payload):
    if payload == 0x30:
        return 'Fan operation ON'
    elif payload == 0x31:
        return 'Fan operation OFF'
    else:
        return 'Unknown fan operation status'

def _0155C0(payload):
    if payload == 0x41:
        return 'Heat storage ON'
    elif payload == 0x42:
        return 'Heat storage OFF'
    else:
        return 'Unknown heat storage operation status'

def _0155C1(payload):
    return _int(payload)

def _0155C2(payload):
    return _int(payload)

def _0155C3(payload):
    if payload == 0x41:
        return 'Daytime heat storage enabled'
    elif payload == 0x42:
        return 'Daytime heat storage disabled'
    else:
        return 'Unknown daytime heat storage setting'

def _0155C4(payload):
    if payload == 0x41:
        return 'Daytime heat storage available'
    elif payload == 0x42:
        return 'Daytime heat storage not available'
    else:
        return 'Unknown daytime heat storage ability'

def _0155C5(payload):
    return _int(payload)

def _0155C6(payload):
    return _hh_mm(payload)

def _0155C7(payload):
    if payload == 0x41:
        return 'Radiant heat method'
    elif payload == 0x42:
        return 'Air heat method'
    elif payload == 0x43:
        return 'Radiant and air heat method'
    else:
        return 'Unknown radiation method'

def _0155C8(payload):
    if payload == 0x41:
        return 'Child lock enabled'
    elif payload == 0x42:
        return 'Child lock disabled'
    else:
        return 'Unknown child lock setting'

def _0155D0(payload):
    return _int(payload)

def _0155D1(payload):
    return _hh_mm(payload)

def _0155D2(payload):
    return _hh_mm(payload)

def _0155D3(payload):
    return _int(payload)

class ElectricStorageHeater(EchonetInstance):
    class_codes = {
        'class_group_code': 0x01,
        'class_code': 0x55
    }

    EPC_FUNCTIONS = {
        0xB3: _0155B3,
        0xB8: _0155B8,
        0xBB: _0155BB,
        0xBE: _0155BE,
        0xA0: _0155A0,
        0xA1: _0155A1,
        0xC0: _0155C0,
        0xC1: _0155C1,
        0xC2: _0155C2,
        0xC3: _0155C3,
        0xC4: _0155C4,
        0xC5: _0155C5,
        0xC6: _0155C6,
        0xC7: _0155C7,
        0xC8: _0155C8,
        0xD0: _0155D0,
        0xD1: _hh_mm,
        0xD2: _hh_mm,
        0xD3: _0155D3,
        0xD4: _hh_mm,
        0xD5: _hh_mm,
    }

    def __init__(self, host, device):
        super().__init__(host, device)

    def getTemperatureSetting(self):
        return self.getMessage(0xB3)

    def getRatedPowerConsumption(self):
        return self.getMessage(0xB8)

    def getMeasuredIndoorTemperature(self):
        return self.getMessage(0xBB)

    def getMeasuredOutdoorTemperature(self):
        return self.getMessage(0xBE)

    def getAirFlowRateSetting(self):
        return self.getMessage(0xA0)

    def setAirFlowRateSetting(self, setting):
        self.setMessage(0xA0, setting)

    def getFanOperationStatus(self):
        return self.getMessage(0xA1)

    def setFanOperationStatus(self, status):
        self.setMessage(0xA1, status)

    def getHeatStorageOperationStatus(self):
        return self.getMessage(0xC0)

    def setHeatStorageOperationStatus(self, status):
        self.setMessage(0xC0, status)

    def getHeatStorageTemperatureSetting(self):
        return self.getMessage(0xC1)

    def setHeatStorageTemperatureSetting(self, temperature):
        self.setMessage(0xC1, temperature)

    def getMeasuredStoredHeatTemperature(self):
        return self.getMessage(0xC2)

    def getDaytimeHeatStorageSetting(self):
        return self.getMessage(0xC3)

    def setDaytimeHeatStorageSetting(self, setting):
        self.setMessage(0xC3, setting)

    def getDaytimeHeatStorageAbility(self):
        return self.getMessage(0xC4)

    def getMidnightPowerDurationSetting(self):
        return self.getMessage(0xC5)

    def setMidnightPowerDurationSetting(self, duration):
        self.setMessage(0xC5, duration)

    def getMidnightPowerStartTimeSetting(self):
        return self.getMessage(0xC6)

    def setMidnightPowerStartTimeSetting(self, time):
        self.setMessage(0xC6, time)

    def getRadiationMethod(self):
        return self.getMessage(0xC7)

    def setRadiationMethod(self, method):
        self.setMessage(0xC7, method)

    def getChildLockSetting(self):
        return self.getMessage(0xC8)

    def setChildLockSetting(self, setting):
        self.setMessage(0xC8, setting)

    def getFanTimer1Setting(self):
        return self.getMessage(0xD0)

    def setFanTimer1Setting(self, setting):
        self.setMessage(0xD0, setting)

    def getFanTimer1ONTimeSetting(self):
        return self.getMessage(0xD1)

    def setFanTimer1ONTimeSetting(self, time):
        self.setMessage(0xD1, time)

    def getFanTimer1OFFTimeSetting(self):
        return self.getMessage(0xD2)

    def setFanTimer1OFFTimeSetting(self, time):
        self.setMessage(0xD2, time)

    def getFanTimer2Setting(self):
        return self.getMessage(0xD3)

    def setFanTimer2Setting(self, setting):
        self.setMessage(0xD3, setting)

    def getFanTimer2ONTimeSetting(self):
        return self.getMessage(0xD4)

    def setFanTimer2ONTimeSetting(self, time):
        self.setMessage(0xD4, time)

    def getFanTimer2OFFTimeSetting(self):
        return self.getMessage(0xD5)

    def setFanTimer2OFFTimeSetting(self, time):
        self.setMessage(0xD5, time)
