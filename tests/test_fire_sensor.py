# tests/test_fire_sensor.py
import unittest
from unittest.mock import AsyncMock, patch
from pychonet.EchonetInstance import EchonetInstance
from pychonet.FireSensor import FireSensor

class MockECHONETAPIClient:
    def __init__(self):
        self._state = {
            "192.168.1.7": {
                "instances": {
                    0x00: {  # EoJGC (Class Group Code) for Fire Sensor
                        0x19: {  # EoJCC (Class Code) for Fire Sensor
                            0x01: {  # Instance code
                                0x80: b'\x30',  # Operation status: 0x30 = 'ON'
                                0xB0: b'\x35',  # Detection threshold level: 0x35 = 'level-5'
                                0xB1: b'\x42',  # Fire occurrence detection status: 0x42 = 'not found'
                                0x9F: [0x80, 0xB0, 0xB1],  # GETMAP
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

    def _state(self, host):
        return self._state[host]


class TestFireSensor(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = FireSensor("192.168.1.7", api_connector)

        status = await sensor.getOperationStatus()
        print(status)
        self.assertEqual(status, b'\x30')  # 'on'

        status = await sensor.update(0x80)
        expected = 'on'
        self.assertEqual(status, expected)

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = FireSensor("192.168.1.7", api_connector)

        # Test setting to OFF (0x31)
        result = await sensor.setOperationStatus(0x31)
        self.assertTrue(result)

    async def test_getDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = FireSensor("192.168.1.7", api_connector)

        level = await sensor.getDetectionThresholdLevel()
        self.assertEqual(level, b'\x35')  # 'level-5'

        status = await sensor.update(0xB0)
        expected = 'level-5'
        self.assertEqual(status, expected)

    async def test_setDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = FireSensor("192.168.1.7", api_connector)

        # Test setting to level-3 (0x33)
        result = await sensor.setDetectionThresholdLevel(0x33)
        self.assertTrue(result)

    async def test_getFireOccurrenceDetectionStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = FireSensor("192.168.1.7", api_connector)

        status = await sensor.getFireOccurrenceDetectionStatus()
        self.assertEqual(status, b'\x42')  # 'not found'

        result = await sensor.update(0xB1)
        expected = 'Fire occurrence detection status not found'
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()