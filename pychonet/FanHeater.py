from pychonet import EchonetInstance
from pychonet.lib.epc_functions import _hh_mm, _int

@staticmethod
def _0143BB(payload):
    return str(payload)

@staticmethod
def _0143B1(payload):
    return str(payload)

@staticmethod
def _014390(payload):
    return str(payload)

@staticmethod
def _014394(payload):
    return str(payload)

@staticmethod
def _0143C0(payload):
    if payload == 0x41:
        return 'Extension ON'
    elif payload == 0x42:
        return 'Extension OFF'
    else:
        return 'Unknown'

@staticmethod
def _0143C2(payload):
    if payload == 0x41:
        return 'Ion emission ON'
    elif payload == 0x42:
        return 'Ion emission OFF'
    else:
        return 'Unknown'

@staticmethod
def _0143C3(payload):
    return str(payload)

@staticmethod
def _0143C4(payload):
    return str(payload)

class FanHeater(EchonetInstance):
    class_codes = {
        'class_group_code': 0x01,
        'class_code': 0x43
    }

    EPC_FUNCTIONS = {
        0xB3: _int,
        0xBB: _0143BB,
        0xB1: _0143B1,
        0x90: _014390,
        0x91: _hh_mm,
        0x92: _hh_mm,
        0x94: _014394,
        0x95: _hh_mm,
        0x96: _hh_mm,
        0xC0: _0143C0,
        0xC1: _hh_mm,
        0xC2: _0143C2,
        0xC3: _0143C3,
        0xC4: _0143C4,
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = self.class_codes['class_group_code']
        self._eojcc = self.class_codes['class_code']
        super().__init__(host, self._eojgc, self._eojcc, instance, api_connector)

    def getTemperatureSettingValue(self):
        return self.getMessage(0xB3)

    def setTemperatureSettingValue(self, value):
        self.setMessage(0xB3, value)

    def getMeasuredTemperature(self):
        return self.getMessage(0xBB)

    def getAutomaticTemperatureControlSetting(self):
        return self.getMessage(0xB1)

    def setAutomaticTemperatureControlSetting(self, setting):
        self.setMessage(0xB1, setting)

    def getOnTimerReservationSetting(self):
        return self.getMessage(0x90)

    def setOnTimerReservationSetting(self, setting):
        self.setMessage(0x90, setting)

    def getOnTimerSettingValue(self):
        return self.getMessage(0x91)

    def setOnTimerSettingValue(self, value):
        self.setMessage(0x91, value)

    def getOnTimerSettingRelativeTime(self):
        return self.getMessage(0x92)

    def setOnTimerSettingRelativeTime(self, value):
        self.setMessage(0x92, value)

    def getOffTimerReservationSetting(self):
        return self.getMessage(0x94)

    def setOffTimerReservationSetting(self, setting):
        self.setMessage(0x94, setting)

    def getOffTimerSettingValue(self):
        return self.getMessage(0x95)

    def setOffTimerSettingValue(self, value):
        self.setMessage(0x95, value)

    def getOffTimerSettingRelativeTime(self):
        return self.getMessage(0x96)

    def setOffTimerSettingRelativeTime(self, value):
        self.setMessage(0x96, value)

    def getExtensionalOperationSetting(self):
        return self.getMessage(0xC0)

    def setExtensionalOperationSetting(self, setting):
        self.setMessage(0xC0, setting)

    def getExtensionalOperationTimerTimeSettingValue(self):
        return self.getMessage(0xC1)

    def setExtensionalOperationTimerTimeSettingValue(self, value):
        self.setMessage(0xC1, value)

    def getIonEmissionSetting(self):
        return self.getMessage(0xC2)

    def setIonEmissionSetting(self, setting):
        self.setMessage(0xC2, setting)

    def getImplementedIonEmissionMethod(self):
        return self.getMessage(0xC3)

    def getOilAmountLevel(self):
        return self.getMessage(0xC4)

