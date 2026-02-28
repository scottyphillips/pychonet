from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int


class ElectricThermos(EchonetInstance):
    EPC_FUNCTIONS = {
        0x80: [_int, {0x30: 'ON', 0x31: 'OFF'}],  # Operation status
        0xB0: [_int, {0x41: 'Cover open', 0x42: 'Cover closed'}],  # Cover open/close status
        0xB1: [_int, {0x41: 'No-water condition found', 0x40: 'No-water condition not found'}],  # No-water warning
        0xB2: [_int, {0x41: 'Boil-up start', 0x42: 'Boil-up stop/warmer'}],  # Boil-up setting
        0xE0: [_int, {0x41: 'Citric acid cleaning', 0x42: 'Normal warmer', 0x43: 'Power-saving warmer'}],  # Boil-up/warmer mode setting
        0xE1: [_int, lambda x: 0x00 <= x <= 0x64],  # Set value of warmer temperature (0-100°C)
        0xE2: [_int, {0x41: 'Hot water discharged', 0x42: 'Hot water not discharged'}],  # Hot water discharge status
        0xE3: [_int, {0x41: 'Locked', 0x42: 'Unlocked'}],  # Lock status
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x03  # Cooking/housework-related device group
        self._eojcc = 0xB2  # Electric hot water pot (Electric thermos) class
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        return await self.setMessage(0x80, status)

    async def getCoverStatus(self):
        return await self.getMessage(0xB0)

    async def getNoWaterWarning(self):
        return await self.getMessage(0xB1)

    async def getBoilUpSetting(self):
        return await self.getMessage(0xB2)

    async def setBoilUpSetting(self, setting):
        return await self.setMessage(0xB2, setting)

    async def getBoilUpMode(self):
        return await self.getMessage(0xE0)

    async def setBoilUpMode(self, mode):
        return await self.setMessage(0xE0, mode)

    async def getWarmerTemperature(self):
        return await self.getMessage(0xE1)

    async def setWarmerTemperature(self, temperature):
        return await self.setMessage(0xE1, temperature)

    async def getHotWaterDischargeStatus(self):
        return await self.getMessage(0xE2)

    async def getLockStatus(self):
        return await self.getMessage(0xE3)

