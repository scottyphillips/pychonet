# tests/test_emergency_button.py
import unittest
from pychonet.EmergencyButton import EmergencyButton


class MockECHONETAPIClient:
    def __init__(self):
        self._state = {
            "192.168.1.150": {
                "instances": {
                    0x00: {
                        0x03: {
                            0x01: {
                                0x80: b'\x31',  # Operation status: OFF
                                0xB1: b'\x41',  # Emergency occurrence status: Found
                                0xBF: b'\x00',  # Emergency status resetting: Reset
                                0x9F: [0x80, 0xB1],  # GETMAP
                                0x9E: [0x80],  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        return True


class TestEmergencyButton(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        button = EmergencyButton("192.168.1.150", api_connector)

        status = await button.getOperationStatus()
        self.assertEqual(status, b'\x31')  # OFF

        status = await button.update(0x80)
        expected = 'off'  # DICT_30_ON_OFF[0x31] = 'off'
        self.assertEqual(status, expected)

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        button = EmergencyButton("192.168.1.150", api_connector)

        result = await button.setOperationStatus('on')
        self.assertTrue(result)

    async def test_getEmergencyOccurrenceStatus(self):
        api_connector = MockECHONETAPIClient()
        button = EmergencyButton("192.168.1.150", api_connector)

        status = await button.getEmergencyOccurrenceStatus()
        self.assertEqual(status, b'\x41')  # Found
        status = await button.update(0xB1)
        expected = 'Found'
        self.assertEqual(status, expected)

    async def test_resetEmergencyOccurrenceStatus(self):
        api_connector = MockECHONETAPIClient()
        button = EmergencyButton("192.168.1.150", api_connector)

        result = await button.resetEmergencyOccurrenceStatus()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()