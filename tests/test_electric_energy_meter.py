"""Unit tests for ElectricEnergyMeter ECHONET device class."""
import unittest
from pychonet.ElectricEnergyMeter import ElectricEnergyMeter


class MockECHONETAPIClient:
    """Mock API client for testing ElectricEnergyMeter functionality.

    Uses EOJX codes: group=0x02, class=0x80 (Electric energy meter)
    EPCs cover operation status and cumulative energy readings
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    def __init__(self):
        self._state = {
            "192.168.1.80": {
                "instances": {
                    0x02: {  # EoJGC (Class Group Code) for Power Supply device
                        0x80: {  # EoJCC (Class Code) for Electric Energy Meter
                            0x01: {  # Instance code
                                0x80: b"\x30",   # Operation status: on
                                0xE0: b"\x00\x00\x01\xF4",  # Accumulated energy: 500 kWh (raw bytes)
                                0xE2: b"\x01",     # Energy unit decimal places: 0.1 kWh
                                0xE3: b"\xFF" * 192,  # Measurement log 1: past 24 hours (all unmeasured)
                                0xE4: b"\xFF" * 2880,  # Measurement log 2: past 45 days (all unmeasured)
                                0x9F: [0x80, 0xE0, 0xE2, 0xE3, 0xE4],  # GETMAP
                                0x9E: [0x80],  # SETMAP
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


class TestElectricEnergyMeter(unittest.IsolatedAsyncioTestCase):
    """Test cases for ElectricEnergyMeter device class.

    Uses EOJX codes: group=0x02, class=0x80 (Electric energy meter)
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    async def test_get_operation_status_returns_bytes(self):
        """Test getOperationStatus returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        meter = ElectricEnergyMeter("192.168.1.80", api_connector)

        status = await meter.getOperationStatus()
        self.assertEqual(status, b"\x30")  # on (raw bytes)

    async def test_set_operation_status(self):
        """Test setOperationStatus sets correct value."""
        api_connector = MockECHONETAPIClient()
        meter = ElectricEnergyMeter("192.168.1.80", api_connector)

        result = await meter.setOperationStatus(0x31)  # off
        self.assertTrue(result)

    async def test_get_accumulated_energy_left_returns_bytes(self):
        """Test getAccumulatedEnergyLeft returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        meter = ElectricEnergyMeter("192.168.1.80", api_connector)

        energy = await meter.getAccumulatedEnergyLeft()
        self.assertEqual(energy, b"\x00\x00\x01\xF4")  # 500 kWh (raw bytes)

    async def test_get_energy_unit_decimal_places(self):
        """Test getEnergyUnitDecimalPlaces returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        meter = ElectricEnergyMeter("192.168.1.80", api_connector)

        unit = await meter.getEnergyUnitDecimalPlaces()
        self.assertEqual(unit, b"\x01")  # 0.1 kWh (raw bytes)

    async def test_get_measurement_log_1_returns_bytes(self):
        """Test getMeasurementLog1 returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        meter = ElectricEnergyMeter("192.168.1.80", api_connector)

        log = await meter.getMeasurementLog1()
        self.assertEqual(log, b"\xFF" * 192)  # past 24 hours (raw bytes)

    async def test_get_measurement_log_2_returns_bytes(self):
        """Test getMeasurementLog2 returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        meter = ElectricEnergyMeter("192.168.1.80", api_connector)

        log = await meter.getMeasurementLog2()
        self.assertEqual(log, b"\xFF" * 2880)  # past 45 days (raw bytes)

    async def test_update_returns_all_properties(self):
        """Test update method returns dictionary with all properties."""
        api_connector = MockECHONETAPIClient()
        meter = ElectricEnergyMeter("192.168.1.80", api_connector)

        result = await meter.update()
        self.assertIsInstance(result, dict)
        self.assertIn(0x80, result)  # Operation status
        self.assertIn(0xE0, result)  # Accumulated energy left
        self.assertIn(0xE2, result)  # Energy unit decimal places

    async def test_set_operation_status_to_on(self):
        """Test setOperationStatus sets ON state."""
        api_connector = MockECHONETAPIClient()
        meter = ElectricEnergyMeter("192.168.1.80", api_connector)

        result = await meter.setOperationStatus(0x30)  # on
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
