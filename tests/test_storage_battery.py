"""Unit tests for StorageBattery ECHONET device class."""
import unittest
from pychonet.StorageBattery import StorageBattery


class MockECHONETAPIClient:
    """Mock API client for testing StorageBattery functionality.

    Uses EOJX codes: group=0x02, class=0x7D (Storage Battery)
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    def __init__(self):
        self._state = {
            "192.168.1.50": {
                "instances": {
                    0x02: {  # EoJGC (Class Group Code) for Storage Battery
                        0x7D: {  # EoJCC (Class Code) for Storage Battery
                            0x01: {  # Instance code
                                # Basic properties - tested in existing tests
                                0x80: b"\x30",           # Operation status: on
                                0xA2: b"\x00\x0A\xF5",   # AC chargeable capacity (2550 Wh)
                                0xA3: b"\x00\x0B\xC4",   # AC dischargeable capacity (3012 Wh)
                                0xC7: b"\x00\x00\xC8",   # AC rated electric energy (300 Wh)
                                0xCF: b"\x42",           # Working operation status: charging
                                0xD0: b"\x00\x0C\x35",   # Rated electric energy (3125 Wh)
                                0xD1: b"\x00\x64",       # Rated capacity (100 * 0.1Ah = 10Ah)
                                0xE5: b"\x78",           # Battery state of health: 90%
                                0xE6: b"\x04",           # Battery type: Lithium ion

                                # Additional properties for testing
                                0xA0: b"\x00\x01\x00",    # AC effective capacity (charging) - 256 Wh
                                0xA1: b"\x00\x01\xF4",    # AC effective capacity (discharging) - 500 Wh
                                0xA4: b"\x00\x0A\xF5",    # AC chargeable electric energy (2550 Wh)
                                0xA5: b"\x00\x0B\xC4",    # AC dischargeable electric energy (3012 Wh)
                                0xA6: b"\x64",           # AC charge upper limit setting - 100%
                                0xA7: b"\x0A",           # AC discharge lower limit setting - 10%
                                0xA8: b"\x00\x00\x01",    # AC cumulative charging electric energy (1 Wh)
                                0xA9: b"\x00\x00\x02",    # AC cumulative discharging electric energy (2 Wh)
                                0xAA: b"\x00\x0A\xF5",    # AC charge amount setting value (2550 Wh)
                                0xAB: b"\x00\x0B\xC4",    # AC discharge amount setting value (3012 Wh)
                                0xC1: b"\x01",           # Charging method - maximum
                                0xC2: b"\x01",           # Discharging method - maximum
                                0xC8: b"\x00\x64\x00\xC8", # Min/max charging power (300/200 W)
                                0xC9: b"\x00\x64\x00\xC8", # Min/max discharging power (300/200 W)
                                0xCA: b"\x0A\x00\x1F\x40", # Min/max charging current (1000.0/800.0 A in 0.1A units)
                                0xCB: b"\x0A\x00\x1F\x40", # Min/max discharging current
                                0xCC: b"\x41",           # Re-interconnection permission - permitted
                                0xCD: b"\x41",           # Operation permission - permitted
                                0xCE: b"\x41",           # Independent operation permission - permitted
                                0xD2: b"\x0C\x35",       # Rated voltage (3125 V)
                                0xD3: b"\x64",           # Instantaneous charging/discharging power (-100 W, signed)
                                0xD4: b"\x0A",           # Instantaneous current (1.0 A in 0.1A units)
                                0xD5: b"\x0C\x35",       # Instantaneous voltage (3125 V)
                                0xD6: b"\x00\x00\x03",    # Cumulative discharging electric energy (3 Wh)
                                0xD8: b"\x00\x00\x04",    # Cumulative charging electric energy (4 Wh)
                                0xDB: b"\x00",           # System-interconnected type - reverse power flow acceptable

                                # Additional optional properties for testing
                                0xDC: b"\x00\x32\x00\x64", # Min/max charging power at Independent (100/100 W)
                                0xDD: b"\x00\x32\x00\x64", # Min/max discharging power at Independent (100/100 W)
                                0xDE: b"\x0A\x00\x1F\x40", # Min/max charging current at Independent (1000.0/800.0 A in 0.1A units)
                                0xDF: b"\x0A\x00\x1F\x40", # Min/max discharging current at Independent (1000.0/800.0 A in 0.1A units)
                                0xE2: b"\x00\x0B\xC4",    # Remaining stored electricity 1 (3012 Wh)
                                0xE3: b"\x00\x64",        # Remaining stored electricity 2 (100 * 0.1Ah = 10Ah)
                                0xE4: b"\x78",            # Remaining stored electricity 3 (90%)

                                # GETMAP and SETMAP
                                0xF9: [0x80, 0xA2, 0xA3, 0xC7, 0xCF, 0xD0, 0xD1, 0xE5, 0xE6],
                                0xFA: [0x80, 0xA2, 0xA3, 0xC7, 0xCF, 0xD0, 0xD1, 0xE5, 0xE6],
                            }
                        },
                    },
                },
            },
        }

    async def echonetMessage(
        self, host, eojgc, eojcc, eojci, message_type, opc
    ):  # pylint: disable=unused-argument
        """Simulate successful ECHONET message response."""
        return True


class TestStorageBattery(unittest.IsolatedAsyncioTestCase):
    """Test cases for StorageBattery device class.

    Uses EOJX codes: group=0x02, class=0x7D (Storage Battery)
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    async def test_get_operation_status_returns_bytes(self):
        """Test getOperationStatus returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        status = await battery.getOperationStatus()
        self.assertEqual(status, b"\x30")  # on (raw bytes)

    async def test_get_chargeable_capacity_returns_bytes(self):
        """Test getChargeableCapacity returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        capacity = await battery.getChargeableCapacity()
        self.assertEqual(capacity, b"\x00\x0A\xF5")  # 2550 (raw bytes)

    async def test_get_dischargeable_capacity_returns_bytes(self):
        """Test getDischargeableCapacity returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        capacity = await battery.getDischargeableCapacity()
        self.assertEqual(capacity, b"\x00\x0B\xC4")  # 3012 (raw bytes)

    async def test_get_operation_mode_returns_bytes(self):
        """Test getOperationMode returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        mode = await battery.getOperationMode()
        self.assertEqual(mode, b"\x42")  # charging (raw bytes)

    async def test_get_battery_type_returns_bytes(self):
        """Test getBatteryType returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        btype = await battery.getBatteryType()
        self.assertEqual(btype, b"\x04")  # Lithium (raw bytes)

    # Additional getters for EPC=0xA0 - AC effective capacity (charging)
    async def test_get_ac_effective_charging_capacity_returns_bytes(self):
        """Test getAcEffectiveChargingCapacity returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        capacity = await battery.getAcEffectiveChargingCapacity()
        self.assertEqual(capacity, b"\x00\x01\x00")  # 256 Wh (raw bytes)

    async def test_get_ac_effective_discharging_capacity_returns_bytes(self):
        """Test getAcEffectiveDischargingCapacity returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        capacity = await battery.getAcEffectiveDischargingCapacity()
        self.assertEqual(capacity, b"\x00\x01\xF4")  # 500 Wh (raw bytes)

    async def test_get_chargeable_electric_energy_returns_bytes(self):
        """Test getChargeableElectricEnergy returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        energy = await battery.getChargeableElectricEnergy()
        self.assertEqual(energy, b"\x00\x0A\xF5")  # 2550 Wh (raw bytes)

    async def test_get_dischargeable_electric_energy_returns_bytes(self):
        """Test getDischargeableElectricEnergy returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        energy = await battery.getDischargeableElectricEnergy()
        self.assertEqual(energy, b"\x00\x0B\xC4")  # 3012 Wh (raw bytes)

    async def test_get_ac_cumulative_charging_electric_energy_returns_bytes(self):
        """Test getAcCumulativeChargingElectricEnergy returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        energy = await battery.getAcCumulativeChargingElectricEnergy()
        self.assertEqual(energy, b"\x00\x00\x01")  # 1 Wh (raw bytes)

    async def test_get_ac_cumulative_discharging_electric_energy_returns_bytes(self):
        """Test getAcCumulativeDischargingElectricEnergy returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        energy = await battery.getAcCumulativeDischargingElectricEnergy()
        self.assertEqual(energy, b"\x00\x00\x02")  # 2 Wh (raw bytes)

    async def test_get_ac_charge_amount_setting_value_returns_bytes(self):
        """Test getAcChargeAmountSettingValue returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        value = await battery.getAcChargeAmountSettingValue()
        self.assertEqual(value, b"\x00\x0A\xF5")  # 2550 Wh (raw bytes)

    async def test_get_ac_discharge_amount_setting_value_returns_bytes(self):
        """Test getAcDischargeAmountSettingValue returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        value = await battery.getAcDischargeAmountSettingValue()
        self.assertEqual(value, b"\x00\x0B\xC4")  # 3012 Wh (raw bytes)

    async def test_get_charging_method_returns_bytes(self):
        """Test getChargingMethod returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        method = await battery.getChargingMethod()
        self.assertEqual(method, b"\x01")  # maximum (raw bytes)

    async def test_get_discharging_method_returns_bytes(self):
        """Test getDischargingMethod returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        method = await battery.getDischargingMethod()
        self.assertEqual(method, b"\x01")  # maximum (raw bytes)

    async def test_get_ac_rated_electric_energy_returns_bytes(self):
        """Test getAcRatedElectricEnergy returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        energy = await battery.getAcRatedElectricEnergy()
        self.assertEqual(energy, b"\x00\x00\xC8")  # 300 Wh (raw bytes)

    async def test_get_minimum_and_maximum_charging_electric_power_returns_bytes(self):
        """Test getMinimumAndMaximumChargingElectricPower returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        power = await battery.getMinimumAndMaximumChargingElectricPower()
        self.assertEqual(power, b"\x00\x64\x00\xC8")  # 300/200 W (raw bytes)

    async def test_get_minimum_and_maximum_discharging_electric_power_returns_bytes(self):
        """Test getMinimumAndMaximumDischargingElectricPower returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        power = await battery.getMinimumAndMaximumDischargingElectricPower()
        self.assertEqual(power, b"\x00\x64\x00\xC8")  # 300/200 W (raw bytes)

    async def test_get_minimum_and_maximum_charging_current_returns_bytes(self):
        """Test getMinimumAndMaximumChargingCurrent returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        current = await battery.getMinimumAndMaximumChargingCurrent()
        self.assertEqual(current, b"\x0A\x00\x1F\x40")  # 1000.0/800.0 A in 0.1A units (raw bytes)

    async def test_get_minimum_and_maximum_discharging_current_returns_bytes(self):
        """Test getMinimumAndMaximumDischargingCurrent returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        current = await battery.getMinimumAndMaximumDischargingCurrent()
        self.assertEqual(current, b"\x0A\x00\x1F\x40")  # 1000.0/800.0 A in 0.1A units (raw bytes)

    async def test_get_actual_operation_mode_returns_bytes(self):
        """Test getActualOperationMode returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        mode = await battery.getActualOperationMode()
        self.assertEqual(mode, b"\x42")  # charging (raw bytes)

    async def test_get_rated_electric_energy_returns_bytes(self):
        """Test getRatedElectricEnergy returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        energy = await battery.getRatedElectricEnergy()
        self.assertEqual(energy, b"\x00\x0C\x35")  # 3125 Wh (raw bytes)

    async def test_get_rated_capacity_returns_bytes(self):
        """Test getRatedCapacity returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        capacity = await battery.getRatedCapacity()
        self.assertEqual(capacity, b"\x00\x64")  # 10 Ah (raw bytes)

    async def test_get_rated_voltage_returns_bytes(self):
        """Test getRatedVoltage returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        voltage = await battery.getRatedVoltage()
        self.assertEqual(voltage, b"\x0C\x35")  # 3125 V (raw bytes)

    async def test_get_instantaneous_charging_and_discharging_electric_power_returns_bytes(self):
        """Test getInstantaneousChargingAndDischargingElectricPower returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        power = await battery.getInstantaneousChargingAndDischargingElectricPower()
        self.assertEqual(power, b"\x64")  # -100 W (signed raw bytes)

    async def test_get_instantaneous_charging_and_discharging_current_returns_bytes(self):
        """Test getInstantaneousChargingAndDischargingCurrent returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        current = await battery.getInstantaneousChargingAndDischargingCurrent()
        self.assertEqual(current, b"\x0A")  # 1.0 A (raw bytes)

    async def test_get_instantaneous_charging_and_discharging_voltage_returns_bytes(self):
        """Test getInstantaneousChargingAndDischargingVoltage returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        voltage = await battery.getInstantaneousChargingAndDischargingVoltage()
        self.assertEqual(voltage, b"\x0C\x35")  # 3125 V (raw bytes)

    async def test_get_cumulative_discharging_electric_energy_returns_bytes(self):
        """Test getCumulativeDischargingElectricEnergy returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        energy = await battery.getCumulativeDischargingElectricEnergy()
        self.assertEqual(energy, b"\x00\x00\x03")  # 3 Wh (raw bytes)

    async def test_get_cumulative_charging_electric_energy_returns_bytes(self):
        """Test getCumulativeChargingElectricEnergy returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        energy = await battery.getCumulativeChargingElectricEnergy()
        self.assertEqual(energy, b"\x00\x00\x04")  # 4 Wh (raw bytes)

    async def test_get_power_system_interconnection_status_returns_bytes(self):
        """Test getPowerSystemInterconnectionStatus returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        status = await battery.getPowerSystemInterconnectionStatus()
        self.assertEqual(status, b"\x00")  # reversePowerFlowAcceptable (raw bytes)

    async def test_get_minimum_and_maximum_charging_power_at_independent_returns_bytes(self):
        """Test getMinimumAndMaximumChargingPowerAtIndependent returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        power = await battery.getMinimumAndMaximumChargingPowerAtIndependent()
        self.assertEqual(power, b"\x00\x32\x00\x64")  # 100/100 W (raw bytes)

    async def test_get_minimum_and_maximum_discharging_power_at_independent_returns_bytes(self):
        """Test getMinimumAndMaximumDischargingPowerAtIndependent returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        power = await battery.getMinimumAndMaximumDischargingPowerAtIndependent()
        self.assertEqual(power, b"\x00\x32\x00\x64")  # 100/100 W (raw bytes)

    async def test_get_minimum_and_maximum_charging_current_at_independent_returns_bytes(self):
        """Test getMinimumAndMaximumChargingCurrentAtIndependent returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        current = await battery.getMinimumAndMaximumChargingCurrentAtIndependent()
        self.assertEqual(current, b"\x0A\x00\x1F\x40")  # 1000.0/800.0 A (raw bytes)

    async def test_get_minimum_and_maximum_discharging_current_at_independent_returns_bytes(self):
        """Test getMinimumAndMaximumDischargingCurrentAtIndependent returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        current = await battery.getMinimumAndMaximumDischargingCurrentAtIndependent()
        self.assertEqual(current, b"\x0A\x00\x1F\x40")  # 1000.0/800.0 A (raw bytes)

    async def test_get_remaining_capacity_1_returns_bytes(self):
        """Test getRemainingCapacity1 returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        capacity = await battery.getRemainingCapacity1()
        self.assertEqual(capacity, b"\x00\x0B\xC4")  # 3012 Wh (raw bytes)

    async def test_get_remaining_capacity_2_returns_bytes(self):
        """Test getRemainingCapacity2 returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        capacity = await battery.getRemainingCapacity2()
        self.assertEqual(capacity, b"\x00\x64")  # 10 Ah (raw bytes)

    async def test_get_remaining_capacity_3_returns_bytes(self):
        """Test getRemainingCapacity3 returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        capacity = await battery.getRemainingCapacity3()
        self.assertEqual(capacity, b"\x78")  # 90% (raw bytes)

    # Tests for setter methods
    async def test_set_operation_status(self):
        """Test setOperationStatus sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setOperationStatus(0x31)  # OFF
        self.assertTrue(result)

    async def test_set_ac_charge_upper_limit(self):
        """Test setAcChargeUpperLimit sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setAcChargeUpperLimit(80)  # 80%
        self.assertTrue(result)

    async def test_set_dischargeable_capacity(self):
        """Test setDischargeableCapacity sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setDischargeableCapacity(2000)  # 2000 Wh
        self.assertTrue(result)

    async def test_set_ac_charge_upper_limit_setting(self):
        """Test setAcChargeUpperLimitSetting sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setAcChargeUpperLimitSetting(75)  # 75%
        self.assertTrue(result)

    async def test_set_ac_discharge_lower_limit_setting(self):
        """Test setAcDischargeLowerLimitSetting sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setAcDischargeLowerLimitSetting(15)  # 15%
        self.assertTrue(result)

    async def test_set_target_charging_electric_energy(self):
        """Test setTargetChargingElectricEnergy sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setTargetChargingElectricEnergy(3000)  # 3000 Wh
        self.assertTrue(result)

    async def test_set_target_discharging_electric_energy(self):
        """Test setTargetDischargingElectricEnergy sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setTargetDischargingElectricEnergy(3000)  # 3000 Wh
        self.assertTrue(result)

    async def test_set_operation_mode(self):
        """Test setOperationMode sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setOperationMode(0x46)  # auto mode
        self.assertTrue(result)

    async def test_reset_cumulative_discharging_electric_energy(self):
        """Test resetCumulativeDischargingElectricEnergy sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.resetCumulativeDischargingElectricEnergy()
        self.assertTrue(result)

    async def test_reset_cumulative_charging_electric_energy(self):
        """Test resetCumulativeChargingElectricEnergy sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.resetCumulativeChargingElectricEnergy()
        self.assertTrue(result)

    async def test_set_charging_and_discharging_amount_1(self):
        """Test setChargingAndDischargingAmount1 sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setChargingAndDischargingAmount1(5000)  # 5000 Wh
        self.assertTrue(result)

    async def test_set_charging_and_discharging_amount_2(self):
        """Test setChargingAndDischargingAmount2 sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setChargingAndDischargingAmount2(5000)  # 5000 Wh
        self.assertTrue(result)

    async def test_set_charging_amount_1(self):
        """Test setChargingAmount1 sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setChargingAmount1(4000)  # 4000 Wh
        self.assertTrue(result)

    async def test_set_discharging_amount_1(self):
        """Test setDischargingAmount1 sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setDischargingAmount1(4000)  # 4000 Wh
        self.assertTrue(result)

    async def test_set_charging_amount_2(self):
        """Test setChargingAmount2 sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setChargingAmount2(4000)  # 4000 Wh
        self.assertTrue(result)

    async def test_set_discharging_amount_2(self):
        """Test setDischargingAmount2 sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setDischargingAmount2(4000)  # 4000 Wh
        self.assertTrue(result)

    async def test_set_charging_power_setting(self):
        """Test setChargingPowerSetting sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setChargingPowerSetting(300)  # 300 W AC
        self.assertTrue(result)

    async def test_set_discharging_power_setting(self):
        """Test setDischargingPowerSetting sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setDischargingPowerSetting(300)  # 300 W AC
        self.assertTrue(result)

    async def test_set_charging_current_setting(self):
        """Test setChargingCurrentSetting sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setChargingCurrentSetting(100)  # 10 A (in 0.1A units)
        self.assertTrue(result)

    async def test_set_discharging_current_setting(self):
        """Test setDischargingCurrentSetting sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setDischargingCurrentSetting(100)  # 10 A (in 0.1A units)
        self.assertTrue(result)

    async def test_set_re_interconnection_permission(self):
        """Test setReInterconnectionPermission sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setReInterconnectionPermission(0x41)  # permitted
        self.assertTrue(result)

    async def test_set_operation_permission(self):
        """Test setOperationPermission sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setOperationPermission(0x41)  # permitted
        self.assertTrue(result)

    async def test_set_independent_operation_permission(self):
        """Test setIndependentOperationPermission sends correct message."""
        api_connector = MockECHONETAPIClient()
        battery = StorageBattery("192.168.1.50", api_connector)

        result = await battery.setIndependentOperationPermission(0x41)  # permitted
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
