# tests/test_activity_amount_sensor.py
import unittest
from pychonet.ActivityAmountSensor import ActivityAmountSensor


class MockECHONETAPIClient:
    def __init__(self):
        # Raw byte values that simulate device responses
        # DICT_30_ON_OFF: 0x30='on', 0x31='off'
        # DICT_31_8_LEVELS: 0x31='level-1', 0x38='level-8'
        self._state = {
            "192.168.1.60": {
                "instances": {
                    0x00: {  # Class group code for activity amount sensor
                        0x1D: {  # Class code for activity amount sensor
                            0x01: {
                                0x80: b'\x31',  # Operation status: OFF
                                0xB0: b'\x35',  # Activity threshold level: level-5
                                0xB1: b'\x41',  # Activity status: active
                                0xE0: b'\x14',  # Measured activity amount: 20
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


class TestActivityAmountSensor(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = ActivityAmountSensor("192.168.1.60", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b'\x31')  # OFF

        status = await sensor.update(0x80)
        expected = 'off'  # DICT_30_ON_OFF[0x31] = 'off'
        self.assertEqual(status, expected)

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = ActivityAmountSensor("192.168.1.60", api_connector)

        result = await sensor.setOperationStatus('on')
        self.assertTrue(result)

    async def test_getActivityThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = ActivityAmountSensor("192.168.1.60", api_connector)

        level = await sensor.getActivityThresholdLevel()
        self.assertEqual(level, b'\x35')  # level-5

        level = await sensor.update(0xB0)
        expected = 'level-5'  # DICT_31_8_LEVELS[0x35] = 'level-5'
        self.assertEqual(level, expected)

    async def test_setActivityThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = ActivityAmountSensor("192.168.1.60", api_connector)

        result = await sensor.setActivityThresholdLevel('level-8')
        self.assertTrue(result)

    async def test_getActivityStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = ActivityAmountSensor("192.168.1.60", api_connector)

        status = await sensor.getActivityStatus()
        self.assertEqual(status, b'\x41')  # active
        status = await sensor.update(0xB1)
        expected = 'active'  # {0x41: 'active', 0x42: 'inactive'}
        self.assertEqual(status, expected)

    async def test_getMeasuredActivityAmount(self):
        api_connector = MockECHONETAPIClient()
        sensor = ActivityAmountSensor("192.168.1.60", api_connector)

        amount = await sensor.getMeasuredActivityAmount()
        self.assertEqual(amount, b'\x14')  # 20

        amount = await sensor.update(0xE0)
        expected = 20  # _int() returns integer value
        self.assertEqual(amount, expected)


if __name__ == '__main__':
    unittest.main()