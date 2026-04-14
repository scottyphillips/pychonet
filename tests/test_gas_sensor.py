# tests/test_gas_sensor.py
import unittest
from pychonet.GasSensor import GasSensor


class MockECHONETAPIClient:
    def __init__(self):
        # Raw byte values that simulate device responses
        # DICT_30_ON_OFF: 0x30='on', 0x31='off'
        # DICT_31_8_LEVELS: 0x31='level-1', 0x38='level-8'
        self._state = {
            "192.168.1.110": {
                "instances": {
                    0x00: {  # Class group code for gas sensor
                        0x1C: {  # Class code for gas sensor
                            0x01: {
                                0x80: b'\x31',  # Operation status: OFF
                                0xB0: b'\x35',  # Detection threshold level: level-5
                                0xB1: b'\x41',  # Gas detection status: found
                                0xE0: b'\x0d',  # Measured gas concentration: 13 ppm
                                0x9F: [0x80, 0xB0, 0xB1, 0xE0],  # GETMAP
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


class TestGasSensor(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = GasSensor("192.168.1.110", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b'\x31')  # OFF

        status = await sensor.update(0x80)
        expected = 'off'  # DICT_30_ON_OFF[0x31] = 'off'
        self.assertEqual(status, expected)

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = GasSensor("192.168.1.110", api_connector)

        result = await sensor.setOperationStatus('on')
        self.assertTrue(result)

    async def test_getDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = GasSensor("192.168.1.110", api_connector)

        level = await sensor.getDetectionThresholdLevel()
        self.assertEqual(level, b'\x35')  # level-5

        level = await sensor.update(0xB0)
        expected = 'level-5'  # DICT_31_8_LEVELS[0x35] = 'level-5'
        self.assertEqual(level, expected)

    async def test_setDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = GasSensor("192.168.1.110", api_connector)

        result = await sensor.setDetectionThresholdLevel('level-8')
        self.assertTrue(result)

    async def test_getGasDetectionStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = GasSensor("192.168.1.110", api_connector)

        status = await sensor.getGasDetectionStatus()
        self.assertEqual(status, b'\x41')  # found
        status = await sensor.update(0xB1)
        expected = 'found'  # {0x41: 'found', 0x42: 'not found'}
        self.assertEqual(status, expected)

    async def test_getGasConcentration(self):
        api_connector = MockECHONETAPIClient()
        sensor = GasSensor("192.168.1.110", api_connector)

        concentration = await sensor.getGasConcentration()
        self.assertEqual(concentration, b'\x0d')  # 13 ppm

        concentration = await sensor.update(0xE0)
        expected = 13  # _int() returns integer value
        self.assertEqual(concentration, expected)


if __name__ == '__main__':
    unittest.main()