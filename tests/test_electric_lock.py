import asyncio
import unittest
from pychonet.ElectricLock import ElectricLock


class MockECHONETAPIClient:
    """Mock ECHONET API client for testing."""

    def __init__(self):
        self._state = {
            "192.168.1.50": {
                "instances": {
                    0x02: {  # EoJGC (Class Group Code) for Electric Lock
                        0x6F: {  # EoJCC (Class Code) for Electric Lock
                            0x01: {  # Instance code
                                0xE1: b'\x43',  # Lock one status: 0x43 = 'unlocked'
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        return True


class TestElectricLock(unittest.IsolatedAsyncioTestCase):
    """Test suite for ElectricLock class."""

    async def asyncSetUp(self):
        self.api_connector = MockECHONETAPIClient()
        self.lock = ElectricLock("192.168.1.50", self.api_connector)

    async def test_get_lock_one_status_returns_bytes(self):
        """Test getLockOneStatus returns raw bytes."""
        status = await self.lock.getLockOneStatus()
        self.assertEqual(status, b'\x43')  # 'unlocked'


if __name__ == '__main__':
    asyncio.run(unittest.main())
