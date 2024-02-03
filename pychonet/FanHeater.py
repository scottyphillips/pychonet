from pychonet import EchonetInstance
from pychonet.lib.epc_functions import (
    DATA_STATE_OFF,
    DATA_STATE_ON,
    DICT_41_AUTO_NONAUTO,
    DICT_41_ON_OFF,
    _hh_mm,
    _int,
    _signed_int,
)


class FanHeater(EchonetInstance):
    class_codes = {"class_group_code": 0x01, "class_code": 0x43}

    EPC_FUNCTIONS = {
        0xB3: _int,
        0xBB: _signed_int,
        0xB1: [_int, DICT_41_AUTO_NONAUTO],
        0x90: [
            _int,
            {
                0x41: DATA_STATE_ON,
                0x42: DATA_STATE_OFF,
                0x43: "Timer-based ON",
                0x44: "Relative time ON",
            },
        ],
        0x91: _hh_mm,
        0x92: _hh_mm,
        0x94: [
            _int,
            {
                0x41: DATA_STATE_ON,
                0x42: DATA_STATE_OFF,
                0x43: "Timer-based ON",
                0x44: "Relative time ON",
            },
        ],
        0x95: _hh_mm,
        0x96: _hh_mm,
        0xC0: [_int, DICT_41_ON_OFF],
        0xC1: _hh_mm,
        0xC2: [_int, DICT_41_ON_OFF],
        # 0xC3: #Specifies ion emission method implemented in humidifier by bit map,
        # Bit 0: negative ion method mounting
        # Bit 1: cluster ion method mounting
        0xC4: [
            _int,
            {
                0x40: "Empty",
                0x41: "Minimum",
                0x42: "Low",
                0x43: "Middium",
                0x44: "High",
                0x45: "Maximum",
            },
        ],
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = self.class_codes["class_group_code"]
        self._eojcc = self.class_codes["class_code"]
        super().__init__(host, self._eojgc, self._eojcc, instance, api_connector)

    async def getTemperatureSettingValue(self):
        return self.getMessage(0xB3)

    async def setTemperatureSettingValue(self, value):
        self.setMessage(0xB3, value)

    async def getMeasuredTemperature(self):
        return self.getMessage(0xBB)

    async def getAutomaticTemperatureControlSetting(self):
        return self.getMessage(0xB1)

    async def setAutomaticTemperatureControlSetting(self, setting):
        self.setMessage(0xB1, setting)

    async def getOnTimerReservationSetting(self):
        return self.getMessage(0x90)

    async def setOnTimerReservationSetting(self, setting):
        self.setMessage(0x90, setting)

    async def getOnTimerSettingValue(self):
        return self.getMessage(0x91)

    async def setOnTimerSettingValue(self, value):
        self.setMessage(0x91, value)

    async def getOnTimerSettingRelativeTime(self):
        return self.getMessage(0x92)

    async def setOnTimerSettingRelativeTime(self, value):
        self.setMessage(0x92, value)

    async def getOffTimerReservationSetting(self):
        return self.getMessage(0x94)

    async def setOffTimerReservationSetting(self, setting):
        self.setMessage(0x94, setting)

    async def getOffTimerSettingValue(self):
        return self.getMessage(0x95)

    async def setOffTimerSettingValue(self, value):
        self.setMessage(0x95, value)

    async def getOffTimerSettingRelativeTime(self):
        return self.getMessage(0x96)

    async def setOffTimerSettingRelativeTime(self, value):
        self.setMessage(0x96, value)

    async def getExtensionalOperationSetting(self):
        return self.getMessage(0xC0)

    async def setExtensionalOperationSetting(self, setting):
        self.setMessage(0xC0, setting)

    async def getExtensionalOperationTimerTimeSettingValue(self):
        return self.getMessage(0xC1)

    async def setExtensionalOperationTimerTimeSettingValue(self, value):
        self.setMessage(0xC1, value)

    async def getIonEmissionSetting(self):
        return self.getMessage(0xC2)

    async def setIonEmissionSetting(self, setting):
        self.setMessage(0xC2, setting)

    async def getImplementedIonEmissionMethod(self):
        return self.getMessage(0xC3)

    async def getOilAmountLevel(self):
        return self.getMessage(0xC4)
