"""Unit tests for TemperatureSensor ECHONET device class."""
import unittest
from pychonet.EchonetInstance import EchonetInstance
from pychonet.TemperatureSensor import TemperatureSensor, MEASURED_TEMP


class MockECHONETAPIClient:
    """Mock API client for testing TemperatureSensor functionality.

    Uses EOJX codes: group=0x00, class=0x11 (Temperature sensor)
    """

    def __init__(self):
        self._state = {
            "192.168.1.55": {
                "instances": {
                    0x00: {  # Group code: Sensor device group
                        0x11: {  # Class code: Temperature sensor
                            0x01: {
                                MEASURED_TEMP: b"\x01\x2c",  # 30.0°C (0x12c / 10)
                                0x9F: [MEASURED_TEMP],  # GETMAP
                                0x9E: [],  # SETMAP (read-only device)
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


class TestTemperatureSensor(unittest.IsolatedAsyncioTestCase):
    """Test cases for TemperatureSensor device class.

    Uses EOJX codes: group=0x00, class=0x11 (Temperature sensor)
    Expected value: 0x12c = 300 / 10 = 30.0°C
    """

    async def test_getMeasuredTemperature(self):
        """Test getMeasuredTemperature returns correct float value."""
        api_connector = MockECHONETAPIClient()
        sensor = TemperatureSensor("192.168.1.55", api_connector)

        temperature = await sensor.getMeasuredTemperature()
        self.assertEqual(temperature, b"\x01\x2c")  # Raw value 300 = 30.0°C

    async def test_update_returns_formatted_temperature(self):
        """Test update method returns formatted float value."""
        api_connector = MockECHONETAPIClient()
        sensor = TemperatureSensor("192.168.1.55", api_connector)

        result = await sensor.update(MEASURED_TEMP)
        self.assertEqual(result, 30.0)

    async def test_update_with_invalid_epc_returns_none(self):
        """Test update with invalid EPC code returns None."""
        api_connector = MockECHONETAPIClient()
        sensor = TemperatureSensor("192.168.1.55", api_connector)

        result = await sensor.update(0xFF)  # Invalid EPC
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
