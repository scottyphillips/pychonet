# pychonet/ElectricVehicleCharger.py
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _unsigned_long, _unsigned_short, _signed_long, DICT_30_ON_OFF


class ElectricVehicleCharger(EchonetInstance):
    EPC_FUNCTIONS = {
        # Electric vehicle charger class
        0x80: [_int, DICT_30_ON_OFF],  # Operation status
        0xC5: [_unsigned_long],  # Rated charge capacity
        0xC7: [_int, {0x30: "Vehicle not connected", 0x40: "Connected to vehicle, Not chargeable", 0x41: "Connected to vehicle, Chargeable", 0x44: "Connected to vehicle, chargeable status unknown", 0xFF: "Undetermined"}],  # Vehicle connection and chargeable status
        0xC8: [_unsigned_long],  # Minimum/maximum charging electric power
        0xCA: [_unsigned_short],  # Minimum/maximum charging current
        0xCC: [_int, {0x10: "AC_No_Communication", 0x11: "AC_CPLT", 0x12: "AC_HLC (charging only)", 0x21: "DC_type AA (charging only)", 0x31: "DC_type BB (charging only)", 0x41: "DC_type EE (charging only)", 0x51: "DC_type FF (charging only)"}],  # Charger type
        0xCD: [_int, {0x10: "Connection confirmation"}],  # Vehicle connection confirmation
        0xCE: [_unsigned_long],  # Chargeable capacity of vehicle mounted battery
        0xCF: [_unsigned_long],  # Remaining chargeable capacity of vehicle mounted battery
        0xD0: [_unsigned_long],  # Used capacity of vehicle-mounted battery
        0xD2: [_unsigned_short],  # Rated voltage
        0xD3: [_signed_long],  # Measured instantaneous charging electric power
        0xD8: [_unsigned_long],  # Measured cumulative amount of charging electric energy
        0xD9: [_int, {0x00: "Reset"}],  # Cumulative amount of charging electric energy reset setting
        0xDA: [_int, {0x40: "Other", 0x42: "Charging", 0x44: "Standby", 0x47: "Idle"}],  # Operating mode setting
        0xE2: [_unsigned_long],  # Remaining stored electricity of vehicle-mounted battery
        0xE4: [_int],  # Remaining stored electricity of vehicle-mounted battery
        0xE6: [_int],  # Vehicle ID
        0xE7: [_unsigned_long],  # Charging amount setting
        0xEB: [_unsigned_long],  # Charging electric power setting
        0xED: [_unsigned_short],  # Charging current setting
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0xA1
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        return await self.setMessage(0x80, status)

    async def getRatedChargeCapacity(self):
        return await self.getMessage(0xC5)

    async def getVehicleConnectionAndChargeableStatus(self):
        return await self.getMessage(0xC7)

    async def getMinimumMaximumChargingElectricPower(self):
        return await self.getMessage(0xC8)

    async def getMinimumMaximumChargingCurrent(self):
        return await self.getMessage(0xCA)

    async def getChargerType(self):
        return await self.getMessage(0xCC)

    async def getVehicleConnectionConfirmation(self):
        return await self.getMessage(0xCD)

    async def getChargeableCapacityOfVehicleMountedBattery(self):
        return await self.getMessage(0xCE)

    async def getRemainingChargeableCapacityOfVehicleMountedBattery(self):
        return await self.getMessage(0xCF)

    async def getUsedCapacityOfVehicleMountedBattery(self):
        return await self.getMessage(0xD0)

    async def getRatedVoltage(self):
        return await self.getMessage(0xD2)

    async def getMeasuredInstantaneousChargingElectricPower(self):
        return await self.getMessage(0xD3)

    async def getMeasuredCumulativeAmountOfChargingElectricEnergy(self):
        return await self.getMessage(0xD8)

    async def setCumulativeAmountOfChargingElectricEnergy(self):
        return await self.setMessage(0xD9, 0x00)

    async def getOperatingModeSetting(self):
        return await self.getMessage(0xDA)

    async def setOperatingModeSetting(self, mode):
        return await self.setMessage(0xDA, mode)

    async def getRemainingStoredElectricityOfVehicleMountedBattery1(self):
        return await self.getMessage(0xE2)

    async def getRemainingStoredElectricityOfVehicleMountedBattery3(self):
        return await self.getMessage(0xE4)

    async def getVehicleID(self):
        return await self.getMessage(0xE6)

    async def getChargingAmountSetting(self):
        return await self.getMessage(0xE7)

    async def setChargingAmountSetting(self, amount):
        return await self.setMessage(0xE7, amount)

    async def getChargingElectricPowerSetting(self):
        return await self.getMessage(0xEB)

    async def setChargingElectricPowerSetting(self, power):
        return await self.setMessage(0xEB, power)

    async def getChargingCurrentSetting(self):
        return await self.getMessage(0xED)

    async def setChargingCurrentSetting(self, current):
        return await self.setMessage(0xED, current)