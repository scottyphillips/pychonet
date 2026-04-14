# tests/test_hybrid_water_heater.py
import unittest
from pychonet.HybridWaterHeater import HybridWaterHeater


class MockECHONETAPIClient:
    def __init__(self):
        self._state = {
            "192.168.1.220": {
                "instances": {
                    0x02: {
                        0xA6: {
                            0x01: {
                                0xB0: b'\x41',
                                0xB2: b'\x41',
                                0xB3: b'\x41',
                                0xB6: b'\x41',
                                0xB7: b'\x41',
                                0xB8: b'\x41',
                                0xB9: b'\x00\x30\x00\x00',
                                0xC3: b'\x42',
                                0xE1: b'\x3c',
                                0xE2: b'\x14',
                                0x9F: [0xB0, 0xB2, 0xB3, 0xB6, 0xB7, 0xB8, 0xB9, 0xC3, 0xE1, 0xE2],
                                0x9E: [0xB0, 0xB2, 0xB3, 0xB6, 0xB7, 0xB8, 0xE1, 0xE2],
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        return True


class TestHybridWaterHeater(unittest.IsolatedAsyncioTestCase):
    async def test_getAutomaticWaterHeatingSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = HybridWaterHeater("192.168.1.220", api_connector)

        setting = await heater.getMessage(0xB0)
        self.assertEqual(setting, b'\x41')

        setting = await heater.update(0xB0)
        expected = 'Automatic water heating'
        self.assertEqual(setting, expected)

    async def test_getWaterHeatingStatus(self):
        api_connector = MockECHONETAPIClient()
        heater = HybridWaterHeater("192.168.1.220", api_connector)

        status = await heater.getMessage(0xB2)
        self.assertEqual(status, b'\x41')

        status = await heater.update(0xB2)
        expected = 'heating'
        self.assertEqual(status, expected)

    async def test_getHeaterStatus(self):
        api_connector = MockECHONETAPIClient()
        heater = HybridWaterHeater("192.168.1.220", api_connector)

        status = await heater.getMessage(0xB3)
        self.assertEqual(status, b'\x41')

        status = await heater.update(0xB3)
        expected = 'heating'
        self.assertEqual(status, expected)

    async def test_getAuxiliaryHeatSourceSetting(self):
        api_connector = MockECHONETAPIClient()
        heater = HybridWaterHeater("192.168.1.220", api_connector)

        setting = await heater.getMessage(0xB6)
        self.assertEqual(setting, b'\x41')

        setting = await heater.update(0xB6)
        expected = 'Set'
        self.assertEqual(setting, expected)

    async def test_getAuxiliaryHeatSourceMode(self):
        api_connector = MockECHONETAPIClient()
        heater = HybridWaterHeater("192.168.1.220", api_connector)

        mode = await heater.getMessage(0xB7)
        self.assertEqual(mode, b'\x41')

        mode = await heater.update(0xB7)
        expected = 'Set'
        self.assertEqual(mode, expected)

    async def test_getSolarPowerGenerationsUtilizationTime(self):
        api_connector = MockECHONETAPIClient()
        heater = HybridWaterHeater("192.168.1.220", api_connector)

        time = await heater.getMessage(0xB8)
        self.assertEqual(time, b'\x41')

        time = await heater.update(0xB8)
        expected = 'Mode off'
        self.assertEqual(time, expected)

    async def test_getSolarPowerGenerationsUtilizationTime0(self):
        api_connector = MockECHONETAPIClient()
        heater = HybridWaterHeater("192.168.1.220", api_connector)

        time = await heater.getMessage(0xB9)
        self.assertEqual(time, b'\x00\x30\x00\x00')  # 4 bytes

        time = await heater.update(0xB9)
        # _02A6B9 returns datetime in H:MM format (single digit for HH)
        # byte[0]=0x00, byte[1]=0x30=48, byte[2]=0x00, byte[3]=0x00
        # start_time = "0:48", end_time = "0:00"
        expected = {'start_time': '0:48', 'end_time': '0:00'}
        self.assertEqual(time, expected)

    async def test_getHotWaterSupplyStatus(self):
        api_connector = MockECHONETAPIClient()
        heater = HybridWaterHeater("192.168.1.220", api_connector)

        status = await heater.getMessage(0xC3)
        self.assertEqual(status, b'\x42')

        status = await heater.update(0xC3)
        expected = 'Stopped'
        self.assertEqual(status, expected)

    async def test_getMeasuredAmountOfHotWater(self):
        api_connector = MockECHONETAPIClient()
        heater = HybridWaterHeater("192.168.1.220", api_connector)

        water = await heater.getMessage(0xE1)
        self.assertEqual(water, b'\x3c')

        water = await heater.update(0xE1)
        expected = 60
        self.assertEqual(water, expected)

    async def test_getTankCapacity(self):
        api_connector = MockECHONETAPIClient()
        heater = HybridWaterHeater("192.168.1.220", api_connector)

        capacity = await heater.getMessage(0xE2)
        self.assertEqual(capacity, b'\x14')

        capacity = await heater.update(0xE2)
        expected = 20
        self.assertEqual(capacity, expected)


if __name__ == '__main__':
    unittest.main()