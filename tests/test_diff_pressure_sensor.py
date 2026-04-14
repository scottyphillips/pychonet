# tests/test_diff_pressure_sensor.py
import unittest
from pychonet.DiffPressureSensor import DiffPressureSensor


class MockECHONETAPIClient:
    def __init__(self):
        self._state = {
            "192.168.1.170": {
                "instances": {
                    0x00: {
                        0x1E: {
                            0x01: {
                                0x80: b'\x31',  # Operation status: OFF
                                0xE0: b'\x64',  # Measured differential pressure: 100 Pa
                                0x9F: [0x80, 0xE0],  # GETMAP
                                0x9E: [0x80],  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        return True


class TestDiffPressureSensor(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = DiffPressureSensor("192.168.1.170", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b'\x31')  # OFF

        status = await sensor.update(0x80)
        expected = 'off'  # DICT_30_ON_OFF[0x31] = 'off'
        self.assertEqual(status, expected)

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = DiffPressureSensor("192.168.1.170", api_connector)

        result = await sensor.setOperationStatus('on')
        self.assertTrue(result)

    async def test_getDifferentialPressure(self):
        api_connector = MockECHONETAPIClient()
        sensor = DiffPressureSensor("192.168.1.170", api_connector)

        pressure = await sensor.getDifferentialPressure()
        self.assertEqual(pressure, b'\x64')  # 100 Pa

        pressure = await sensor.update(0xE0)
        expected = 100  # _int() returns integer value
        self.assertEqual(pressure, expected)


if __name__ == '__main__':
    unittest.main()