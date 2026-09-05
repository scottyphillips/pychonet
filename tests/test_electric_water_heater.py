"""Unit tests for ElectricWaterHeater ECHONET device class."""
import unittest
from pychonet.EchonetInstance import EchonetInstance, call_epc_function
from pychonet.ElectricWaterHeater import ElectricWaterHeater
from pychonet.lib.epc_functions import EPC_SUPER_FUNCTIONS


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
                                # Superclass properties
                                0x8F: b"\x41",  # Power-saving operation setting (on)
                                # Property maps
                                0x9F: [
                                    0x8F,
                                    0xB0,
                                    0xB2,
                                    0xC3,
                                    0xE1,
                                    0xEA,
                                    0xC2,
                                ],  # GETMAP
                                0x9E: [0x8F, 0xB0],  # SETMAP
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

    def _logger(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Stub for EchonetInstance.update(), which logs via the API client."""


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

    async def test_getPowerSavingOperationSettingDecoder(self):
        """Test the superclass decoder for EPC 0x8F maps both defined EDT values."""
        self.assertEqual(call_epc_function(EPC_SUPER_FUNCTIONS[0x8F], b"\x41"), "on")
        self.assertEqual(call_epc_function(EPC_SUPER_FUNCTIONS[0x8F], b"\x42"), "off")

    async def test_getPowerSavingOperationSetting(self):
        """Test EPC 0x8F is decoded instead of falling back to a hex string."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricWaterHeater("192.168.1.60", api_connector)
        instance = api_connector._state["192.168.1.60"]["instances"][0x02][0x6B][0x01]

        result = await heater.update(0x8F)
        self.assertEqual(result, "on")  # Value from DICT_41_ON_OFF

        instance[0x8F] = b"\x42"  # Normal operation
        result = await heater.update(0x8F)
        self.assertEqual(result, "off")  # Value from DICT_41_ON_OFF

    async def test_getPowerSavingOperationSettingInBatch(self):
        """Test EPC 0x8F is decoded when requested alongside class properties.

        Guards the branch order in EchonetInstance.update(): the superclass
        function table must be consulted before the hex fallback for EPC codes
        that are known to the superclass but have no class-specific function.
        """
        api_connector = MockECHONETAPIClient()
        heater = ElectricWaterHeater("192.168.1.60", api_connector)

        result = await heater.update([0xB0, 0x8F, 0xE1])
        self.assertIsInstance(result, dict)
        self.assertEqual(result[0x8F], "on")  # Value from DICT_41_ON_OFF
        self.assertEqual(result[0xB0], "Automatic")
        self.assertEqual(result[0xE1], 100)


if __name__ == "__main__":
    unittest.main()
