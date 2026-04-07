# tests/test_first_aid_sensor.py
import unittest
from pychonet.FirstAidSensor import FirstAidSensor


class MockECHONETAPIClient:
    def __init__(self):
        self._state = {
            "192.168.1.140": {
                "instances": {
                    0x00: {
                        0x04: {
                            0x01: {
                                0x80: b'\x31',  # Operation status: OFF
                                0xB0: b'\x33',  # Detection threshold level: level-3
                                0xB1: b'\x42',  # First-aid occurrence status: not found
                                0xBF: b'\x00',  # First-aid occurrence status resetting: Reset
                                0x9F: [0x80, 0xB0, 0xB1],  # GETMAP
                                0x9E: [0x80, 0xB0],  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        return True


class TestFirstAidSensor(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = FirstAidSensor("192.168.1.140", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b'\x31')  # OFF

        status = await sensor.update(0x80)
        expected = 'off'  # DICT_30_ON_OFF[0x31] = 'off'
        self.assertEqual(status, expected)

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = FirstAidSensor("192.168.1.140", api_connector)

        result = await sensor.setOperationStatus('on')
        self.assertTrue(result)

    async def test_getDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = FirstAidSensor("192.168.1.140", api_connector)

        level = await sensor.getDetectionThresholdLevel()
        self.assertEqual(level, b'\x33')  # level-3

        level = await sensor.update(0xB0)
        expected = 'level-3'  # DICT_31_8_LEVELS[0x33] = 'level-3'
        self.assertEqual(level, expected)

    async def test_setDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = FirstAidSensor("192.168.1.140", api_connector)

        result = await sensor.setDetectionThresholdLevel('level-8')
        self.assertTrue(result)

    async def test_getFirstAidOccurrenceStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = FirstAidSensor("192.168.1.140", api_connector)

        status = await sensor.getFirstAidOccurrenceStatus()
        self.assertEqual(status, b'\x42')  # not found
        status = await sensor.update(0xB1)
        expected = 'First-aid occurrence status not found'
        self.assertEqual(status, expected)

    async def test_resetFirstAidOccurrenceStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = FirstAidSensor("192.168.1.140", api_connector)

        result = await sensor.resetFirstAidOccurrenceStatus()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()