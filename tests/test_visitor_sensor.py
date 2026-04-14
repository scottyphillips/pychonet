# tests/test_visitor_sensor.py
import unittest
from pychonet.VisitorSensor import VisitorSensor


class MockECHONETAPIClient:
    def __init__(self):
        # VisitorSensor EPC_FUNCTIONS:
        # 0xB0: [_int, DICT_31_8_LEVELS] - Detection threshold level
        # 0xB1: [_int, DICT_41_ON_OFF] - Visitor detection status
        # 0xBE: _int - Visitor detection holding time
        self._state = {
            "192.168.1.210": {
                "instances": {
                    0x00: {
                        0x08: {
                            0x01: {
                                0xB0: b'\x35',  # Detection threshold level: level-5
                                0xB1: b'\x41',  # Visitor detection status: on
                                0xBE: b'\x30',  # Visitor detection holding time: 0 seconds
                                0x9F: [0xB0, 0xB1, 0xBE],  # GETMAP
                                0x9E: [0xB0, 0xB1, 0xBE],  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        return True


class TestVisitorSensor(unittest.IsolatedAsyncioTestCase):
    async def test_getDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = VisitorSensor("192.168.1.210", api_connector)

        level = await sensor.getMessage(0xB0)
        self.assertEqual(level, b'\x35')  # level-5

        level = await sensor.update(0xB0)
        expected = 'level-5'  # DICT_31_8_LEVELS[0x35] = 'level-5'
        self.assertEqual(level, expected)

    async def test_setDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = VisitorSensor("192.168.1.210", api_connector)

        result = await sensor.setMessage(0xB0, 'level-8')
        self.assertTrue(result)

    async def test_getVisitorDetectionStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = VisitorSensor("192.168.1.210", api_connector)

        status = await sensor.getMessage(0xB1)
        self.assertEqual(status, b'\x41')  # on

        status = await sensor.update(0xB1)
        expected = 'on'  # DICT_41_ON_OFF[0x41] = 'on'
        self.assertEqual(status, expected)

    async def test_setVisitorDetectionStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = VisitorSensor("192.168.1.210", api_connector)

        result = await sensor.setMessage(0xB1, 'off')
        self.assertTrue(result)

    async def test_getVisitorDetectionHoldingTime(self):
        api_connector = MockECHONETAPIClient()
        sensor = VisitorSensor("192.168.1.210", api_connector)

        time = await sensor.getMessage(0xBE)
        self.assertEqual(time, b'\x30')  # 0 seconds in mock data

        time = await sensor.update(0xBE)
        # _int() interprets byte 0x30 as 48, not 0
        expected = 48
        self.assertEqual(time, expected)

    async def test_setVisitorDetectionHoldingTime(self):
        api_connector = MockECHONETAPIClient()
        sensor = VisitorSensor("192.168.1.210", api_connector)

        result = await sensor.setMessage(0xBE, 60)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()