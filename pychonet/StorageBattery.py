from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DICT_41_PERMITTED_PROHIBITED,
    _int,
    _signed_int,
)


def _max_min_int(edt):
    """Parse minimum/maximum values from 8-byte EPC data."""
    max_val = str(int.from_bytes(edt[0:4], "big"))
    min_val = str(int.from_bytes(edt[4:8], "big"))
    return f"{max_val}/{min_val}"


def _max_min_short_int(edt):
    """Parse minimum/maximum values from 4-byte EPC data."""
    max_val = str(int.from_bytes(edt[0:2], "big"))
    min_val = str(int.from_bytes(edt[2:4], "big"))
    return f"{max_val}/{min_val}"


class StorageBattery(EchonetInstance):
    DICT_OPERATION_MODE = {
        0x41: "rapidCharging",
        0x42: "charging",
        0x43: "discharging",
        0x44: "standby",
        0x45: "test",
        0x46: "auto",
        0x48: "restart",
        0x49: "capacityRecalculation",
        0x40: "Other",
    }
    EPC_FUNCTIONS = {
        # Properties marked as DEL in MCRules - not available on this device
        # 0x83: _to_string,  # Identification number
        # 0x97: _hh_mm,  # Current time setting
        # 0x98: _yyyy_mm_dd,  # Current date setting
        0xA0: _int,  # AC effective capacity (charging)
        0xA1: _int,  # AC effective capacity (discharging)
        0xA2: _int,  # AC chargeable capacity
        0xA3: _int,  # AC dischargeable capacity
        0xA4: _int,  # AC chargeable electric energy
        0xA5: _int,  # AC dischargeable electric energy
        0xA6: _int,  # AC charge upper limit setting
        0xA7: _int,  # AC discharge lower limit setting
        0xA8: _int,  # AC measured cumulative charging electric energy
        0xA9: _int,  # AC measured cumulative discharging electric energy
        0xAA: _int,  # AC charge amount setting value
        0xAB: _int,  # AC discharge amount setting value
        0xC1: [
            _int,
            {
                0x00: "other",
                0x01: "maximum",
                0x02: "surplus",
                0x03: "designatedPower",
                0x04: "designatedCurrent",
            },
        ],  # Charging method
        0xC2: [
            _int,
            {
                0x00: "other",
                0x01: "maximum",
                0x02: "loadFollowing",
                0x03: "designatedPower",
                0x04: "designatedCurrent",
            },
        ],  # Discharging method
        0xC7: _int,  # AC rated electric energy
        0xC8: _max_min_int,  # Minimum/maximum charging electric power
        0xC9: _max_min_int,  # Minimum/maximum discharging electric power
        0xCA: _max_min_short_int,  # Minimum/maximum charging current
        0xCB: _max_min_short_int,  # Minimum/maximum discharging current
        0xCC: [
            _int,
            DICT_41_PERMITTED_PROHIBITED,
        ],  # Re-interconnection permission setting
        0xCD: [
            _int,
            DICT_41_PERMITTED_PROHIBITED,
        ],  # Operation permission setting
        0xCE: [
            _int,
            DICT_41_PERMITTED_PROHIBITED,
        ],  # Independent operation permission setting
        0xCF: [_int, DICT_OPERATION_MODE],  # Working operation status
        0xD0: _int,  # Rated electric energy
        0xD1: _int,  # Rated capacity
        0xD2: _int,  # Rated voltage
        0xD3: _signed_int,  # Measured instantaneous charging/discharging electric energy
        0xD4: _signed_int,  # Measured instantaneous charging/discharging current
        0xD5: _signed_int,  # Measured instantaneous charging/discharging voltage
        0xD6: _int,  # Measured cumulative discharging electric energy
        # Set-only property: Reset measured cumulative discharging electric energy (EPC=0xD7)
        0xD8: _int,  # Measured cumulative charging electric energy
        # Set-only property: Reset measured cumulative charging electric energy (EPC=0xD9)
        0xDA: [_int, DICT_OPERATION_MODE],  # Operation mode setting
        0xDB: [
            _int,
            {
                0x00: "reversePowerFlowAcceptable",
                0x01: "independent",
                0x02: "reversePowerFlowNotAcceptable",
            },
        ],  # System-interconnected type
        0xDC: _max_min_int,  # Minimum/maximum charging power (Independent)
        0xDD: _max_min_int,  # Minimum/maximum discharging power (Independent)
        0xDE: _max_min_short_int,  # Minimum/maximum charging current (Independent)
        0xDF: _max_min_short_int,  # Minimum/maximum discharging current (Independent)
        0xE0: _signed_int,  # Charging/discharging amount setting 1
        0xE1: _signed_int,  # Charging/discharging amount setting 2
        0xE2: _int,  # Remaining stored electricity 1
        0xE3: _int,  # Remaining stored electricity 2
        0xE4: _int,  # Remaining stored electricity 3
        0xE5: _int,  # Battery state of health
        0xE6: [
            _int,
            {
                0x00: "unknown",
                0x01: "lead",
                0x02: "ni_mh",
                0x03: "ni_cd",
                0x04: "lithiumIon",
                0x05: "zinc",
                0x06: "alkaline",
            },
        ],  # Battery type - per ECHONET spec, 0x04 = lithium ion
        0xE7: _int,  # Charging amount setting 1
        0xE8: _int,  # Discharging amount setting 1
        0xE9: _int,  # Charging amount setting 2
        0xEA: _int,  # Discharging amount setting 2
        0xEB: _int,  # Charging electric energy setting
        0xEC: _int,  # Discharging electric energy setting
        0xED: _int,  # Charging current setting
        0xEE: _int,  # Discharging current setting
        0xEF: _int,  # Rated voltage (Independent)
    }

    async def getOperationStatus(self):
        """Get operation status (ON=0x30, OFF=0x31)."""
        return await self.getMessage(0x80)

    async def setOperationStatus(self, value):
        """Set operation status (ON=0x30, OFF=0x31)."""
        return await self.setMessage(0x80, value)

    async def getIdentificationNumber(self):
        """Get identification number (EPC=0x83)."""
        return await self.getMessage(0x83)

    async def getFaultDescription(self):
        """Get fault description (EPC=0x89)."""
        return await self.getMessage(0x89)

    async def getProductCode(self):
        """Get product code (EPC=0x8C)."""
        return await self.getMessage(0x8C)

    async def getCurrentTimeSetting(self):
        """Get current time setting HH:MM (EPC=0x97)."""
        return await self.getMessage(0x97)

    async def setCurrentTimeSetting(self, value):
        """Set current time setting HH:MM (EPC=0x97)."""
        return await self.setMessage(0x97, value)

    async def getCurrentDateSetting(self):
        """Get current date setting YYYY:MM:DD (EPC=0x98)."""
        return await self.getMessage(0x98)

    async def setCurrentDateSetting(self, value):
        """Set current date setting YYYY:MM:DD (EPC=0x98)."""
        return await self.setMessage(0x98, value)

    async def getAcEffectiveChargingCapacity(self):
        """Get AC effective capacity for charging in Wh (EPC=0xA0)."""
        return await self.getMessage(0xA0)

    async def getAcEffectiveDischargingCapacity(self):
        """Get AC effective capacity for discharging in Wh (EPC=0xA1)."""
        return await self.getMessage(0xA1)

    async def getChargeableCapacity(self):
        """Get AC chargeable capacity in Wh (EPC=0xA2)."""
        return await self.getMessage(0xA2)

    async def setAcChargeUpperLimit(self, value):
        """Set AC charge upper limit percentage (EPC=0xA6)."""
        return await self.setMessage(0xA6, value)

    async def getChargeableElectricEnergy(self):
        """Get AC chargeable electric energy at present in Wh (EPC=0xA4)."""
        return await self.getMessage(0xA4)

    async def getDischargeableCapacity(self):
        """Get AC dischargeable capacity in Wh (EPC=0xA3)."""
        return await self.getMessage(0xA3)

    async def setDischargeableCapacity(self, value):
        """Set AC discharge amount target value in Wh (EPC=0xAB)."""
        return await self.setMessage(0xAB, value)

    async def getDischargeableElectricEnergy(self):
        """Get AC dischargeable electric energy at present in Wh (EPC=0xA5)."""
        return await self.getMessage(0xA5)

    async def setAcChargeUpperLimitSetting(self, value):
        """Set AC charge upper limit setting percentage (EPC=0xA6)."""
        return await self.setMessage(0xA6, value)

    async def setAcDischargeLowerLimitSetting(self, value):
        """Set AC discharge lower limit setting percentage (EPC=0xA7)."""
        return await self.setMessage(0xA7, value)

    async def getAcChargeUpperLimitSetting(self):
        """Get AC charge upper limit setting percentage (EPC=0xA6)."""
        return await self.getMessage(0xA6)

    async def getAcDischargeLowerLimitSetting(self):
        """Get AC discharge lower limit setting percentage (EPC=0xA7)."""
        return await self.getMessage(0xA7)

    async def getAcCumulativeChargingElectricEnergy(self):
        """Get AC measured cumulative charging electric energy in 0.001kWh (EPC=0xA8)."""
        return await self.getMessage(0xA8)

    async def getAcCumulativeDischargingElectricEnergy(self):
        """Get AC measured cumulative discharging electric energy in 0.001kWh (EPC=0xA9)."""
        return await self.getMessage(0xA9)

    async def setTargetChargingElectricEnergy(self, value):
        """Set AC charge amount target value in Wh (EPC=0xAA)."""
        return await self.setMessage(0xAA, value)

    async def setTargetDischargingElectricEnergy(self, value):
        """Set AC discharge amount target value in Wh (EPC=0xAB)."""
        return await self.setMessage(0xAB, value)

    async def getAcChargeAmountSettingValue(self):
        """Get AC charge amount setting value in Wh (EPC=0xAA)."""
        return await self.getMessage(0xAA)

    async def getAcDischargeAmountSettingValue(self):
        """Get AC discharge amount setting value in Wh (EPC=0xAB)."""
        return await self.getMessage(0xAB)

    # EPC=0xC1: Charging method (optional get)
    async def getChargingMethod(self):
        """Get charging method (maximum/surplus/designatedPower/designatedCurrent/other) (EPC=0xC1)."""
        return await self.getMessage(0xC1)

    # EPC=0xC2: Discharging method (optional get)
    async def getDischargingMethod(self):
        """Get discharging method (maximum/loadFollowing/designatedPower/designatedCurrent/other) (EPC=0xC2)."""
        return await self.getMessage(0xC2)

    # EPC=0xC7: AC rated electric energy (optional get)
    async def getAcRatedElectricEnergy(self):
        """Get AC rated electric energy in Wh (EPC=0xC7)."""
        return await self.getMessage(0xC7)

    # EPC=0xC8: Minimum/maximum charging electric power (required from H+)
    async def getMinimumAndMaximumChargingElectricPower(self):
        """Get minimum/maximum charging electric power in W AC (EPC=0xC8)."""
        return await self.getMessage(0xC8)

    # EPC=0xC9: Minimum/maximum discharging electric power (required from H+)
    async def getMinimumAndMaximumDischargingElectricPower(self):
        """Get minimum/maximum discharging electric power in W AC (EPC=0xC9)."""
        return await self.getMessage(0xC9)

    # EPC=0xCA: Minimum/maximum charging current (optional get)
    async def getMinimumAndMaximumChargingCurrent(self):
        """Get minimum/maximum charging current in 0.1A AC (EPC=0xCA)."""
        return await self.getMessage(0xCA)

    #  EPC=0xCB: Minimum/maximum discharging current (optional get)
    async def getMinimumAndMaximumDischargingCurrent(self):
        """Get minimum/maximum discharging current in 0.1A AC (EPC=0xCB)."""
        return await self.getMessage(0xCB)

    # EPC=0xCF: Working operation status (required)
    async def getActualOperationMode(self):
        """Get actual working operation status (rapidCharging/charging/discharging/standby/test/auto/restart/capacityRecalculation/other) (EPC=0xCF)."""
        return await self.getMessage(0xCF)

    # EPC=0xD0: Rated electric energy (optional get)
    async def getRatedElectricEnergy(self):
        """Get rated electric energy in Wh DC (EPC=0xD0)."""
        return await self.getMessage(0xD0)

    # EPC=0xD1: Rated capacity (optional get)
    async def getRatedCapacity(self):
        """Get rated charging capacity in 0.1Ah DC (EPC=0xD1)."""
        return await self.getMessage(0xD1)

    # EPC=0xD2: Rated voltage (optional get)
    async def getRatedVoltage(self):
        """Get rated voltage in V DC (EPC=0xD2)."""
        return await self.getMessage(0xD2)

    # EPC=0xD3: Measured instantaneous charging/discharging electric energy (optional get)
    async def getInstantaneousChargingAndDischargingElectricPower(self):
        """Get measured instantaneous charging/discharging electric power in W AC (positive/negative) (EPC=0xD3)."""
        return await self.getMessage(0xD3)

    # EPC=0xD4: Measured instantaneous charging/discharging current (optional get)
    async def getInstantaneousChargingAndDischargingCurrent(self):
        """Get measured instantaneous charging/discharging current in 0.1A AC (positive/negative) (EPC=0xD4)."""
        return await self.getMessage(0xD4)

    # EPC=0xD5: Measured instantaneous charging/discharging voltage (optional get)
    async def getInstantaneousChargingAndDischargingVoltage(self):
        """Get measured instantaneous charging/discharging voltage in V AC (positive/negative) (EPC=0xD5)."""
        return await self.getMessage(0xD5)

    # EPC=0xD6: Measured cumulative discharging electric energy (optional get)
    async def getCumulativeDischargingElectricEnergy(self):
        """Get measured cumulative discharging electric energy in 0.001kWh (EPC=0xD6)."""
        return await self.getMessage(0xD6)

    # EPC=0xD8: Measured cumulative charging electric energy (optional get)
    async def getCumulativeChargingElectricEnergy(self):
        """Get measured cumulative charging electric energy in 0.001kWh (EPC=0xD8)."""
        return await self.getMessage(0xD8)

    # EPC=0xDB: System-interconnected type (required from H+)
    async def getPowerSystemInterconnectionStatus(self):
        """Get system-interconnection status (reversePowerFlowAcceptable/independent/reversePowerFlowNotAcceptable) (EPC=0xDB)."""
        return await self.getMessage(0xDB)

    # EPC=0xDC: Minimum/maximum charging power at Independent (optional get)
    async def getMinimumAndMaximumChargingPowerAtIndependent(self):
        """Get minimum/maximum charging power in W AC during independent operation (EPC=0xDC)."""
        return await self.getMessage(0xDC)

    # EPC=0xDD: Minimum/maximum discharging power at Independent (optional get)
    async def getMinimumAndMaximumDischargingPowerAtIndependent(self):
        """Get minimum/maximum discharging power in W AC during independent operation (EPC=0xDD)."""
        return await self.getMessage(0xDD)

    # EPC=0xDE: Minimum/maximum charging current at Independent (optional get)
    async def getMinimumAndMaximumChargingCurrentAtIndependent(self):
        """Get minimum/maximum charging current in 0.1A AC during independent operation (EPC=0xDE)."""
        return await self.getMessage(0xDE)

    # EPC=0xDF: Minimum/maximum discharging current at Independent (optional get)
    async def getMinimumAndMaximumDischargingCurrentAtIndependent(self):
        """Get minimum/maximum discharging current in 0.1A AC during independent operation (EPC=0xDF)."""
        return await self.getMessage(0xDF)

    # EPC=0xE2: Remaining stored electricity 1 (required_c get)
    async def getRemainingCapacity1(self):
        """Get remaining stored electric energy in Wh DC (EPC=0xE2)."""
        return await self.getMessage(0xE2)

    # EPC=0xE3: Remaining stored electricity 2 (required_c get)
    async def getRemainingCapacity2(self):
        """Get remaining capacity in 0.1Ah DC (EPC=0xE3)."""
        return await self.getMessage(0xE3)

    # EPC=0xE4: Remaining stored electricity 3 (required_c get)
    async def getRemainingCapacity3(self):
        """Get charging rate of battery in % (EPC=0xE4)."""
        return await self.getMessage(0xE4)

    # EPC=0xE5: Battery state of health (optional get)
    async def getBatteryHealthState(self):
        """Get battery state of health in % (EPC=0xE5)."""
        return await self.getMessage(0xE5)

    # EPC=0xEF: Rated voltage at Independent (optional get)
    async def getRatedVoltageAtIndependent(self):
        """Get rated voltage in V AC during independent operation (EPC=0xEF)."""
        return await self.getMessage(0xEF)

    async def getOperationMode(self):
        """Get working operation status (charging=0x42, discharging=0x43, etc.)."""
        return await self.getMessage(0xCF)

    async def setOperationMode(self, value):
        """Set operation mode setting."""
        return await self.setMessage(0xDA, value)

    async def getBatteryType(self):
        """Get battery type (lithiumIon=0x04, lead=0x01, etc.)."""
        return await self.getMessage(0xE6)

    # Reset cumulative discharging electric energy (EPC=0xD7 - Set only)
    async def resetCumulativeDischargingElectricEnergy(self):
        """Reset measured cumulative discharging electric energy to zero (EPC=0xD7)."""
        return await self.setMessage(0xD7, 0x00)

    # Reset cumulative charging electric energy (EPC=0xD9 - Set only)
    async def resetCumulativeChargingElectricEnergy(self):
        """Reset measured cumulative charging electric energy to zero (EPC=0xD9)."""
        return await self.setMessage(0xD9, 0x00)

    # EPC=0xE0: Charging/discharging amount setting 1 (optional get/set)
    async def setChargingAndDischargingAmount1(self, value):
        """Set charging/discharging amount in Wh DC positive/negative (EPC=0xE0)."""
        return await self.setMessage(0xE0, value)

    # EPC=0xE1: Charging/discharging amount setting 2 (optional get/set)
    async def setChargingAndDischargingAmount2(self, value):
        """Set charging/discharging amount in 0.1Ah DC positive/negative (EPC=0xE1)."""
        return await self.setMessage(0xE1, value)

    # EPC=0xE7: Charging amount setting 1 (optional get/set)
    async def setChargingAmount1(self, value):
        """Set charging amount in Wh DC (EPC=0xE7)."""
        return await self.setMessage(0xE7, value)

    # EPC=0xE8: Discharging amount setting 1 (optional get/set)
    async def setDischargingAmount1(self, value):
        """Set discharging amount in Wh DC (EPC=0xE8)."""
        return await self.setMessage(0xE8, value)

    # EPC=0xE9: Charging amount setting 2 (optional get/set)
    async def setChargingAmount2(self, value):
        """Set charging capacity in 0.1Ah DC (EPC=0xE9)."""
        return await self.setMessage(0xE9, value)

    # EPC=0xEA: Discharging amount setting 2 (optional get/set)
    async def setDischargingAmount2(self, value):
        """Set discharging capacity in 0.1Ah DC (EPC=0xEA)."""
        return await self.setMessage(0xEA, value)

    # EPC=0xEB: Charging electric power setting (optional get/set)
    async def setChargingPowerSetting(self, value):
        """Set charging electric power in W AC (EPC=0xEB)."""
        return await self.setMessage(0xEB, value)

    # EPC=0xEC: Discharging electric power setting (optional get/set)
    async def setDischargingPowerSetting(self, value):
        """Set discharging electric power in W AC (EPC=0xEC)."""
        return await self.setMessage(0xEC, value)

    # EPC=0xED: Charging current setting (optional get/set)
    async def setChargingCurrentSetting(self, value):
        """Set charging current in 0.1A AC (EPC=0xED)."""
        return await self.setMessage(0xED, value)

    # EPC=0xEE: Discharging current setting (optional get/set)
    async def setDischargingCurrentSetting(self, value):
        """Set discharging current in 0.1A AC (EPC=0xEE)."""
        return await self.setMessage(0xEE, value)

    # EPC=0xCC: Re-interconnection permission setting (optional get/set)
    async def setReInterconnectionPermission(self, value):
        """Set re-interconnection permission (permitted/prohibited) (EPC=0xCC)."""
        return await self.setMessage(0xCC, value)

    # EPC=0xCD: Operation permission setting (optional get/set)
    async def setOperationPermission(self, value):
        """Set operation permission (permitted/prohibited) (EPC=0xCD)."""
        return await self.setMessage(0xCD, value)

    # EPC=0xCE: Independent operation permission setting (optional get/set)
    async def setIndependentOperationPermission(self, value):
        """Set independent operation permission (permitted/prohibited) (EPC=0xCE)."""
        return await self.setMessage(0xCE, value)

    # WORKING_OPERATION_STATES = {
    #     0x40: "Other",
    #     0x41: "Rapid charging",
    #     0x42: "Charging",
    #     0x43: "Discharging",
    #     0x44: "Standby",
    #     0x45: "Test",
    #     0x46: "Automatic",
    #     0x48: "Restart",
    #     0x49: "Effective capacity recalculation processing",
    # }

    # def _permission_setting(edt):
    #     op_mode = int.from_bytes(edt, "big")
    #     values = {
    #         0x41: "permitted",
    #         0x42: "Prohibited",
    #     }
    #     return values.get(op_mode, "Invalid setting")

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x7D
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
