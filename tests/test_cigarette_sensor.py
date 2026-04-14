# tests/test_cigarette_sensor.py
import unittest
from pychonet.CigaretteSensor import CigaretteSensor


class MockECHONETAPIClient:
    def __init__(self):
        # Note: CigaretteSensor EPC_FUNCTIONS uses custom dict {0x30: 'ON', 0x31: 'OFF'}
        # But update() uses DICT_30_ON_OFF which returns lowercase values
        self._state = {
            "192.168.1.130": {
                "instances": {
                    0x00: {
                        0x05: {
                            0x01: {
                                0x80: b'\x31',  # Operation status: OFF
                                0xB0: b'\x35',  # Detection threshold level: level-5
                                0xB1: b'\x42',  # Smoke detection status: not found
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


class TestCigaretteSensor(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = CigaretteSensor("192.168.1.130", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b'\x31')  # OFF

        status = await sensor.update(0x80)
        expected = 'off'  # DICT_30_ON_OFF[0x31] returns lowercase
        self.assertEqual(status, expected)

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = CigaretteSensor("192.168.1.130", api_connector)

        result = await sensor.setOperationStatus('on')
        self.assertTrue(result)

    async def test_getDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = CigaretteSensor("192.168.1.130", api_connector)

        level = await sensor.getDetectionThresholdLevel()
        self.assertEqual(level, b'\x35')  # level-5

        level = await sensor.update(0xB0)
        expected = 'level-5'  # DICT_31_8_LEVELS[0x35] = 'level-5'
        self.assertEqual(level, expected)

    async def test_setDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = CigaretteSensor("192.168.1.130", api_connector)

        result = await sensor.setDetectionThresholdLevel('level-8')
        self.assertTrue(result)

    async def test_getSmokeDetectionStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = CigaretteSensor("192.168.1.130", api_connector)

        status = await sensor.getSmokeDetectionStatus()
        self.assertEqual(status, b'\x42')  # not found
        status = await sensor.update(0xB1)
        expected = 'Smoke (cigarette) detection status not found'
        self.assertEqual(status, expected)


if __name__ == '__main__':
    unittest.main()