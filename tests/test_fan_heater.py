# tests/test_fan_heater.py
import unittest
from unittest.mock import AsyncMock, patch
from pychonet.EchonetInstance import EchonetInstance
from pychonet.FanHeater import FanHeater

class MockECHONETAPIClient:
    def __init__(self):
        self._state = {
            "192.168.1.8": {
                "instances": {
                    0x01: {  # EoJGC (Class Group Code) for Fan Heater
                        0x43: {  # EoJCC (Class Code) for Fan Heater
                            0x01: {  # Instance code
                                0xB3: b'\x28',  # Temperature setting value: 0x28 = 40°C
                                0xBB: b'\x1A',  # Measured temperature: 0x1A = 26°C (signed)
                                0xB1: b'\x41',  # Automatic temperature control: 0x41 = 'auto'
                                0x90: b'\x41',  # On timer reservation: 0x41 = 'ON'
                                0x91: b'\x38\x60',  # On timer setting value: 0x3860 = 14:24
                                0x92: b'\x3C\x00',  # On timer relative time: 0x3C00 = 3584 min
                                0x94: b'\x42',  # Off timer reservation: 0x42 = 'OFF'
                                0x95: b'\x1F\x90',  # Off timer setting value: 0x1F90 = 8:16
                                0x96: b'\x3C\x00',  # Off timer relative time: 0x3C00 = 3584 min
                                0xC0: b'\x42',  # Extensional operation: 0x42 = 'OFF'
                                0xC1: b'\x1F\x90',  # Extensional timer time value: 0x1F90 = 8:16
                                0xC2: b'\x42',  # Ion emission: 0x42 = 'OFF'
                                0xC3: b'\x41',  # Implemented ion method: 0x41 = negative ion mounting
                                0xC4: b'\x43',  # Oil amount level: 0x43 = 'Middium'
                                0x9F: [0xB1, 0xB3, 0xBB, 0x90, 0x91, 0x92, 0x94, 0x95, 0x96, 0xC0, 0xC1, 0xC2, 0xC3, 0xC4],  # GETMAP
                                0x9E: [0xB1, 0xB3, 0x90, 0x91, 0x92, 0x94, 0x95, 0x96, 0xC0, 0xC1, 0xC2],  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        # Simulate a successful response
        return True

    def _state(self, host):
        return self._state[host]


class TestFanHeater(unittest.IsolatedAsyncioTestCase):
    async def test_getTemperatureSettingValue(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        temp_value = await heater.getTemperatureSettingValue()
        self.assertEqual(temp_value, b'\x28')  # 40°C

        status = await heater.update(0xB3)
        expected = 40
        self.assertEqual(status, expected)

    async def test_setTemperatureSettingValue(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        # Test setting temperature to 35°C (0x23)
        result = await heater.setTemperatureSettingValue(35)
        self.assertTrue(result)

    async def test_getMeasuredTemperature(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        measured_temp = await heater.getMeasuredTemperature()
        self.assertEqual(measured_temp, b'\x1A')  # 26°C (signed)

        status = await heater.update(0xBB)
        expected = 26
        self.assertEqual(status, expected)

    async def test_getAutomaticTemperatureControlSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        auto_setting = await heater.getAutomaticTemperatureControlSetting()
        self.assertEqual(auto_setting, b'\x41')  # 'auto'

        status = await heater.update(0xB1)
        expected = 'auto'
        self.assertEqual(status, expected)

    async def test_setAutomaticTemperatureControlSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        # Test setting to non-auto (0x42)
        result = await heater.setAutomaticTemperatureControlSetting(0x42)
        self.assertTrue(result)

    async def test_getOnTimerReservationSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        on_timer = await heater.getOnTimerReservationSetting()
        self.assertEqual(on_timer, b'\x41')  # 'ON'

    async def test_setOnTimerReservationSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        # Test setting to OFF (0x42)
        result = await heater.setOnTimerReservationSetting(0x42)
        self.assertTrue(result)

    async def test_getOnTimerSettingValue(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        on_time = await heater.getOnTimerSettingValue()
        self.assertEqual(on_time, b'\x38\x60')  # 14:24

    async def test_setOnTimerSettingValue(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        # Test setting time value
        result = await heater.setOnTimerSettingValue(0x3860)  # 14:24
        self.assertTrue(result)

    async def test_getOnTimerSettingRelativeTime(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        on_relative_time = await heater.getOnTimerSettingRelativeTime()
        self.assertEqual(on_relative_time, b'\x3C\x00')  # 3584 min

    async def test_setOnTimerSettingRelativeTime(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        # Test setting relative time value
        result = await heater.setOnTimerSettingRelativeTime(3584)
        self.assertTrue(result)

    async def test_getOffTimerReservationSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        off_timer = await heater.getOffTimerReservationSetting()
        self.assertEqual(off_timer, b'\x42')  # 'OFF'

    async def test_setOffTimerReservationSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        # Test setting to ON (0x41)
        result = await heater.setOffTimerReservationSetting(0x41)
        self.assertTrue(result)

    async def test_getOffTimerSettingValue(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        off_time = await heater.getOffTimerSettingValue()
        self.assertEqual(off_time, b'\x1F\x90')  # 8:16

    async def test_setOffTimerSettingValue(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        # Test setting time value
        result = await heater.setOffTimerSettingValue(0x1F90)  # 8:16
        self.assertTrue(result)

    async def test_getOffTimerSettingRelativeTime(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        off_relative_time = await heater.getOffTimerSettingRelativeTime()
        self.assertEqual(off_relative_time, b'\x3C\x00')  # 3584 min

    async def test_setOffTimerSettingRelativeTime(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        # Test setting relative time value
        result = await heater.setOffTimerSettingRelativeTime(3584)
        self.assertTrue(result)

    async def test_getExtensionalOperationSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        ext_op = await heater.getExtensionalOperationSetting()
        self.assertEqual(ext_op, b'\x42')  # 'OFF'

    async def test_setExtensionalOperationSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        # Test setting to ON (0x41)
        result = await heater.setExtensionalOperationSetting(0x41)
        self.assertTrue(result)

    async def test_getExtensionalOperationTimerTimeSettingValue(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        ext_timer_time = await heater.getExtensionalOperationTimerTimeSettingValue()
        self.assertEqual(ext_timer_time, b'\x1F\x90')  # 8:16

    async def test_setExtensionalOperationTimerTimeSettingValue(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        # Test setting time value
        result = await heater.setExtensionalOperationTimerTimeSettingValue(0x1F90)  # 8:16
        self.assertTrue(result)

    async def test_getIonEmissionSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        ion_setting = await heater.getIonEmissionSetting()
        self.assertEqual(ion_setting, b'\x42')  # 'OFF'

    async def test_setIonEmissionSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        # Test setting to ON (0x41)
        result = await heater.setIonEmissionSetting(0x41)
        self.assertTrue(result)

    async def test_getImplementedIonEmissionMethod(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        ion_method = await heater.getImplementedIonEmissionMethod()
        self.assertEqual(ion_method, b'\x41')  # negative ion mounting

    async def test_getOilAmountLevel(self):
        api_connector = MockECHONETAPIClient()
        heater = FanHeater("192.168.1.8", api_connector)

        oil_level = await heater.getOilAmountLevel()
        self.assertEqual(oil_level, b'\x43')  # 'Middium'


if __name__ == '__main__':
    unittest.main()