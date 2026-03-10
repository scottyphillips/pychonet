"""Unit tests for ElectricShutter ECHONET device class."""
import unittest
from pychonet.ElectricShutter import ElectricShutter


class MockECHONETAPIClient:
    """Mock API client for testing ElectricShutter functionality.

    Uses EOJX codes: group=0x02, class=0x61 (Electric shutter)
    Inherits EPCs from ElectricBlind: E0=open/close state, EA=open/closed status,
    C2=winds detection, C3=sunlight detection
    """

    def __init__(self):
        self._state = {
            "192.168.1.71": {
                "instances": {
                    0x02: {  # Group code: Housing/facility-related device group
                        0x61: {  # Class code: Electric shutter
                            0x01: {
                                0x80: b"\x30",  # Operation status (ON) - from EchonetInstance
                                0xE0: b"\x41",  # Open/close state (fully open)
                                0xEA: b"\x41",  # Open/closed status (fully open)
                                0xC2: b"\x30",  # Wind detection (no wind detected)
                                0xC3: b"\x30",  # Sunlight detection (no sunlight detected)
                                0xE1: b"\x41",  # Degree-of-opening level
                                0x9F: [0x80, 0xE0, 0xEA, 0xC2, 0xC3, 0xE1],  # GETMAP
                                0x9E: [0x80],  # SETMAP (only operation status can be set)
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


class TestElectricShutter(unittest.IsolatedAsyncioTestCase):
    """Test cases for ElectricShutter device class.

    Uses EOJX codes: group=0x02, class=0x61 (Electric shutter)
    """

    async def test_getOperationalStatus(self):
        """Test getOperationalStatus returns correct value."""
        api_connector = MockECHONETAPIClient()
        shutter = ElectricShutter("192.168.1.71", api_connector)

        status = await shutter.getOperationalStatus()
        self.assertEqual(status, b"\x30")  # ON

    async def test_on(self):
        """Test on() sets operation status to ON."""
        api_connector = MockECHONETAPIClient()
        shutter = ElectricShutter("192.168.1.71", api_connector)

        result = await shutter.on()
        self.assertTrue(result)

    async def test_off(self):
        """Test off() sets operation status to OFF."""
        api_connector = MockECHONETAPIClient()
        shutter = ElectricShutter("192.168.1.71", api_connector)

        result = await shutter.off()
        self.assertTrue(result)

    async def test_getOpenCloseState(self):
        """Test getOpenCloseSetting returns correct value."""
        api_connector = MockECHONETAPIClient()
        shutter = ElectricShutter("192.168.1.71", api_connector)

        state = await shutter.getOpenCloseSetting()
        self.assertEqual(state, b"\x41")  # Fully open


if __name__ == "__main__":
    unittest.main()
