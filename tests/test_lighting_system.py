"""Test lighting devices with ACTUAL EOJ codes from pychonet."""
import unittest
from unittest.mock import AsyncMock, patch
from pychonet import LightingSystem, GeneralLighting, SingleFunctionLighting


class MockLightingAPI:
    """Mock API for lighting device tests."""
    
    def __init__(self):
        self._state = {
            "192.168.1.200": {
                "instances": {
                    0x02: {  # ✅ Housing/facility group
                        0xA3: {  # ✅ Lighting System
                            0x01: {
                                0x80: b"\x30",  # Status: ON
                                0xB0: b"\x64",  # Brightness: 100%
                                0xC0: b"\x01",  # Scene: 1
                            },
                        },
                        0x90: {  # ✅ General Lighting
                            0x01: {
                                0x80: b"\x30",  # Status: ON
                                0xB0: b"\x64",  # Brightness: 100%
                                0xB1: b"\x65",  # Color: warm white
                            },
                        },
                        0x91: {  # ✅ Single Function Lighting
                            0x01: {
                                0x80: b"\x30",  # Status: ON
                                0xB0: b"\x64",  # Brightness: 100%
                            },
                        },
                    },
                }
            }
        }
    
    async def get(self, host, eojgc, eojcc, instance=0x1):
        if host in self._state:
            instances = self._state[host]["instances"]
            if eojgc in instances and eojcc in instances[eojgc]:
                return instances[eojgc][eojcc].get(f"{instance:02X}", b"\x00")
        return b"\x00"


class TestLightingSystem(unittest.TestCase):
    """Test LightingSystem class."""
    
    def setUp(self):
        self.mock_api = MockLightingAPI()
        self.lighting = LightingSystem("192.168.1.200", api_connector=self.mock_api)
    
    def test_init(self):
        """Test initialization with ACTUAL EOJ codes."""
        # ✅ CORRECT: Housing/facility group (0x02)
        self.assertEqual(self.lighting._eojgc, 0x02)
        # ✅ CORRECT: Lighting System class (0xA3)
        self.assertEqual(self.lighting._eojcc, 0xA3)


class TestGeneralLighting(unittest.TestCase):
    """Test GeneralLighting class."""
    
    def setUp(self):
        self.mock_api = MockLightingAPI()
        self.general = GeneralLighting("192.168.1.200", api_connector=self.mock_api)
    
    def test_init(self):
        """Test initialization with ACTUAL EOJ codes."""
        # ✅ CORRECT: Housing/facility group (0x02)
        self.assertEqual(self.general._eojgc, 0x02)
        # ✅ CORRECT: General Lighting class (0x90)
        self.assertEqual(self.general._eojcc, 0x90)


class TestSingleFunctionLighting(unittest.TestCase):
    """Test SingleFunctionLighting class."""
    
    def setUp(self):
        self.mock_api = MockLightingAPI()
        self.single = SingleFunctionLighting("192.168.1.200", api_connector=self.mock_api)
    
    def test_init(self):
        """Test initialization with ACTUAL EOJ codes."""
        # ✅ CORRECT: Housing/facility group (0x02)
        self.assertEqual(self.single._eojgc, 0x02)
        # ✅ CORRECT: Single Function Lighting class (0x91)
        self.assertEqual(self.single._eojcc, 0x91)


if __name__ == '__main__':
    unittest.main()
