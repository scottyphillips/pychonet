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
                                0xB8: bytes.fromhex("04b0003c0014003c"),
                                0xBB: bytes.fromhex("fb"),
                                0xBE: bytes.fromhex("f6"),
                                0xA0: b'\x41',  # Air flow rate setting (0x41 = 65)
                                0xA1: bytes.fromhex("32"),
                                0xC0: bytes.fromhex("30"),
                                0xC1: bytes.fromhex("0030"),
                                0xC2: bytes.fromhex("fff6"),
                                0xC3: bytes.fromhex("31"),
                                0xC4: bytes.fromhex("30"),
                                0xC5: bytes.fromhex("10"),
                                0xC6: bytes.fromhex("14"),
                                0xC7: bytes.fromhex("30"),
                                0xC8: bytes.fromhex("31"),
                                0xD0: bytes.fromhex("42"),
                                0xD1: bytes.fromhex("061e"),
                                0xD2: bytes.fromhex("0700"),
                                0xD3: bytes.fromhex("41"),
                                0xD4: bytes.fromhex("1200"),
                                0xD5: bytes.fromhex("1400"),
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
        self.assertEqual(power, bytes.fromhex("04b0003c0014003c"))

        power = await heater.update(0xB8)
        self.assertEqual(power, {"heat_storage": 1200, "control": 60, "weak_airflow": 20, "strong_airflow": 60})

    async def test_getMeasuredIndoorTemperature(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        temp = await heater.getMeasuredIndoorTemperature()
        self.assertEqual(temp, bytes.fromhex("fb"))

        temp = await heater.update(0xBB)
        self.assertEqual(temp, -5)

    async def test_getMeasuredOutdoorTemperature(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        temp = await heater.getMeasuredOutdoorTemperature()
        self.assertEqual(temp, bytes.fromhex("f6"))

        temp = await heater.update(0xBE)
        self.assertEqual(temp, -10)

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
        self.assertEqual(status, bytes.fromhex("32"))

        status = await heater.update(0xA1)
        self.assertEqual(status, "weak")

    async def test_setFanOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanOperationStatus('off')
        self.assertIsNone(result)

    async def test_getHeatStorageOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        status = await heater.getHeatStorageOperationStatus()
        self.assertEqual(status, bytes.fromhex("30"))

        status = await heater.update(0xC0)
        self.assertEqual(status, "on")

    async def test_setHeatStorageOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setHeatStorageOperationStatus('off')
        self.assertIsNone(result)

    async def test_getHeatStorageTemperatureSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        temp = await heater.getHeatStorageTemperatureSetting()
        self.assertEqual(temp, bytes.fromhex("0030"))

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
        self.assertEqual(temp, bytes.fromhex("fff6"))

        temp = await heater.update(0xC2)
        self.assertEqual(temp, -10)

    async def test_getDaytimeHeatStorageSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        setting = await heater.getDaytimeHeatStorageSetting()
        self.assertEqual(setting, bytes.fromhex("31"))

        setting = await heater.update(0xC3)
        self.assertEqual(setting, "off")

    async def test_setDaytimeHeatStorageSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setDaytimeHeatStorageSetting('enabled')
        self.assertIsNone(result)

    async def test_getDaytimeHeatStorageAbility(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        ability = await heater.getDaytimeHeatStorageAbility()
        self.assertEqual(ability, bytes.fromhex("30"))

        ability = await heater.update(0xC4)
        self.assertEqual(ability, "available")

    async def test_getMidnightPowerDurationSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        duration = await heater.getMidnightPowerDurationSetting()
        self.assertEqual(duration, bytes.fromhex("10"))

        duration = await heater.update(0xC5)
        self.assertEqual(duration, 16)

    async def test_setMidnightPowerDurationSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setMidnightPowerDurationSetting(12)
        self.assertIsNone(result)

    async def test_getMidnightPowerStartTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        time = await heater.getMidnightPowerStartTimeSetting()
        self.assertEqual(time, bytes.fromhex("14"))

        time = await heater.update(0xC6)
        self.assertEqual(time, 20)

    async def test_setMidnightPowerStartTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setMidnightPowerStartTimeSetting('01:00')
        self.assertIsNone(result)

    async def test_getRadiationMethod(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        method = await heater.getRadiationMethod()
        self.assertEqual(method, bytes.fromhex("30"))

        method = await heater.update(0xC7)
        self.assertEqual(method, "With fan")

    async def test_setRadiationMethod(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setRadiationMethod('Radiant heat method')
        self.assertIsNone(result)

    async def test_getChildLockSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        lock = await heater.getChildLockSetting()
        self.assertEqual(lock, bytes.fromhex("31"))

        lock = await heater.update(0xC8)
        self.assertEqual(lock, "disabled")

    async def test_setChildLockSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setChildLockSetting('enabled')
        self.assertIsNone(result)

    async def test_getFanTimer1Setting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        setting = await heater.getFanTimer1Setting()
        self.assertEqual(setting, bytes.fromhex("42"))

        setting = await heater.update(0xD0)
        self.assertEqual(setting, 0x42)

    async def test_setFanTimer1Setting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanTimer1Setting('45:00')
        self.assertIsNone(result)

    async def test_getFanTimer1ONTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        time = await heater.getFanTimer1ONTimeSetting()
        self.assertEqual(time, bytes.fromhex("061e"))

        time = await heater.update(0xD1)
        self.assertEqual(time, "6:30")

    async def test_setFanTimer1ONTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanTimer1ONTimeSetting('01:00')
        self.assertIsNone(result)

    async def test_getFanTimer1OFFTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        time = await heater.getFanTimer1OFFTimeSetting()
        self.assertEqual(time, bytes.fromhex("0700"))

        time = await heater.update(0xD2)
        self.assertEqual(time, "7:00")

    async def test_setFanTimer1OFFTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanTimer1OFFTimeSetting('02:00')
        self.assertIsNone(result)

    async def test_getFanTimer2Setting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        setting = await heater.getFanTimer2Setting()
        self.assertEqual(setting, bytes.fromhex("41"))

        setting = await heater.update(0xD3)
        self.assertEqual(setting, 0x41)

    async def test_setFanTimer2Setting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanTimer2Setting('45:00')
        self.assertIsNone(result)

    async def test_getFanTimer2ONTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        time = await heater.getFanTimer2ONTimeSetting()
        self.assertEqual(time, bytes.fromhex("1200"))

        time = await heater.update(0xD4)
        self.assertEqual(time, "18:00")

    async def test_setFanTimer2ONTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanTimer2ONTimeSetting('01:00')
        self.assertIsNone(result)

    async def test_getFanTimer2OFFTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        time = await heater.getFanTimer2OFFTimeSetting()
        self.assertEqual(time, bytes.fromhex("1400"))

        time = await heater.update(0xD5)
        self.assertEqual(time, "20:00")

    async def test_setFanTimer2OFFTimeSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = ElectricStorageHeater("192.168.1.250", api_connector)

        result = await heater.setFanTimer2OFFTimeSetting('02:00')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()