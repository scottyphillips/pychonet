"""Unit tests for WaterFlowSensor ECHONET device class."""
import unittest
from pychonet.WaterFlowSensor import WaterFlowSensor


class MockECHONETAPIClient:
    """Mock API client for testing WaterFlowSensor functionality.

    Uses EOJX codes: group=0x00, class=0x25 (Water Flow Sensor)
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    def __init__(self):
        self._state = {
            "192.168.1.50": {
                "instances": {
                    0x00: {  # EoJGC (Class Group Code) for Water flow sensor-related device
                        0x25: {  # EoJCC (Class Code) for Water Flow Sensor
                            0x01: {  # Instance code
                                0x80: b"\x30",   # Operation status: on
                                0xE0: b"\x00\x6C\xE2\x00",  # Cumulative flow rate (115,763,200 cm³)
                                0xE2: b"\x00\x01\xF4",  # Flow rate (500 cm³/min)
                                0xF9: [0x80, 0xE0, 0xE2],  # GETMAP
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


class TestWaterFlowSensor(unittest.IsolatedAsyncioTestCase):
    """Test cases for WaterFlowSensor device class.

    Uses EOJX codes: group=0x00, class=0x25 (Water Flow Sensor)
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    async def test_get_operation_status_returns_bytes(self):
        """Test getOperationStatus returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        sensor = WaterFlowSensor("192.168.1.50", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b"\x30")  # on (raw bytes)

    async def test_get_cumulative_flow_rate_returns_bytes(self):
        """Test get_cumulative_flow_rate returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        sensor = WaterFlowSensor("192.168.1.50", api_connector)

        flow = await sensor.get_cumulative_flow_rate()
        self.assertEqual(flow, b"\x00\x6C\xE2\x00")  # cumulative flow (raw bytes)

    async def test_get_flow_rate_returns_bytes(self):
        """Test get_flow_rate returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        sensor = WaterFlowSensor("192.168.1.50", api_connector)

        rate = await sensor.get_flow_rate()
        self.assertEqual(rate, b"\x00\x01\xF4")  # flow rate (raw bytes)


if __name__ == "__main__":
    unittest.main()
