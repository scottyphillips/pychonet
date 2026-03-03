"""Unit tests for ElectricWaterHeater ECHONET device class."""
import unittest
from pychonet.EchonetInstance import EchonetInstance
from pychonet.ElectricWaterHeater import ElectricWaterHeater


class MockECHONETAPIClient:
    """Mock API client for testing ElectricWaterHeater functionality.

    Uses EOJX codes: group=0x02, class=0x6B (Electric water heater)
    """

    def __init__(self):
        self._state = {
            "192.168.1.60": {
                "instances": {
                    0x02: {  # Group code: Water heater device group
                        0x6B: {  # Class code: Electric water heater
                            0x01: {
                                # Operation and status values
                                0xB0: b"\x41",  # Automatic water heating setting (Automatic)
                                0xB2: b"\x42",  # Water heating status (not heating)
                                0xC3: b"\x41",  # Hot water supply status (supplying hot water)
                                0xE1: b"\x64",  # Measured amount of hot water remaining (100 L)
                                0xEA: b"\x42",  # Bath operation status monitor (stopped)
                                # Alarm and settings
                                0xC2: b"\x00",  # Alarm Status (normal - no alarms)
                                0xB6: b"\x41",  # Tank Operation mode setting (Standard)
                                # Property maps
                                0x9F: [0xB0, 0xB2, 0xC3, 0xE1, 0xEA, 0xC2],  # GETMAP
                                0x9E: [0xB0],  # SETMAP
                            }
                        },
                    },
                }
            }
        }

    async def echonetMessage(
        self, host, eojgc, eojcc, eojci, message_type, opc
    ):  # pylint: disable=unused-argument
        """Simulate successful ECHONET message response."""
        return True


class TestElectricWaterHeater(unittest.IsolatedAsyncioTestCase):
    """Test cases for ElectricWaterHeater device class.

    Uses EOJX codes: group=0x02, class=0x6B (Electric water heater)
    """

    async def test_getOperationStatus(self):
        """Test getOperationStatus returns correct value."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricWaterHeater("192.168.1.60", api_connector)

        # Note: Operation status for water heater is typically EPC 0xB2 (water heating status)
        result = await heater.update(0xB2)
        self.assertEqual(result, "not heating")  # Value from DICT_41_HEATING_NOT_HEATING

    async def test_getHotWaterSupplyStatus(self):
        """Test get hot water supply status returns correct value."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricWaterHeater("192.168.1.60", api_connector)

        result = await heater.update(0xC3)
        self.assertEqual(result, "Supplying hot water")  # Value from DICT_41_HEATING_NOT_HEATING

    async def test_getMeasuredHotWaterAmount(self):
        """Test get measured amount of hot water remaining."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricWaterHeater("192.168.1.60", api_connector)

        result = await heater.update(0xE1)
        self.assertEqual(result, 100)  # Measured amount in liters

    async def test_getBathOperationStatus(self):
        """Test get bath operation status monitor."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricWaterHeater("192.168.1.60", api_connector)

        result = await heater.update(0xEA)
        self.assertEqual(result, "Stopped")  # Value from DICT_41_HEATING_NOT_HEATING

    async def test_getAlarmStatus(self):
        """Test get alarm status returns correct structure."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricWaterHeater("192.168.1.60", api_connector)

        result = await heater.update(0xC2)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["Out of Hot Water"], "Normal")
        self.assertEqual(result["Water leaking"], "Normal")
        self.assertEqual(result["Water frozen"], "Normal")


if __name__ == "__main__":
    unittest.main()
