"""Unit tests for HomeAirCleaner ECHONET device class."""
import unittest
from pychonet.EchonetInstance import EchonetInstance
from pychonet.HomeAirCleaner import HomeAirCleaner


class MockECHONETAPIClient:
    """Mock API client for testing HomeAirCleaner functionality."""

    def __init__(self):
        self._state = {
            "192.168.1.50": {
                "instances": {
                    0x01: {  # Group code: Air conditioner-related device group
                        0x35: {  # Class code: Home air cleaner
                            0x01: {
                                0xA0: b"\x42",  # Fan speed (auto mode)
                                0xC0: b"\x41",  # Air pollution status (pollution)
                                0xC1: b"\x31",  # Cigarette sensor (on)
                                0xC2: b"\x30",  # Photocatalyst (off)
                                0xE1: b"\x42",  # Filter change status (yes)
                                0x9F: [0xA0, 0xC0, 0xC1, 0xC2, 0xE1],  # GETMAP
                                0x9E: [0xA0, 0xC2],  # SETMAP
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


class TestHomeAirCleaner(unittest.IsolatedAsyncioTestCase):
    """Test cases for HomeAirCleaner device class.

    Uses EOJX codes: group=0x01, class=0x35 (Home air cleaner)
    """

    async def test_getFanSpeed(self):
        """Test getFanSpeed returns correct value."""
        api_connector = MockECHONETAPIClient()
        ac = HomeAirCleaner("192.168.1.50", api_connector)

        fan_speed = await ac.getFanSpeed()
        self.assertEqual(fan_speed, b"\x42")  # 'auto' mode

    async def test_setFanSpeed(self):
        """Test setFanSpeed with valid fan speed value."""
        api_connector = MockECHONETAPIClient()
        ac = HomeAirCleaner("192.168.1.50", api_connector)

        result = await ac.setFanSpeed("auto")
        self.assertTrue(result)

    async def test_getAirPollutionStatus(self):
        """Test getAirPollutionStatus returns correct value."""
        api_connector = MockECHONETAPIClient()
        ac = HomeAirCleaner("192.168.1.50", api_connector)

        status = await ac.getAirPollutionStatus()
        self.assertEqual(status, b"\x41")  # 'pollution'

    async def test_getCigaretteSensorStatus(self):
        """Test getCigaretteSensorStatus returns correct value."""
        api_connector = MockECHONETAPIClient()
        ac = HomeAirCleaner("192.168.1.50", api_connector)

        status = await ac.getCigaretteSensorStatus()
        self.assertEqual(status, b"\x31")  # 'on'

    async def test_getPhotocatalystStatus(self):
        """Test getPhotocatalystStatus returns correct value."""
        api_connector = MockECHONETAPIClient()
        ac = HomeAirCleaner("192.168.1.50", api_connector)

        status = await ac.getPhotocatalystStatus()
        self.assertEqual(status, b"\x30")  # 'off'

    async def test_setPhotocatalyst(self):
        """Test setPhotocatalyst with valid value."""
        api_connector = MockECHONETAPIClient()
        ac = HomeAirCleaner("192.168.1.50", api_connector)

        # PHOTOCATALYST_STATUS maps 'yes'/'no' to EPC values
        result = await ac.setPhotocatalyst("yes")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
