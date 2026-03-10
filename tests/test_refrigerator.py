"""Unit tests for Refrigerator ECHONET device class."""
import unittest
from pychonet.Refrigerator import Refrigerator


class MockECHONETAPIClient:
    """Mock API client for testing Refrigerator functionality.

    Uses EOJX codes: group=0x03, class=0xB7 (Refrigerator)
    EPCs include door status, temperature settings, measured temperatures, icemaker settings
    """

    def __init__(self):
        self._state = {
            "192.168.1.110": {
                "instances": {
                    0x03: {  # EoJGC (Class Group Code) for Refrigerator
                        0xB7: {  # EoJCC (Class Code) for Refrigerator
                            0x01: {  # Instance code
                                0xB0: b"\x42",  # Door open/close status (Closed)
                                0xB1: b"\x41",  # Door open warning (No warning)
                                0xB2: b"\x42",  # Refrigerator compartment door status (Closed)
                                0xB3: b"\x42",  # Freezer compartment door status (Closed)
                                0xD1: b"\xC7\xD0",  # Measured refrigerator compartment temp (-20.0°C, signed)
                                0xD2: b"\xC8\x90",  # Measured freezer compartment temp (-32.0°C, signed)
                                0xA0: b"\x41",  # Quick freeze function setting (Quick stand-by)
                                0xA4: b"\x30",  # Icemaker setting (Enabled)
                                0xA5: b"\x41",  # Icemaker operation status (Enabled)
                                0xD8: b"\xFF\x80",  # Compressor rotation speed (max=255, current=128)
                                0x9F: [0xB0, 0xB1, 0xB2, 0xB3, 0xD1, 0xD2, 0xA0, 0xA4, 0xA5, 0xD8],
                                0x9E: [0xB0, 0xB1, 0xB2, 0xB3, 0xA0, 0xA4],
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


class TestRefrigerator(unittest.IsolatedAsyncioTestCase):
    """Test cases for Refrigerator device class.

    Uses EOJX codes: group=0x03, class=0xB7 (Refrigerator)
    """

    async def test_getDoorOpenCloseStatus(self):
        """Test getDoorOpenCloseStatus returns correct value."""
        api_connector = MockECHONETAPIClient()
        fridge = Refrigerator("192.168.1.110", api_connector)

        status = await fridge.getDoorOpenCloseStatus()
        self.assertEqual(status, b"\x42")

    async def test_getMeasuredRefrigeratorCompartmentTemp(self):
        """Test getMeasuredRefrigeratorCompartmentTemp returns correct value."""
        api_connector = MockECHONETAPIClient()
        fridge = Refrigerator("192.168.1.110", api_connector)

        temp = await fridge.getMeasuredRefrigeratorCompartmentTemp()
        self.assertEqual(temp, b"\xC7\xD0")  # -20.0°C in signed int16 format
        
    async def test_getIcemakerSetting(self):
        """Test getIcemakerSetting returns correct value."""
        api_connector = MockECHONETAPIClient()
        fridge = Refrigerator("192.168.1.110", api_connector)

        setting = await fridge.getIcemakerSetting()
        self.assertEqual(setting, b"\x30")

    async def test_getCompressorRotationSpeed(self):
        """Test getCompressorRotationSpeed returns correct dict."""
        api_connector = MockECHONETAPIClient()
        fridge = Refrigerator("192.168.1.110", api_connector)

        speed = await fridge.update(0xD8)
        self.assertEqual(speed["maximum_rotation_speed"], 255)
        self.assertEqual(speed["rotation_speed"], 128)


if __name__ == "__main__":
    unittest.main()
