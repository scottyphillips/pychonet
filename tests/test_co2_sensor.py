# tests/test_co2_sensor.py
import unittest
from pychonet.CO2Sensor import CO2Sensor


class MockECHONETAPIClient:
    def __init__(self):
        # Raw byte values that simulate device responses
        # DICT_30_ON_OFF returns lowercase: {0x30: 'on', 0x31: 'off'}
        self._state = {
            "192.168.1.90": {
                "instances": {
                    0x00: {  # Class group code for CO2 sensor
                        0x1B: {  # Class code for CO2 sensor
                            0x01: {
                                0x80: b'\x31',  # Operation status: OFF
                                0xE0: b'\x0d',  # Measured CO2 concentration: 13 ppm
                                0x9F: [0x80, 0xE0],  # GETMAP
                                0x9E: [0x80],  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        # Simulate a successful response
        return True


class TestCO2Sensor(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = CO2Sensor("192.168.1.90", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b'\x31')  # OFF

        status = await sensor.update(0x80)
        expected = 'off'  # DICT_30_ON_OFF[0x31] = 'off' (lowercase from epc_functions)
        self.assertEqual(status, expected)

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = CO2Sensor("192.168.1.90", api_connector)

        result = await sensor.setOperationStatus('on')
        self.assertTrue(result)

    async def test_getCO2Concentration(self):
        api_connector = MockECHONETAPIClient()
        sensor = CO2Sensor("192.168.1.90", api_connector)

        concentration = await sensor.getCO2Concentration()
        self.assertEqual(concentration, b'\x0d')  # 13 ppm

        concentration = await sensor.update(0xE0)
        expected = 13  # _int() returns integer value
        self.assertEqual(concentration, expected)


if __name__ == '__main__':
    unittest.main()