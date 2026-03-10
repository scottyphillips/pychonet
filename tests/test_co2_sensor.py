"""Unit tests for CO2Sensor ECHONET device class."""
import unittest
from pychonet.CO2Sensor import CO2Sensor


class MockECHONETAPIClient:
    """Mock API client for testing CO2Sensor functionality.

    Uses EOJX codes: group=0x00, class=0x1B (CO2 sensor)
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    def __init__(self):
        self._state = {
            "192.168.1.10": {
                "instances": {
                    0x00: {  # EoJGC (Class Group Code) for Air conditioner-related device
                        0x1B: {  # EoJCC (Class Code) for CO2 Sensor
                            0x01: {  # Instance code
                                0x80: b"\x30",   # Operation status: on
                                0xE0: b"\x00\x00\x0E\xA4",  # CO2 concentration: 3750 ppm (raw bytes)
                                0x9F: [0x80, 0xE0],  # GETMAP
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


class TestCO2Sensor(unittest.IsolatedAsyncioTestCase):
    """Test cases for CO2Sensor device class.

    Uses EOJX codes: group=0x00, class=0x1B (CO2 sensor)
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    async def test_get_operation_status_returns_bytes(self):
        """Test getOperationStatus returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        sensor = CO2Sensor("192.168.1.10", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b"\x30")  # on (raw bytes)

    async def test_set_operation_status(self):
        """Test setOperationStatus sets correct value."""
        api_connector = MockECHONETAPIClient()
        sensor = CO2Sensor("192.168.1.10", api_connector)

        result = await sensor.setOperationStatus(0x31)  # off
        self.assertTrue(result)

    async def test_get_co2_concentration_returns_bytes(self):
        """Test getCO2Concentration returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        sensor = CO2Sensor("192.168.1.10", api_connector)

        co2_level = await sensor.getCO2Concentration()
        self.assertEqual(co2_level, b"\x00\x00\x0E\xA4")  # 3750 ppm (raw bytes)


if __name__ == "__main__":
    unittest.main()
