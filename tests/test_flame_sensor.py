# tests/test_flame_sensor.py
import unittest
from pychonet.FlameSensor import FlameSensor


class MockECHONETAPIClient:
    def __init__(self):
        self._state = {
            "192.168.1.180": {
                "instances": {
                    0x00: {
                        0x21: {
                            0x01: {
                                0x80: b'\x31',  # Operation status: OFF
                                0xB0: b'\x35',  # Detection threshold level: level-5
                                0xB1: b'\x42',  # Flame detection status: not found
                                0xBF: b'\x00',  # Flame detection status resetting: reset
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


class TestFlameSensor(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = FlameSensor("192.168.1.180", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b'\x31')  # OFF

        status = await sensor.update(0x80)
        expected = 'off'  # DICT_30_ON_OFF[0x31] = 'off'
        self.assertEqual(status, expected)

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = FlameSensor("192.168.1.180", api_connector)

        result = await sensor.setOperationStatus('on')
        self.assertTrue(result)

    async def test_getDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = FlameSensor("192.168.1.180", api_connector)

        level = await sensor.getDetectionThresholdLevel()
        self.assertEqual(level, b'\x35')  # level-5

        level = await sensor.update(0xB0)
        expected = 'level-5'  # DICT_31_8_LEVELS[0x35] = 'level-5'
        self.assertEqual(level, expected)

    async def test_setDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = FlameSensor("192.168.1.180", api_connector)

        result = await sensor.setDetectionThresholdLevel('level-8')
        self.assertTrue(result)

    async def test_getFlameDetectionStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = FlameSensor("192.168.1.180", api_connector)

        status = await sensor.getFlameDetectionStatus()
        self.assertEqual(status, b'\x42')  # not found
        status = await sensor.update(0xB1)
        expected = 'not found'
        self.assertEqual(status, expected)

    async def test_resetFlameDetectionStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = FlameSensor("192.168.1.180", api_connector)

        result = await sensor.resetFlameDetectionStatus()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()