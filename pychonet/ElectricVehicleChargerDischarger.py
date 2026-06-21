# pychonet/ElectricVehicleChargerDischarger.py
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _unsigned_long, _unsigned_short, _signed_long, _signed_int, DICT_30_ON_OFF, _yyyy_mm_dd


class ElectricVehicleChargerDischarger(EchonetInstance):
    EPC_FUNCTIONS = {
        # Electric vehicle charger/discharger class (V2G)
        # Note: EPC super functions (0x80, 0x83-0x85, 0x88-0x8A, 0x8C, 0x97, 0x9A, 0x9D-0x9F) 
        # are handled automatically by EchonetInstance via EPC_SUPER_FUNCTIONS
        0x81: [None],  # Installation location
        0x82: [None],  # Standard version information
        0x86: [None],  # Manufacturer's fault code
        0x87: [_int],  # Current limit setting (0-100%)
        0x8B: [None],  # Business facility code (3 bytes)
        0x8D: [None],  # Production number (ASCII)
        0x8E: [None],  # Production date (4 bytes)
        0x8F: [_int, {0x41: "Power saving Operation", 0x42: "Normal Operation"}],  # Power-saving operation setting
        0x93: [None],  # Remote control setting (raw_16)
        0x98: [_yyyy_mm_dd],  # Current date setting (YYYY:MM:DD format)
        0x99: [_unsigned_short],  # Power limit setting (W)
        # Discharge capacity properties
        0xC0: [_unsigned_long],  # Dischargeable capacity of vehicle mounted battery 1 (Wh)
        0xC1: [_unsigned_short],  # Dischargeable capacity of vehicle mounted battery 2 (0.1Ah)
        0xC2: [_unsigned_long],  # Remaining dischargeable capacity of vehicle mounted battery 1 (Wh)
        0xC3: [_unsigned_short],  # Remaining dischargeable capacity of vehicle mounted battery 2 (0.1Ah)
        0xC4: [_int],  # Remaining dischargeable capacity of vehicle mounted battery 3 (%)
        # Charge capacity properties
        0xC5: [_unsigned_long],  # Rated charge capacity (W)
        0xC6: [_unsigned_long],  # Rated discharge capacity (W)
        # Vehicle connection and charge/discharge status
        0xC7: [_int, {
            0x30: "Not Connected",
            0x40: "Connected",
            0x41: "Chargeable",
            0x42: "Dischargeable",
            0x43: "Chargeable and Dischargeable"
        }],  # Vehicle connection and chargeable/dischargeable status
        # Charging limits
        0xC8: [_unsigned_long],  # Minimum/maximum charging electric energy (W)
        0xC9: [_unsigned_long],  # Minimum/maximum discharging electric energy (W)
        0xCA: [_unsigned_short],  # Minimum/maximum charging current (0.1A)
        0xCB: [_unsigned_short],  # Minimum/maximum discharging current (0.1A)
        # Charger/Discharger type
        0xCC: [_int, {
            0x11: "AC_CPLT",
            0x12: "AC_HLC_Charge",
            0x13: "AC_HLC_ChargeDischarge",
            0x21: "DC_AA_Charge",
            0x22: "DC_AA_ChargeDischarge",
            0x23: "DC_AA_Discharge",
            0x31: "DC_BB_Charge",
            0x32: "DC_BB_ChargeDischarge",
            0x33: "DC_BB_Discharge",
            0x41: "DC_EE_Charge",
            0x42: "DC_EE_ChargeDischarge",
            0x43: "DC_EE_Discharge",
            0x51: "DC_FF_Charge",
            0x52: "DC_FF_ChargeDischarge",
            0x53: "DC_FF_Discharge"
        }],  # Charger/Discharger type
        0xCD: [_int, {0x10: "Connection confirmation"}],  # Vehicle connection confirmation (set only)
        # Battery capacity properties
        0xCE: [_unsigned_long],  # Chargeable capacity of vehicle mounted battery (Wh)
        0xCF: [_unsigned_long],  # Remaining chargeable capacity of vehicle mounted battery (Wh)
        0xD0: [_unsigned_long],  # Used capacity of vehicle mounted battery 1 (Wh)
        0xD1: [_unsigned_short],  # Used capacity of vehicle mounted battery 2 (0.1Ah)
        0xD2: [_unsigned_short],  # Rated voltage (V)
        # Instantaneous measurements (signed for bidirectional)
        0xD3: [_signed_long],  # Measured instantaneous charging/discharging electric energy (±W)
        0xD4: [_signed_int],  # Measured instantaneous charging/discharging current (±0.1A)
        0xD5: [_signed_int],  # Measured instantaneous charging/discharging voltage (±V)
        # Discharge cumulative energy
        0xD6: [_unsigned_long],  # Measured cumulative amount of discharging electric energy (0.001kWh)
        0xD7: [_int, {0x0: "Reset"}],  # Cumulative amount of discharging electric energy reset setting (set only)
        0xD8: [_unsigned_long],  # Measured cumulative amount of charging electric energy (0.001kWh)
        0xD9: [_int, {0x0: "Reset"}],  # Cumulative amount of charging electric energy reset setting (set only)
        # Operation mode
        0xDA: [_int, {
            0x40: "Other",
            0x41: "Rapid charge",
            0x42: "Charge",
            0x43: "Discharge",
            0x44: "Standby",
            0x45: "Test"
        }],  # Operation mode setting
        0xDB: [_int, {
            0x0: "Grid connection (reverse flow acceptable)",
            0x1: "Independent operation",
            0x2: "Grid connection (reverse flow not acceptable)"
        }],  # System interconnected type
        0xDC: [_int, {
            0x0: "Others",
            0x1: "Maximum charging electric power charging",
            0x2: "Surplus electric power charging",
            0x3: "Designated electric power charging",
            0x4: "Designated electric current charging",
            0x5: "Designated purchasing electric power charging"
        }],  # Charging method
        0xDD: [_int, {
            0x0: "Others",
            0x1: "Maximum discharging electric power discharging",
            0x2: "Load-following discharging",
            0x3: "Designated electric power discharging",
            0x4: "Designated electric current discharging",
            0x5: "Designated purchasing electric power discharging"
        }],  # Discharging method
        0xDE: [_unsigned_long],  # Purchasing electric power setting (W)
        0xDF: [_int, {0x41: "Permitted", 0x42: "Prohibited"}],  # Re-interconnection permission setting
        0xE0: [_signed_long],  # Charging/Discharging electric power setting (±W)
        0xE1: [_int, {
            0x40: "Other",
            0x42: "Charge",
            0x43: "Discharge",
            0x44: "Standby",
            0x47: "Idle",
            0x48: "Preparation"
        }],  # Actual operation mode
        # Remaining stored electricity
        0xE2: [_unsigned_long],  # Remaining stored electricity of vehicle mounted battery1 (Wh)
        0xE3: [_unsigned_short],  # Remaining stored electricity of vehicle mounted battery2 (0.1Ah)
        0xE4: [_int],  # Remaining stored electricity of vehicle mounted battery3 (%)
        0xE5: [_int, {0x41: "Occurrence status found", 0x42: "Occurrence status not found"}],  # Maintenance status
        0xE6: [_int],  # Vehicle ID
        0xE7: [_unsigned_long],  # Charging amount setting 1 (Wh)
        0xE9: [_unsigned_short],  # Charging amount setting 2 (0.1Ah)
        0xEA: [_unsigned_long],  # Discharging electric energy setting (Wh)
        0xEB: [_unsigned_long],  # Charging electric energy setting (W)
        0xEC: [_unsigned_long],  # Discharging electric energy setting (W)
        0xED: [_unsigned_short],  # Charging current setting (0.1A)
        0xEE: [_unsigned_short],  # Discharging current setting (0.1A)
        0xEF: [_unsigned_short],  # Rated voltage (Independent) (V)
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x7E
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    # Standard properties
    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        return await self.setMessage(0x80, status)

    async def getInstallationLocation(self):
        return await self.getMessage(0x81)

    async def setInstallationLocation(self, location):
        return await self.setMessage(0x81, location)

    async def getStandardVersionInformation(self):
        return await self.getMessage(0x82)

    async def getIdentificationNumber(self):
        return await self.getMessage(0x83)

    async def getMeasuredInstantaneousPowerConsumption(self):
        return await self.getMessage(0x84)

    async def getMeasuredCumulativeElectricEnergyConsumption(self):
        return await self.getMessage(0x85)

    async def getManufacturersFaultCode(self):
        return await self.getMessage(0x86)

    async def getCurrentLimitSetting(self):
        return await self.getMessage(0x87)

    async def setCurrentLimitSetting(self, limit):
        return await self.setMessage(0x87, limit)

    async def getFaultStatus(self):
        return await self.getMessage(0x88)

    async def getFaultDescription(self):
        return await self.getMessage(0x89)

    async def getManufacturerCode(self):
        return await self.getMessage(0x8A)

    async def getBusinessFacilityCode(self):
        return await self.getMessage(0x8B)

    async def getProductCode(self):
        return await self.getMessage(0x8C)

    async def getProductionNumber(self):
        return await self.getMessage(0x8D)

    async def getProductionDate(self):
        return await self.getMessage(0x8E)

    async def getPowerSavingOperationSetting(self):
        return await self.getMessage(0x8F)

    async def setPowerSavingOperationSetting(self, mode):
        return await self.setMessage(0x8F, mode)

    async def getRemoteControlSetting(self):
        return await self.getMessage(0x93)

    async def setRemoteControlSetting(self, setting):
        return await self.setMessage(0x93, setting)

    async def getCurrentTimeSetting(self):
        return await self.getMessage(0x97)

    async def setCurrentTimeSetting(self, time_val):
        return await self.setMessage(0x97, time_val)

    async def getCurrentDateSetting(self):
        return await self.getMessage(0x98)

    async def setCurrentDateSetting(self, date_val):
        return await self.setMessage(0x98, date_val)

    async def getPowerLimitSetting(self):
        return await self.getMessage(0x99)

    async def setPowerLimitSetting(self, power):
        return await self.setMessage(0x99, power)

    async def getCumulativeOperatingTime(self):
        return await self.getMessage(0x9A)

    async def getStatusChangeAnnouncementPropertyMap(self):
        return await self.getMessage(0x9D)

    async def getSetPropertyMap(self):
        return await self.getMessage(0x9E)

    async def getGetPropertyMap(self):
        return await self.getMessage(0x9F)

    # Discharge capacity properties
    async def getDischargeableCapacityOfVehicleMountedBattery1(self):
        return await self.getMessage(0xC0)

    async def getDischargeableCapacityOfVehicleMountedBattery2(self):
        return await self.getMessage(0xC1)

    async def getRemainingDischargeableCapacityOfVehicleMountedBattery1(self):
        return await self.getMessage(0xC2)

    async def getRemainingDischargeableCapacityOfVehicleMountedBattery2(self):
        return await self.getMessage(0xC3)

    async def getRemainingDischargeableCapacityOfVehicleMountedBattery3(self):
        return await self.getMessage(0xC4)

    # Charge capacity properties
    async def getRatedChargeCapacity(self):
        return await self.getMessage(0xC5)

    async def getRatedDischargeCapacity(self):
        return await self.getMessage(0xC6)

    async def getVehicleConnectionAndChargeableDischargeableStatus(self):
        return await self.getMessage(0xC7)

    # Charging/discharging limits
    async def getMinimumMaximumChargingElectricEnergy(self):
        return await self.getMessage(0xC8)

    async def getMinimumMaximumDischargingElectricEnergy(self):
        return await self.getMessage(0xC9)

    async def getMinimumMaximumChargingCurrent(self):
        return await self.getMessage(0xCA)

    async def getMinimumMaximumDischargingCurrent(self):
        return await self.getMessage(0xCB)

    async def getChargerDischargerType(self):
        return await self.getMessage(0xCC)

    async def setVehicleConnectionConfirmation(self, confirmation):
        return await self.setMessage(0xCD, confirmation)

    # Battery capacity properties
    async def getChargeableCapacityOfVehicleMountedBattery(self):
        return await self.getMessage(0xCE)

    async def getRemainingChargeableCapacityOfVehicleMountedBattery(self):
        return await self.getMessage(0xCF)

    async def getUsedCapacityOfVehicleMountedBattery1(self):
        return await self.getMessage(0xD0)

    async def getUsedCapacityOfVehicleMountedBattery2(self):
        return await self.getMessage(0xD1)

    async def getRatedVoltage(self):
        return await self.getMessage(0xD2)

    # Instantaneous measurements (bidirectional)
    async def getMeasuredInstantaneousChargingDischargingElectricEnergy(self):
        return await self.getMessage(0xD3)

    async def getMeasuredInstantaneousChargingDischargingCurrent(self):
        return await self.getMessage(0xD4)

    async def getMeasuredInstantaneousChargingDischargingVoltage(self):
        return await self.getMessage(0xD5)

    # Cumulative energy
    async def getMeasuredCumulativeAmountOfDischargingElectricEnergy(self):
        return await self.getMessage(0xD6)

    async def setCumulativeAmountOfDischargingElectricEnergyReset(self):
        return await self.setMessage(0xD7, 0x00)

    async def getMeasuredCumulativeAmountOfChargingElectricEnergy(self):
        return await self.getMessage(0xD8)

    async def setCumulativeAmountOfChargingElectricEnergyReset(self):
        return await self.setMessage(0xD9, 0x00)

    # Operation mode and control
    async def getOperationModeSetting(self):
        return await self.getMessage(0xDA)

    async def setOperationModeSetting(self, mode):
        return await self.setMessage(0xDA, mode)

    async def getSystemInterconnectedType(self):
        return await self.getMessage(0xDB)

    async def getChargingMethod(self):
        return await self.getMessage(0xDC)

    async def setChargingMethod(self, method):
        return await self.setMessage(0xDC, method)

    async def getDischargingMethod(self):
        return await self.getMessage(0xDD)

    async def setDischargingMethod(self, method):
        return await self.setMessage(0xDD, method)

    async def getPurchasingElectricPowerSetting(self):
        return await self.getMessage(0xDE)

    async def setPurchasingElectricPowerSetting(self, power):
        return await self.setMessage(0xDE, power)

    async def getReInterconnectionPermissionSetting(self):
        return await self.getMessage(0xDF)

    async def setReInterconnectionPermissionSetting(self, permission):
        return await self.setMessage(0xDF, permission)

    async def getChargingDischargingElectricPowerSetting(self):
        return await self.getMessage(0xE0)

    async def setChargingDischargingElectricPowerSetting(self, power):
        return await self.setMessage(0xE0, power)

    async def getActualOperationMode(self):
        return await self.getMessage(0xE1)

    # Remaining stored electricity
    async def getRemainingStoredElectricityOfVehicleMountedBattery1(self):
        return await self.getMessage(0xE2)

    async def getRemainingStoredElectricityOfVehicleMountedBattery2(self):
        return await self.getMessage(0xE3)

    async def getRemainingStoredElectricityOfVehicleMountedBattery3(self):
        return await self.getMessage(0xE4)

    async def getMaintenanceStatus(self):
        return await self.getMessage(0xE5)

    async def getVehicleID(self):
        return await self.getMessage(0xE6)

    # Charging settings
    async def getChargingAmountSetting1(self):
        return await self.getMessage(0xE7)

    async def setChargingAmountSetting1(self, amount):
        return await self.setMessage(0xE7, amount)

    async def getChargingAmountSetting2(self):
        return await self.getMessage(0xE9)

    async def setChargingAmountSetting2(self, amount):
        return await self.setMessage(0xE9, amount)

    async def getDischargingElectricEnergySetting1(self):
        return await self.getMessage(0xEA)

    async def setDischargingElectricEnergySetting1(self, energy):
        return await self.setMessage(0xEA, energy)

    async def getChargingElectricPowerSetting(self):
        return await self.getMessage(0xEB)

    async def setChargingElectricPowerSetting(self, power):
        return await self.setMessage(0xEB, power)

    async def getDischargingElectricPowerSetting(self):
        return await self.getMessage(0xEC)

    async def setDischargingElectricPowerSetting(self, power):
        return await self.setMessage(0xEC, power)

    async def getChargingCurrentSetting(self):
        return await self.getMessage(0xED)

    async def setChargingCurrentSetting(self, current):
        return await self.setMessage(0xED, current)

    async def getDischargingCurrentSetting(self):
        return await self.getMessage(0xEE)

    async def setDischargingCurrentSetting(self, current):
        return await self.setMessage(0xEE, current)

    async def getRatedVoltageOfIndependentOperation(self):
        return await self.getMessage(0xEF)