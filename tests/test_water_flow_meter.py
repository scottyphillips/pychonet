"""Unit tests for WaterFlowMeter ECHONET device class."""
import unittest
from pychonet.WaterFlowMeter import WaterFlowMeter


class MockECHONETAPIClient:
    """Mock API client for testing WaterFlowMeter functionality.

    Uses EOJX codes: group=0x02, class=0x81 (Water Flow Meter)
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    def __init__(self):
        self._state = {
            "192.168.1.50": {
                "instances": {
                    0x02: {  # EoJGC (Class Group Code) for Water meter-related device
                        0x81: {  # EoJCC (Class Code) for Water Flow Meter
                            0x01: {  # Instance code
                                0xD0: b"\x30",   # Water flow meter classification: Running Water
                                0xD1: b"\x31",   # Owner classification: Public waterworks company
                                0xE0: b"\x00\x01\x86\xA0",  # Measured cumulative amount (100,000)
                                0xE1: b"\x00",    # Unit: 1 cm³
                                0xE5: b"WM001234",  # ID number setting
                                0xF9: [0xD0, 0xD1, 0xE0, 0xE1, 0xE5],  # GETMAP
                                0xFA: [],  # SETMAP
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


class TestWaterFlowMeter(unittest.IsolatedAsyncioTestCase):
    """Test cases for WaterFlowMeter device class.

    Uses EOJX codes: group=0x02, class=0x81 (Water Flow Meter)
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    async def test_get_water_flow_meter_classification_returns_bytes(self):
        """Test get_water_flow_meter_classification returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        meter = WaterFlowMeter("192.168.1.50", api_connector)

        classification = await meter.getWaterFlowMeterClassification()
        self.assertEqual(classification, b"\x30")  # Running Water (raw bytes)

    async def test_get_owner_classification_returns_bytes(self):
        """Test getOwnerClassification returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        meter = WaterFlowMeter("192.168.1.50", api_connector)

        owner = await meter.getOwnerClassification()
        self.assertEqual(owner, b"\x31")  # Public waterworks company (raw bytes)

    async def test_get_measured_cumulative_amount_returns_bytes(self):
        """Test get_measured_cumulative_amount returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        meter = WaterFlowMeter("192.168.1.50", api_connector)

        amount = await meter.getMeasuredCumulativeAmount()
        self.assertEqual(amount, b"\x00\x01\x86\xA0")  # 100,000 (raw bytes)

    async def test_get_unit_returns_bytes(self):
        """Test get_unit returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        meter = WaterFlowMeter("192.168.1.50", api_connector)

        unit = await meter.getUnit()
        self.assertEqual(unit, b"\x00")  # Unit: 1 cm³ (raw bytes)


if __name__ == "__main__":
    unittest.main()
