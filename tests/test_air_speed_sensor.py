# tests/test_air_speed_sensor.py
import unittest
from pychonet.AirSpeedSensor import AirSpeedSensor


class MockECHONETAPIClient:
    def __init__(self):
        # Raw byte values that simulate device responses
        # DICT_30_ON_OFF: 0x30='on', 0x31='off'
        self._state = {
            "192.168.1.70": {
                "instances": {
                    0x00: {  # Class group code for air speed sensor
                        0x1F: {  # Class code for air speed sensor
                            0x01: {
                                0x80: b'\x31',  # Operation status: OFF
                                0xE0: b'\x00',  # Measured air speed: 0 m/s (0.01 * 0)
                                0xE1: b'\x32',  # Air flow direction: 50 degrees
                                0x9F: [0x80, 0xE0, 0xE1],  # GETMAP
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


class TestAirSpeedSensor(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = AirSpeedSensor("192.168.1.70", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b'\x31')  # OFF

        status = await sensor.update(0x80)
        expected = 'off'  # DICT_30_ON_OFF[0x31] = 'off'
        self.assertEqual(status, expected)

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = AirSpeedSensor("192.168.1.70", api_connector)

        result = await sensor.setOperationStatus('on')
        self.assertTrue(result)

    async def test_getAirSpeed(self):
        api_connector = MockECHONETAPIClient()
        sensor = AirSpeedSensor("192.168.1.70", api_connector)

        speed = await sensor.getAirSpeed()
        self.assertEqual(speed, b'\x00')  # 0 m/s

        speed = await sensor.update(0xE0)
        expected = 0  # _int() returns integer value (0.01 * 0 = 0 m/s)
        self.assertEqual(speed, expected)

    async def test_getAirFlowDirection(self):
        api_connector = MockECHONETAPIClient()
        sensor = AirSpeedSensor("192.168.1.70", api_connector)

        direction = await sensor.getAirFlowDirection()
        self.assertEqual(direction, b'\x32')  # 50 degrees

        direction = await sensor.update(0xE1)
        expected = 50  # _int() returns integer value (degrees)
        self.assertEqual(direction, expected)


if __name__ == '__main__':
    unittest.main()