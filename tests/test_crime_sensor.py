# tests/test_crime_sensor.py
import unittest
from pychonet.CrimeSensor import CrimeSensor


class MockECHONETAPIClient:
    def __init__(self):
        # Raw byte values that simulate device responses
        # DICT_41_ON_OFF: 0x41='on', 0x42='off'
        # DICT_31_8_LEVELS: 0x31='level-1', 0x38='level-8'
        self._state = {
            "192.168.1.30": {
                "instances": {
                    0x00: {  # Class group code for crime sensor
                        0x02: {  # Class code for crime sensor
                            0x01: {
                                0x80: b'\x31',  # Operation status: OFF
                                0xB0: b'\x33',  # Detection threshold level: level-3
                                0xB1: b'\x42',  # Invasion occurrence status: not found
                                0xBF: b'\x00',  # Invasion status resetting: Reset
                                0x9F: [0x80, 0xB0, 0xB1],  # GETMAP
                                0x9E: [0x80, 0xB0],  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        # Simulate a successful response
        return True


class TestCrimeSensor(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = CrimeSensor("192.168.1.30", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b'\x31')  # OFF

        status = await sensor.update(0x80)
        expected = 'off'  # DICT_30_ON_OFF[0x31] = 'off' (lowercase from epc_functions)
        self.assertEqual(status, expected)

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = CrimeSensor("192.168.1.30", api_connector)

        result = await sensor.setOperationStatus('on')
        self.assertTrue(result)

    async def test_getDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = CrimeSensor("192.168.1.30", api_connector)

        level = await sensor.getDetectionThresholdLevel()
        self.assertEqual(level, b'\x33')  # level-3

        status = await sensor.update(0xB0)
        expected = 'level-3'  # DICT_31_8_LEVELS[0x33] = 'level-3'
        self.assertEqual(status, expected)

    async def test_setDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = CrimeSensor("192.168.1.30", api_connector)

        result = await sensor.setDetectionThresholdLevel('level-8')
        self.assertTrue(result)

    async def test_getInvasionOccurrenceStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = CrimeSensor("192.168.1.30", api_connector)

        status = await sensor.getInvasionOccurrenceStatus()
        self.assertEqual(status, b'\x42')  # not found
        status = await sensor.update(0xB1)
        expected = 'Invasion occurrence status not found'
        self.assertEqual(status, expected)

    async def test_resetInvasionOccurrenceStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = CrimeSensor("192.168.1.30", api_connector)

        result = await sensor.resetInvasionOccurrenceStatus()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()