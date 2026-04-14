# tests/test_current_sensor.py
import unittest
from pychonet.CurrentSensor import CurrentSensor


class MockECHONETAPIClient:
    def __init__(self):
        # Raw byte values that simulate device responses
        # DICT_30_ON_OFF: 0x30='on', 0x31='off'
        self._state = {
            "192.168.1.40": {
                "instances": {
                    0x00: {  # Class group code for current sensor
                        0x23: {  # Class code for current sensor
                            0x01: {
                                0x80: b'\x31',  # Operation status: OFF
                                0xE0: b'\x0a',  # Measured current value 1: 10 mA
                                0xE1: b'\x00',  # Rated voltage to be measured: 0V
                                0xE2: b'\x06',  # Measured current value 2: 6 mA
                                0x9F: [0x80, 0xE0, 0xE1, 0xE2],  # GETMAP
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


class TestCurrentSensor(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = CurrentSensor("192.168.1.40", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b'\x31')  # OFF

        status = await sensor.update(0x80)
        expected = 'off'  # DICT_30_ON_OFF[0x31] = 'off'
        self.assertEqual(status, expected)

    async def test_getMeasuredCurrentValue1(self):
        api_connector = MockECHONETAPIClient()
        sensor = CurrentSensor("192.168.1.40", api_connector)

        current = await sensor.getMeasuredCurrentValue1()
        # _int() returns int.from_bytes(edt, "big") for plain _int without dict
        self.assertEqual(current, b'\x0a')  # 10 mA

        current = await sensor.update(0xE0)
        expected = 10  # _int() returns the integer value
        self.assertEqual(current, expected)

    async def test_getRatedVoltage(self):
        api_connector = MockECHONETAPIClient()
        sensor = CurrentSensor("192.168.1.40", api_connector)

        voltage = await sensor.getRatedVoltage()
        # _int() returns the raw integer value (0V)
        self.assertEqual(voltage, b'\x00')  # 0V

        voltage = await sensor.update(0xE1)
        expected = 0  # _int() returns the integer value
        self.assertEqual(voltage, expected)

    async def test_getMeasuredCurrentValue2(self):
        api_connector = MockECHONETAPIClient()
        sensor = CurrentSensor("192.168.1.40", api_connector)

        current = await sensor.getMeasuredCurrentValue2()
        self.assertEqual(current, b'\x06')  # 6 mA

        current = await sensor.update(0xE2)
        expected = 6  # _int() returns the integer value
        self.assertEqual(current, expected)


if __name__ == '__main__':
    unittest.main()