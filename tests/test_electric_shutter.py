# tests/test_electric_shutter.py
import unittest
from pychonet.ElectricShutter import ElectricShutter


class MockECHONETAPIClient:
    def __init__(self):
        # Raw byte values that simulate device responses
        # DICT_41_OPEN_CLOSE_STOP: 0x41='Open', 0x42='Close', 0x43='Stop'
        # DICT_41_LOW_MID_HIGH: 0x41='low', 0x42='medium', 0x43='high'
        # DICT_41_YES_NO: 0x41='yes', 0x42='no'
        self._state = {
            "192.168.1.120": {
                "instances": {
                    0x02: {  # Class group code for electric blind/shutter
                        0x61: {  # Class code for electrically operated shutter
                            0x01: {
                                0xE0: b'\x42',  # Open/close setting: Close
                                0xC2: b'\x41',  # Wind detection status: yes
                                0xC3: b'\x41',  # Sunlight detection status: yes
                                0xD0: b'\x41',  # Opening speed setting: low
                                0xD1: b'\x41',  # Closing speed setting: low
                                0xD2: b'\x00',  # Operation time: 0 seconds
                                0xD4: b'\x41',  # Automatic operation setting: on
                                0xE1: b'\x32',  # Degree-of-opening level: 2 (20%)
                                0xE2: b'\x32',  # Shade angle setting: 2 (20 degrees)
                                0xE3: b'\x42',  # Open/close speed: medium
                                0xE5: b'\x42',  # Electric lock setting: locked
                                0xE8: b'\x41',  # Remote operation setting: on
                                0xEA: b'\x42',  # Open/close status: Close
                                0x9F: list(range(0xE0, 0xEF, 0x01)),  # GETMAP
                                0x9E: [0xE0, 0xD0, 0xD1, 0xD4, 0xD2, 0xE1, 0xE2, 0xE3, 0xE5, 0xE8],  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        # Simulate a successful response
        return True


class TestElectricShutter(unittest.IsolatedAsyncioTestCase):
    async def test_getOpenCloseSetting(self):
        api_connector = MockECHONETAPIClient()
        shutter = ElectricShutter("192.168.1.120", api_connector)

        setting = await shutter.getOpenCloseSetting()
        self.assertEqual(setting, b'\x42')  # Close

        setting = await shutter.update(0xE0)
        expected = 'closed'  # DICT_41_OPEN_CLOSE_STOP[0x42] = 'closed'
        self.assertEqual(setting, expected)

    async def test_getWindDetectionStatus(self):
        api_connector = MockECHONETAPIClient()
        shutter = ElectricShutter("192.168.1.120", api_connector)

        status = await shutter.getMessage(0xC2)
        self.assertEqual(status, b'\x41')  # yes

        status = await shutter.update(0xC2)
        expected = 'yes'  # DICT_41_YES_NO[0x41] = 'yes'
        self.assertEqual(status, expected)

    async def test_getSunlightDetectionStatus(self):
        api_connector = MockECHONETAPIClient()
        shutter = ElectricShutter("192.168.1.120", api_connector)

        status = await shutter.getMessage(0xC3)
        self.assertEqual(status, b'\x41')  # yes

        status = await shutter.update(0xC3)
        expected = 'yes'  # DICT_41_YES_NO[0x41] = 'yes'
        self.assertEqual(status, expected)

    async def test_getOpeningSpeedSetting(self):
        api_connector = MockECHONETAPIClient()
        shutter = ElectricShutter("192.168.1.120", api_connector)

        speed = await shutter.getMessage(0xD0)
        self.assertEqual(speed, b'\x41')  # low

        speed = await shutter.update(0xD0)
        expected = 'low'  # DICT_41_LOW_MID_HIGH[0x41] = 'low'
        self.assertEqual(speed, expected)

    async def test_getClosingSpeedSetting(self):
        api_connector = MockECHONETAPIClient()
        shutter = ElectricShutter("192.168.1.120", api_connector)

        speed = await shutter.getMessage(0xD1)
        self.assertEqual(speed, b'\x41')  # low

        speed = await shutter.update(0xD1)
        expected = 'low'  # DICT_41_LOW_MID_HIGH[0x41] = 'low'
        self.assertEqual(speed, expected)

    async def test_getOperationTime(self):
        api_connector = MockECHONETAPIClient()
        shutter = ElectricShutter("192.168.1.120", api_connector)

        time = await shutter.getMessage(0xD2)
        self.assertEqual(time, b'\x00')  # 0 seconds

        time = await shutter.update(0xD2)
        expected = 0  # _int() returns integer value
        self.assertEqual(time, expected)


if __name__ == '__main__':
    unittest.main()