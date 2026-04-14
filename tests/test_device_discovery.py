"""Unit tests for ECHONET device discovery functionality."""
import unittest


class MockECHONETAPIClient:
    """Mock API client for testing device discovery and property maps.

    Uses correct EOJX class codes from eojx.py:
    - 0x30 = Home air conditioner (group 0x01)
    """

    def __init__(self):
        self._state = {
            "192.168.1.10": {
                "instances": {
                    # Group code: 0x01 = Air conditioner-related device group
                    1: {
                        # Class code: 0x30 = Home air conditioner (per eojx.py)
                        48: {
                            # Instance number: 0x01
                            1: {
                                # Property values
                                0x80: b"\x31",  # Operation status (off)
                                0xB0: b"\x42",  # Operational mode (cooling)
                                0xBB: b"\x20",  # Temperature setting
                                0xA0: b"\x34",  # Fan speed
                                0xA1: b"\x41",  # Auto direction
                                0xA3: b"\x41",  # Swing mode
                                0xA4: b"\x41",  # Airflow vertical
                                0xA5: b"\x41",  # Airflow horizontal
                                0xB2: b"\x41",  # Silent mode
                                # Property maps
                                0x9F: [0x80, 0xB0, 0xBB, 0xA0, 0xA3],  # GETMAP
                                0x9E: [0x80, 0xB0, 0xBB, 0xA0],  # SETMAP
                            }
                        }
                    },
                }
            }
        }

    async def echonetMessage(
        self, host, eojgc, eojcc, eojci, message_type, opc
    ):  # pylint: disable=unused-argument
        """Simulate successful ECHONET message response."""
        return True


class TestDeviceDiscovery(unittest.IsolatedAsyncioTestCase):
    """Test cases for device discovery and property map access.

    Uses correct EOJX class codes per eojx.py:
    - HomeAirConditioner: group=0x01 (1), class=0x30 (48) = "Home air conditioner"
    """

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.api = MockECHONETAPIClient()

    async def asyncSetUp(self):
        """Async setup before each test."""
        from pychonet.EchonetInstance import EchonetInstance

        # HomeAirConditioner: group=1 (0x01), class=48 (0x30) per eojx.py
        self.ac_instance = EchonetInstance(
            host="192.168.1.10", eojgc=1, eojcc=48, instance=1, api_connector=self.api
        )

    async def test_getGetProperties_returns_list(self):
        """Test that getGetProperties returns the GETMAP list correctly."""
        properties = self.ac_instance.getGetProperties()
        # Verify we get the expected property codes for HomeAirConditioner (class 0x30)
        self.assertEqual(properties, [0x80, 0xB0, 0xBB, 0xA0, 0xA3])

    async def test_getSetProperties_returns_list(self):
        """Test that getSetProperties returns the SETMAP list correctly."""
        properties = self.ac_instance.getSetProperties()
        # Verify we get writable property codes only for class 0x30
        self.assertEqual(properties, [0x80, 0xB0, 0xBB, 0xA0])


class TestPropertyAccess(unittest.IsolatedAsyncioTestCase):
    """Test cases for accessing device property values.

    Uses correct EOJX class codes: HomeAirConditioner (group=1, class=48).
    """

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.api = MockECHONETAPIClient()

    async def asyncSetUp(self):
        """Async setup before each test."""
        from pychonet.EchonetInstance import EchonetInstance

        # HomeAirConditioner: group=1 (0x01), class=48 (0x30) per eojx.py
        self.ac_instance = EchonetInstance(
            host="192.168.1.10", eojgc=1, eojcc=48, instance=1, api_connector=self.api
        )

    async def test_update_single_property_returns_value(self):
        """Test update with single EPC code returns formatted value."""
        result = await self.ac_instance.update(0x80)
        # 0x80 is operation status, should return 'off' from DICT_30_ON_OFF
        self.assertEqual(result, "off")

    async def test_update_multiple_properties_returns_dict(self):
        """Test update with multiple EPC codes returns dictionary."""
        result = await self.ac_instance.update([0x80, 0xB0])
        # Should return dict with both property values
        self.assertIsInstance(result, dict)
        self.assertIn(0x80, result)
        self.assertIn(0xB0, result)

    async def test_update_unknown_property_returns_none(self):
        """Test update for EPC code not in state returns None."""
        # 0xFF is not defined in our mock state
        result = await self.ac_instance.update(0xFF)
        self.assertIsNone(result)


class TestMockAPIClient(unittest.IsolatedAsyncioTestCase):
    """Unit tests for the mock API client used in testing.

    Verifies correct EOJX class code structure per eojx.py:
    - Group 1 (0x01), Class 48 (0x30) = Home air conditioner
    """

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.api = MockECHONETAPIClient()

    async def test_asyncMessage_returns_true_on_success(self):
        """Test that echonetMessage returns True on successful response."""
        result = await self.api.echonetMessage(
            "192.168.1.10", 1, 48, 1, "GET", [{"EPC": 0x80}]
        )
        self.assertTrue(result)

    async def test_state_structure_is_valid_home_ac(self):
        """Test that mock state has proper structure for HomeAirConditioner."""
        host_data = self.api._state["192.168.1.10"]
        instances = host_data["instances"]

        # Check HomeAirConditioner instance: group=1, class=48 (per eojx.py)
        ac_instance = instances[1][48][1]
        self.assertIn(0x9F, ac_instance)  # GETMAP
        self.assertIn(0x9E, ac_instance)  # SETMAP


if __name__ == "__main__":
    unittest.main()
