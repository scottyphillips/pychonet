"""Unit tests for FloorHeater ECHONET device class."""
import unittest
from pychonet.FloorHeater import FloorHeater


class MockECHONETAPIClient:
    """Mock API client for testing FloorHeater functionality.

    Uses EOJX codes: group=0x02, class=0x7B (Floor heater)
    EPCs include temperature settings, measured temperatures, timers, power consumption
    """

    def __init__(self):
        self._state = {
            "192.168.1.85": {
                "instances": {
                    0x02: {  # EoJGC (Class Group Code) for Floor Heater
                        0x7B: {  # EoJCC (Class Code) for Floor Heater
                            0x01: {  # Instance code
                                0xE0: b"\x41",  # Temperature setting 1
                                0xE1: b"\x42",  # Temperature setting 2
                                0xD1: b"\xFF",  # Maximum settable level
                                0xE2: b"\xFF\x38",  # Measured room temp (-20.0°C as int16 * 0.1)
                                0xE3: b"\xFF\x60",  # Measured floor temp (-16.0°C as int16 * 0.1)
                                0xE5: b"\x41",  # Special operation setting (Normal)
                                0xE6: b"\x41",  # Daily timer setting (Timer 1)
                                0x90: b"\x30",  # ON timer reservation (ON)
                                0x91: b"\x08\x30",  # Time set by ON timer (08:30)
                                0x92: b"\x00\x02",  # Relative ON timer setting
                                0x94: b"\x30",  # OFF timer reservation (ON)
                                0x95: b"\x1E\x00",  # Time set by OFF timer
                                0x84: b"\xFF\xF2",  # Instantaneous power (-14W, signed int16)
                                0x85: b"\x00\x00\x00\x0A",  # Cumulative energy (10kWh)
                                0xE9: b"\x00\x00\x0C\x35",  # Rated power consumption (3125W)
                                0xEA: b"\x41",  # Power consumption measurement method
                                0x9F: [0xE0, 0xE1, 0xD1, 0xE2, 0xE3, 0xE5, 0xE6, 0x90, 0x91, 0x92, 0x94, 0x95, 0x84, 0x85, 0xE9, 0xEA],
                                0x9E: [0xE0, 0xE1, 0xE5, 0xE6, 0x90, 0x92, 0x94, 0x95],
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


class TestFloorHeater(unittest.IsolatedAsyncioTestCase):
    """Test cases for FloorHeater device class.

    Uses EOJX codes: group=0x02, class=0x7B (Floor heater)
    """

    async def test_getMeasuredRoomTemp(self):
        """Test getMeasuredRoomTemp returns correct value."""
        api_connector = MockECHONETAPIClient()
        heater = FloorHeater("192.168.1.85", api_connector)

        temp = await heater.update(0xE2)
        self.assertEqual(temp, -200)  # Signed int conversion for EPC 0xE2 (room temp)

    async def test_getMeasuredFloorTemp(self):
        """Test getMeasuredFloorTemp returns correct value."""
        api_connector = MockECHONETAPIClient()
        heater = FloorHeater("192.168.1.85", api_connector)

        temp = await heater.update(0xE3)
        self.assertEqual(temp, -160)  # Signed int conversion for EPC 0xE3 (floor temp)

    async def test_getTemperatureSetting(self):
        """Test getTemperatureSetting returns correct value."""
        api_connector = MockECHONETAPIClient()
        heater = FloorHeater("192.168.1.85", api_connector)

        setting = await heater.update(0xE0)
        self.assertEqual(setting, 65)

    async def test_getMeasuredInstantPower(self):
        """Test getMeasuredInstantPower returns correct value."""
        api_connector = MockECHONETAPIClient()
        heater = FloorHeater("192.168.1.85", api_connector)

        power = await heater.update(0x84)
        self.assertEqual(power, 65522)  # Signed int conversion for EPC 0x84

    async def test_getDailyTimerSetting(self):
        """Test getDailyTimerSetting returns correct value."""
        api_connector = MockECHONETAPIClient()
        heater = FloorHeater("192.168.1.85", api_connector)

        setting = await heater.update(0xE6)
        self.assertEqual(setting, "Timer 1")  # Timer 1 for EPC 0xE6


if __name__ == "__main__":
    unittest.main()
