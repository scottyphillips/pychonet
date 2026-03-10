"""Unit tests for CeilingFan ECHONET device class."""
import unittest
from pychonet.CeilingFan import CeilingFan


class MockECHONETAPIClient:
    """Mock API client for testing CeilingFan functionality.

    Uses EOJX codes: group=0x01, class=0x3A (Ceiling Fan)
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    def __init__(self):
        self._state = {
            "192.168.1.50": {
                "instances": {
                    0x01: {  # EoJGC (Class Group Code) for Air conditioner-related device
                        0x3A: {  # EoJCC (Class Code) for Ceiling Fan
                            0x01: {  # Instance code
                                0x80: b"\x30",   # Operation status: on
                                0xF0: b"\x35",   # Fan speed: 50% (raw bytes)
                                0xF1: b"\x42",   # Fan direction: reverse
                                0xF2: b"\x30",   # Oscillation: on
                                0xF3: b"\x30",   # Light status: on
                                0x9F: [0x80, 0xF0, 0xF1, 0xF2, 0xF3],  # GETMAP
                                0x9E: [0x80, 0xF0, 0xF1, 0xF2, 0xF3],  # SETMAP
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


class TestCeilingFan(unittest.IsolatedAsyncioTestCase):
    """Test cases for CeilingFan device class.

    Uses EOJX codes: group=0x01, class=0x3A (Ceiling Fan)
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    async def test_get_operation_status_returns_bytes(self):
        """Test getOperationalStatus returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        fan = CeilingFan("192.168.1.50", api_connector)

        status = await fan.getOperationalStatus()
        self.assertEqual(status, b"\x30")  # on (raw bytes)

    async def test_get_fan_speed_percent_returns_bytes(self):
        """Test getFanSpeedPercent returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        fan = CeilingFan("192.168.1.50", api_connector)

        speed = await fan.getFanSpeedPercent()
        self.assertEqual(speed, b"\x35")  # 50% (raw bytes)

    async def test_get_fan_direction_returns_bytes(self):
        """Test getFanDirection returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        fan = CeilingFan("192.168.1.50", api_connector)

        direction = await fan.getFanDirection()
        self.assertEqual(direction, b"\x42")  # reverse (raw bytes)

    async def test_get_fan_oscillation_returns_bytes(self):
        """Test getFanOscillation returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        fan = CeilingFan("192.168.1.50", api_connector)

        oscillation = await fan.getFanOscillation()
        self.assertEqual(oscillation, b"\x30")  # on (raw bytes)


if __name__ == "__main__":
    unittest.main()
