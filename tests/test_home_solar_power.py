"""Unit tests for HomeSolarPower ECHONET device class."""
import unittest
from pychonet.HomeSolarPower import HomeSolarPower


class MockECHONETAPIClient:
    """Mock API client for testing HomeSolarPower functionality.

    Uses EOJX codes: group=0x02, class=0x79 (System-interconnected type)
    EPCs include power measurements and system status
    """

    def __init__(self):
        self._state = {
            "192.168.1.100": {
                "instances": {
                    0x02: {  # EoJGC (Class Group Code) for System-interconnected type
                        0x79: {  # EoJCC (Class Code) for Home Solar Power
                            0x01: {  # Instance code
                                0xE0: b"\x00\x00\x0A\xF8",  # Measured instant power (2088W)
                                0xE1: b"\x00\x00\x51\xE0",  # Measured cumul power (20960 Wh = 20.96 kWh)
                                0xD0: b"\x00",  # System-interconnected type (reverse acceptable)
                                0xD1: b"\x44",  # Output power restraint status (Not restraining)
                                0x9F: [0xE0, 0xE1, 0xD0, 0xD1],  # GETMAP
                                0x9E: [],  # SETMAP (read-only device)
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


class TestHomeSolarPower(unittest.IsolatedAsyncioTestCase):
    """Test cases for HomeSolarPower device class.

    Uses EOJX codes: group=0x02, class=0x79 (System-interconnected type)
    """

    async def test_getMeasuredInstantPower(self):
        """Test getMeasuredInstantPower returns correct value."""
        api_connector = MockECHONETAPIClient()
        solar_power = HomeSolarPower("192.168.1.100", api_connector)

        power = await solar_power.update(0xE0)
        self.assertEqual(power, 2808)  # Watts

    async def test_getMeasuredCumulPower(self):
        """Test getMeasuredCumulPower returns correct value."""
        api_connector = MockECHONETAPIClient()
        solar_power = HomeSolarPower("192.168.1.100", api_connector)

        power = await solar_power.update(0xE1)
        self.assertEqual(power, 20960)  # Wh (20.96 kWh)

    async def test_getSystemInterconnectedType(self):
        """Test getSystemInterconnectedType returns correct value."""
        api_connector = MockECHONETAPIClient()
        solar_power = HomeSolarPower("192.168.1.100", api_connector)

        sys_type = await solar_power.update(0xD0)
        self.assertEqual(sys_type, "System interconnected (reverse power flow acceptable)")


if __name__ == "__main__":
    unittest.main()
