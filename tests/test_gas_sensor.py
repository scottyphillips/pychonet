"""Unit tests for GasSensor ECHONET device class."""
import unittest
from pychonet.GasSensor import GasSensor


class MockECHONETAPIClient:
    """Mock API client for testing GasSensor functionality.

    Uses EOJX codes: group=0x00, class=0x1C (Gas sensor)
    EPCs cover operation status, detection threshold, and gas concentration
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    def __init__(self):
        self._state = {
            "192.168.1.75": {
                "instances": {
                    0x00: {  # EoJGC (Class Group Code) for Gas Sensor
                        0x1C: {  # EoJCC (Class Code) for Gas Sensor
                            0x01: {  # Instance code
                                0x80: b"\x30",  # Operation status: on
                                0xB0: b"\x03",  # Detection threshold level: Level 3
                                0xB1: b"\x42",  # Gas detection status: not found
                                0xE0: b"\x0A",  # Measured gas concentration (10 ppm)
                                0x9F: [0x80, 0xB0, 0xB1, 0xE0],  # GETMAP
                                0x9E: [0x80, 0xB0],  # SETMAP
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


class TestGasSensor(unittest.IsolatedAsyncioTestCase):
    """Test cases for GasSensor device class.

    Uses EOJX codes: group=0x00, class=0x1C (Gas sensor)
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    async def test_getOperationStatus_returns_bytes(self):
        """Test getOperationStatus returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        sensor = GasSensor("192.168.1.75", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b"\x30")  # on (raw bytes)

    async def test_setOperationStatus(self):
        """Test setOperationStatus sets correct value."""
        api_connector = MockECHONETAPIClient()
        sensor = GasSensor("192.168.1.75", api_connector)

        result = await sensor.setOperationStatus(0x31)  # off
        self.assertTrue(result)

    async def test_getDetectionThresholdLevel_returns_bytes(self):
        """Test getDetectionThresholdLevel returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        sensor = GasSensor("192.168.1.75", api_connector)

        level = await sensor.getDetectionThresholdLevel()
        self.assertEqual(level, b"\x03")  # Level 3 (raw bytes)

    async def test_setDetectionThresholdLevel(self):
        """Test setDetectionThresholdLevel sets correct value."""
        api_connector = MockECHONETAPIClient()
        sensor = GasSensor("192.168.1.75", api_connector)

        result = await sensor.setDetectionThresholdLevel(0x05)  # Level 5
        self.assertTrue(result)

    async def test_getGasDetectionStatus_returns_bytes(self):
        """Test getGasDetectionStatus returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        sensor = GasSensor("192.168.1.75", api_connector)

        status = await sensor.getGasDetectionStatus()
        self.assertEqual(status, b"\x42")  # not found (raw bytes)

    async def test_getGasConcentration_returns_bytes(self):
        """Test getGasConcentration returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        sensor = GasSensor("192.168.1.75", api_connector)

        concentration = await sensor.getGasConcentration()
        self.assertEqual(concentration, b"\x0A")  # raw bytes (unsigned short, 10 ppm)

    async def test_update_returns_all_properties(self):
        """Test update method returns dictionary with all properties."""
        api_connector = MockECHONETAPIClient()
        sensor = GasSensor("192.168.1.75", api_connector)

        result = await sensor.update()
        self.assertIsInstance(result, dict)
        self.assertIn(0x80, result)  # Operation status
        self.assertIn(0xB0, result)  # Detection threshold level
        self.assertIn(0xB1, result)  # Gas detection status


if __name__ == "__main__":
    unittest.main()
