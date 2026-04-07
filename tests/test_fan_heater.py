# tests/test_fan_heater.py
import unittest
from pychonet.FanHeater import FanHeater


class MockECHONETAPIClient:
    def __init__(self):
        # Raw byte values that simulate device responses
        # DICT_41_AUTO_NONAUTO: 0x41='auto', 0x42='non-auto'
        # DICT_41_ON_OFF: 0x41='on', 0x42='off'
        self._state = {
            "192.168.1.100": {
                "instances": {
                    0x01: {  # Class group code for fan heater
                        0x43: {  # Class code for fan heater
                            0x01: {
                                0xB3: b'\x01',  # Temperature setting: 1°C
                                0xBB: b'\x31',  # Measured temperature: 49°C (signed int returns 49)
                                0xB1: b'\x41',  # Automatic temperature control: auto
                                0x90: b'\x41',  # On timer reservation: ON
                                0x91: b'\x05\x00',  # On timer setting: 5:00
                                0x92: b'\x00\x00',  # On timer relative time: 0:00
                                0x94: b'\x42',  # Off timer reservation: OFF
                                0x95: b'\x10\x00',  # Off timer setting: 16:00
                                0x96: b'\x03\x00',  # Off timer relative time: 3:00
                                0xC0: b'\x41',  # Extensional operation: ON
                                0xC1: b'\x31',  # Extensional timer: 1:00
                                0xC2: b'\x42',  # Ion emission: OFF
                                0xC4: b'\x42',  # Ion emission level: Low
                                0x9F: list(range(0xB1, 0xC5, 0x01)),  # GETMAP
                                0x9E: [0xB3, 0xB1, 0x90, 0x94, 0xC0],  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        # Simulate a successful response
        return True


class TestFanHeater(unittest.IsolatedAsyncioTestCase):
    async def test_getTemperatureSettingValue(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.100", api_connector)

        temp = await heater.getTemperatureSettingValue()
        self.assertEqual(temp, b'\x01')  # 1°C

        temp = await heater.update(0xB3)
        expected = 1  # _int() returns integer value
        self.assertEqual(temp, expected)

    async def test_setTemperatureSettingValue(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.100", api_connector)

        result = await heater.setTemperatureSettingValue(26)
        self.assertTrue(result)

    async def test_getMeasuredTemperature(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.100", api_connector)

        temp = await heater.getMeasuredTemperature()
        self.assertEqual(temp, b'\x31')  # 49°C (0x31)

        temp = await heater.update(0xBB)
        expected = 49  # _signed_int() returns 49 (not negative because 0x31 fits in signed int)
        self.assertEqual(temp, expected)

    async def test_getAutomaticTemperatureControlSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.100", api_connector)

        setting = await heater.getAutomaticTemperatureControlSetting()
        self.assertEqual(setting, b'\x41')  # auto

        setting = await heater.update(0xB1)
        expected = 'auto'  # DICT_41_AUTO_NONAUTO[0x41] = 'auto'
        self.assertEqual(setting, expected)

    async def test_setAutomaticTemperatureControlSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.100", api_connector)

        result = await heater.setAutomaticTemperatureControlSetting('non-auto')
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()