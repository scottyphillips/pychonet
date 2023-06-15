from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _hh_mm

@staticmethod
def _03BB80(payload):
    return 'On' if payload == 0x30 else 'Off'

@staticmethod
def _03BBB0(payload):
    return 'Open' if payload == 0x30 else 'Closed'

@staticmethod
def _03BBB1(payload):
    if payload == 0x41:
        return 'Rice cooking completed'
    elif payload == 0x42:
        return 'Rice cooking in progress'
    elif payload == 0x43:
        return 'Rice cooking paused'
    elif payload == 0x44:
        return 'Rice cooking aborted'
    else:
        return 'Unknown'

@staticmethod
def _03BBB2(payload):
    return payload

@staticmethod
def _03BBE1(payload):
    if payload == 0x41:
        return 'Warmer on'
    elif payload == 0x42:
        return 'Warmer off'
    else:
        return 'Unknown warmer setting'

@staticmethod
def _03BBE5(payload):
    if payload == 0x41:
        return 'Inner pot installed'
    elif payload == 0x42:
        return 'Inner pot removed'
    else:
        return 'Unknown inner pot removal status'

@staticmethod
def _03BBE6(payload):
    if payload == 0x41:
        return 'Cover installed'
    elif payload == 0x42:
        return 'Cover removed'
    else:
        return 'Unknown cover removal status'

@staticmethod
def _03BB90(payload):
    return payload

class RiceCooker(EchonetInstance):
    class_codes = {
        'class_group_code': 0x03,
        'class_code': 0xBB
    }

    EPC_FUNCTIONS = {
        0x80: _03BB80,
        0xB0: _03BBB0,
        0xB1: _03BBB1,
        0xB2: _03BBB2,
        0xE1: _03BBE1,
        0xE5: _03BBE5,
        0xE6: _03BBE6,
        0x90: _03BB90,
        0x91: _hh_mm,
        0x92: _hh_mm,
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = self.class_codes['class_group_code']
        self._eojcc = self.class_codes['class_code']
        super().__init__(host, self._eojgc, self._eojcc, instance, api_connector)

    def getOperationStatus(self):
        return self.getMessage(0x80)

    def setOperationStatus(self, status):
        self.setMessage(0x80, status)

    def getCoverStatus(self):
        return self.getMessage(0xB0)

    def getRiceCookingStatus(self):
        return self.getMessage(0xB1)

    def getRiceCookingControlSetting(self):
        return self.getMessage(0xB2)

    def setRiceCookingControlSetting(self, setting):
        self.setMessage(0xB2, setting)

    def getWarmerSetting(self):
        return self.getMessage(0xE1)

    def setWarmerSetting(self, setting):
        self.setMessage(0xE1, setting)

    def getInnerPotRemovalStatus(self):
        return self.getMessage(0xE5)

    def getCoverRemovalStatus(self):
        return self.getMessage(0xE6)

    def getRiceCookingReservationSetting(self):
        return self.getMessage(0x90)

    def setRiceCookingReservationSetting(self, setting):
        self.setMessage(0x90, setting)

    def getRiceCookingReservationSettingTime(self):
        return self.getMessage(0x91)

    def setRiceCookingReservationSettingTime(self, time):
        self.setMessage(0x91, time)

    def getRiceCookingReservationSettingRelativeTime(self):
        return self.getMessage(0x92)

    def setRiceCookingReservationSettingRelativeTime(self, time):
        self.setMessage(0x92, time)

