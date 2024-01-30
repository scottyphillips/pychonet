from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DICT_30_ON_OFF,
    DICT_30_OPEN_CLOSED,
    DICT_41_ON_OFF,
    _hh_mm,
    _int,
)


class RiceCooker(EchonetInstance):
    class_codes = {"class_group_code": 0x03, "class_code": 0xBB}

    EPC_FUNCTIONS = {
        0x80: [_int, DICT_30_ON_OFF],
        0xB0: [_int, DICT_30_OPEN_CLOSED],
        0xB1: [
            _int,
            {
                0x41: "Rice cooking completed",
                0x42: "Rice cooking in progress",
                0x43: "Rice cooking paused",
                0x44: "Rice cooking aborted",
            },
        ],
        0xB2: [_int, {0x41: "Start/Restart", 0x42: "Pause"}],
        0xE1: [_int, DICT_41_ON_OFF],
        0xE5: [_int, {0x41: "Installed", 0x42: "Removed"}],
        0xE6: [_int, {0x41: "Installed", 0x42: "Removed"}],
        0x90: [_int, DICT_41_ON_OFF],
        0x91: _hh_mm,
        0x92: _hh_mm,
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = self.class_codes["class_group_code"]
        self._eojcc = self.class_codes["class_code"]
        super().__init__(host, self._eojgc, self._eojcc, instance, api_connector)

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        return await self.setMessage(0x80, status)

    async def getCoverStatus(self):
        return await self.getMessage(0xB0)

    async def getRiceCookingStatus(self):
        return await self.getMessage(0xB1)

    async def getRiceCookingControlSetting(self):
        return await self.getMessage(0xB2)

    async def setRiceCookingControlSetting(self, setting):
        return await self.setMessage(0xB2, setting)

    async def getWarmerSetting(self):
        return await self.getMessage(0xE1)

    async def setWarmerSetting(self, setting):
        return await self.setMessage(0xE1, setting)

    async def getInnerPotRemovalStatus(self):
        return await self.getMessage(0xE5)

    async def getCoverRemovalStatus(self):
        return await self.getMessage(0xE6)

    async def getRiceCookingReservationSetting(self):
        return await self.getMessage(0x90)

    async def setRiceCookingReservationSetting(self, setting):
        return await self.setMessage(0x90, setting)

    async def getRiceCookingReservationSettingTime(self):
        return await self.getMessage(0x91)

    async def setRiceCookingReservationSettingTime(self, time):
        return await self.setMessage(0x91, time)

    async def getRiceCookingReservationSettingRelativeTime(self):
        return await self.getMessage(0x92)

    async def setRiceCookingReservationSettingRelativeTime(self, time):
        return await self.setMessage(0x92, time)
