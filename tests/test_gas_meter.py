"""Unit tests for GasMeter ECHONET device class."""
import unittest
from pychonet.GasMeter import GasMeter


class MockECHONETAPIClient:
    """Mock API client for testing GasMeter functionality.

    Uses EOJX codes: group=0x02, class=0x82 (Gas meter)
    EPCs include cumulative consumption and measurement logs
    """

    def __init__(self):
        self._state = {
            "192.168.1.90": {
                "instances": {
                    0x02: {  # EoJGC (Class Group Code) for Gas Meter
                        0x82: {  # EoJCC (Class Code) for Gas Meter
                            0x01: {  # Instance code
                                0xE0: b"\x00\x00\x01\x2A",  # Cumulative amount of gas consumption (300 liters)
                                0xE2: b"\x00\x00\x00\x64",  # Measurement log (100 units)
                                0x9F: [0xE0, 0xE2],  # GETMAP
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


class TestGasMeter(unittest.IsolatedAsyncioTestCase):
    """Test cases for GasMeter device class.

    Uses EOJX codes: group=0x02, class=0x82 (Gas meter)
    """

    async def test_getCumulativeConsumption(self):
        """Test getCumulativePower returns correct value."""
        api_connector = MockECHONETAPIClient()
        meter = GasMeter("192.168.1.90", api_connector)

        consumption = await meter.update(0xE0)
        self.assertEqual(consumption, 298)

    async def test_getMeasurementLog(self):
        """Test getMeasurementLog returns correct value."""
        api_connector = MockECHONETAPIClient()
        meter = GasMeter("192.168.1.90", api_connector)

        log = await meter.update(0xE2)
        self.assertEqual(log, [100])  # Assuming the log returns a list of measurements


if __name__ == "__main__":
    unittest.main()
