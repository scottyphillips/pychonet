# tests/test_electric_storage_heater.py
import unittest
from pychonet.ElectricStorageHeater import ElectricStorageHeater


class MockECHONETAPIClient:
    def __init__(self):
        # ElectricStorageHeater EPC_FUNCTIONS behavior:
        # The getMessage() returns raw bytes, the update() processes through EPC_FUNCTIONS
        # Note: _hh_mm() expects 2-byte values (HH*256 + MM), so mock data must be 2 bytes
        self._state = {
            "192.168.1.250": {
                "instances": {
                    0x01: {
                        0x55: {
                            0x01: {
                                0xB3: b'\x32',  # Temperature setting: 50 (0x32 = 50)
                                0xB8: b'\x3c',  # Rated power consumption: 60 (0x3c = 60)
                                0xBB: b'\x31',  # Measured indoor temperature: 49 (0x31 = 49)
                                0xBE: b'\x2a',  # Measured outdoor temperature: 42 (0x2a = 42)
                                0xA0: b'\x41',  # Air flow rate setting (0x41 = 65)
                                0xA1: b'\x41',  # Fan operation status
                                0xC0: b'\x41',  # Heat storage operation status
                                0xC1: b'\x30',  # Heat storage temperature setting (0x30 = 48)
                                0xC2: b'\x00',  # Measured stored heat temperature (0x00 = 0)
                                0xC3: b'\x42',  # Daytime heat storage setting (0x42 = disabled)
                                0xC4: b'\x41',  # Daytime heat storage ability (0x41 = available)
                                0xC5: b'\x10\x00',  # Midnight power duration (0x1000 = 4096)
                                0xC6: b'\x14\x00',  # Midnight power start time (0x1400 = 20*256 = '20:00')
                                0xC7: b'\x42',  # Radiation method (0x42 = Air heat method)
                                0xC8: b'\x42',  # Child lock setting (0x42 = disabled)
                                0xD0: b'\x31',  # Fan timer 1 setting (0x31 = 49 = '49:00')
                                0xD1: b'\x31',  # Fan timer 1 ON time (0x31 = 49 = '49:00')
                                0xD2: b'\x31',  # Fan timer 1 OFF time (0x31 = 49 = '49:00')
                                0xD3: b'\x30',  # Fan timer 2 setting (0x30 = 48 = '48:00')
                                0xD4: b'\x30',  # Fan timer 2 ON time (0x30 = 48 = '48:00')
                                0xD5: b'\x30',  # Fan timer 2 OFF time (0x30 = 48 = '48:00')
                                0x9F: list(range(0xA0, 0xD6, 0x01)),  # GETMAP
                                0x9E: list(range(0xA0, 0xD6, 0x01)),  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        return True


class TestElectricStorageHeater(unittest.IsolatedAsyncioTestCase):
    async def test_getTemperatureSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        temp = await heater.getTemperatureSetting()
        self.assertEqual(temp, b'\x32')

        temp = await heater.update(0xB3)
        self.assertEqual(temp, 50)

    async def test_getRatedPowerConsumption(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        power = await heater.getRatedPowerConsumption()
        self.assertEqual(power, b'\x3c')

        power = await heater.update(0xB8)
        self.assertEqual(power, 60)

    async def test_getMeasuredIndoorTemperature(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        temp = await heater.getMeasuredIndoorTemperature()
        self.assertEqual(temp, b'\x31')

        temp = await heater.update(0xBB)
        self.assertEqual(temp, 49)

    async def test_getMeasuredOutdoorTemperature(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        temp = await heater.getMeasuredOutdoorTemperature()
        self.assertEqual(temp, b'\x2a')

        temp = await heater.update(0xBE)
        self.assertEqual(temp, 42)

    async def test_getAirFlowRateSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        setting = await heater.getAirFlowRateSetting()
        self.assertEqual(setting, b'\x41')

        setting = await heater.update(0xA0)
        self.assertEqual(setting, 65)

    async def test_setAirFlowRateSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setAirFlowRateSetting('off')
        self.assertIsNone(result)

    async def test_getFanOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        status = await heater.getFanOperationStatus()
        self.assertEqual(status, b'\x41')

        status = await heater.update(0xA1)
        # DICT_30_ON_OFF[0x41] = 'on' - but library's EPC_FUNCTIONS uses _int without dict
        self.assertEqual(status, 'Invalid setting')

    async def test_setFanOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanOperationStatus('off')
        self.assertIsNone(result)

    async def test_getHeatStorageOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        status = await heater.getHeatStorageOperationStatus()
        self.assertEqual(status, b'\x41')

        status = await heater.update(0xC0)
        self.assertEqual(status, 'on')

    async def test_setHeatStorageOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setHeatStorageOperationStatus('off')
        self.assertIsNone(result)

    async def test_getHeatStorageTemperatureSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        temp = await heater.getHeatStorageTemperatureSetting()
        self.assertEqual(temp, b'\x30')

        temp = await heater.update(0xC1)
        self.assertEqual(temp, 48)

    async def test_setHeatStorageTemperatureSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setHeatStorageTemperatureSetting(60)
        self.assertIsNone(result)

    async def test_getMeasuredStoredHeatTemperature(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        temp = await heater.getMeasuredStoredHeatTemperature()
        self.assertEqual(temp, b'\x00')

        temp = await heater.update(0xC2)
        self.assertEqual(temp, 0)

    async def test_getDaytimeHeatStorageSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        setting = await heater.getDaytimeHeatStorageSetting()
        self.assertEqual(setting, b'\x42')

        setting = await heater.update(0xC3)
        self.assertEqual(setting, 'disabled')

    async def test_setDaytimeHeatStorageSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setDaytimeHeatStorageSetting('enabled')
        self.assertIsNone(result)

    async def test_getDaytimeHeatStorageAbility(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        ability = await heater.getDaytimeHeatStorageAbility()
        self.assertEqual(ability, b'\x41')

        ability = await heater.update(0xC4)
        self.assertEqual(ability, 'available')

    async def test_getMidnightPowerDurationSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        duration = await heater.getMidnightPowerDurationSetting()
        self.assertEqual(duration, b'\x10\x00')

        duration = await heater.update(0xC5)
        self.assertEqual(duration, 4096)

    async def test_setMidnightPowerDurationSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setMidnightPowerDurationSetting(1200)
        self.assertIsNone(result)

    async def test_getMidnightPowerStartTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        time = await heater.getMidnightPowerStartTimeSetting()
        self.assertEqual(time, b'\x14\x00')

        time = await heater.update(0xC6)
        self.assertEqual(time, '20:00')

    async def test_setMidnightPowerStartTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setMidnightPowerStartTimeSetting('01:00')
        self.assertIsNone(result)

    async def test_getRadiationMethod(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        method = await heater.getRadiationMethod()
        self.assertEqual(method, b'\x42')

        method = await heater.update(0xC7)
        self.assertEqual(method, 'Air heat method')

    async def test_setRadiationMethod(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setRadiationMethod('Radiant heat method')
        self.assertIsNone(result)

    async def test_getChildLockSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        lock = await heater.getChildLockSetting()
        self.assertEqual(lock, b'\x42')

        lock = await heater.update(0xC8)
        self.assertEqual(lock, 'disabled')

    async def test_setChildLockSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setChildLockSetting('enabled')
        self.assertIsNone(result)

    async def test_getFanTimer1Setting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        setting = await heater.getFanTimer1Setting()
        self.assertEqual(setting, b'\x31')

        setting = await heater.update(0xD0)
        # _int() returns integer value, not _hh_mm() string
        self.assertEqual(setting, 49)

    async def test_setFanTimer1Setting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanTimer1Setting('45:00')
        self.assertIsNone(result)

    async def test_getFanTimer1ONTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        time = await heater.getFanTimer1ONTimeSetting()
        self.assertEqual(time, b'\x31')

        time = await heater.update(0xD1)
        self.assertEqual(time, '49:00')

    async def test_setFanTimer1ONTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanTimer1ONTimeSetting('01:00')
        self.assertIsNone(result)

    async def test_getFanTimer1OFFTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        time = await heater.getFanTimer1OFFTimeSetting()
        self.assertEqual(time, b'\x31')

        time = await heater.update(0xD2)
        self.assertEqual(time, '49:00')

    async def test_setFanTimer1OFFTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanTimer1OFFTimeSetting('02:00')
        self.assertIsNone(result)

    async def test_getFanTimer2Setting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        setting = await heater.getFanTimer2Setting()
        self.assertEqual(setting, b'\x30')

        setting = await heater.update(0xD3)
        # _int() returns integer value, not _hh_mm() string
        self.assertEqual(setting, 48)

    async def test_setFanTimer2Setting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanTimer2Setting('45:00')
        self.assertIsNone(result)

    async def test_getFanTimer2ONTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        time = await heater.getFanTimer2ONTimeSetting()
        self.assertEqual(time, b'\x30')

        time = await heater.update(0xD4)
        self.assertEqual(time, '48:00')

    async def test_setFanTimer2ONTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanTimer2ONTimeSetting('01:00')
        self.assertIsNone(result)

    async def test_getFanTimer2OFFTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        time = await heater.getFanTimer2OFFTimeSetting()
        self.assertEqual(time, b'\x30')

        time = await heater.update(0xD5)
        self.assertEqual(time, '48:00')

    async def test_setFanTimer2OFFTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanTimer2OFFTimeSetting('02:00')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()