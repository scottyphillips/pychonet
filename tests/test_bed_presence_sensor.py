# tests/test_bed_presence_sensor.py
import unittest
from pychonet.BedPresenceSensor import BedPresenceSensor


class MockECHONETAPIClient:
    def __init__(self):
        # Raw byte values that simulate device responses
        # DICT_30_ON_OFF: 0x30='on', 0x31='off'
        # DICT_31_8_LEVELS: 0x31='level-1', 0x38='level-8'
        # BED_PRESENCE_MAP: 0x41='bed present', 0x42='bed absent'
        self._state = {
            "192.168.1.20": {
                "instances": {
                    0x00: {  # Class group code for bed presence sensor
                        0x28: {  # Class code for bed presence sensor
                            0x01: {
                                0x80: b'\x31',  # Operation status: OFF
                                0xB0: b'\x33',  # Detection threshold level: level-3
                                0xB1: b'\x41',  # Bed presence detection status: bed present
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


class TestBedPresenceSensor(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = BedPresenceSensor("192.168.1.20", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b'\x31')  # OFF

        status = await sensor.update(0x80)
        expected = 'off'  # DICT_30_ON_OFF[0x31] = 'off'
        self.assertEqual(status, expected)

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = BedPresenceSensor("192.168.1.20", api_connector)

        result = await sensor.setOperationStatus('on')
        self.assertTrue(result)

    async def test_getDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = BedPresenceSensor("192.168.1.20", api_connector)

        level = await sensor.getDetectionThresholdLevel()
        self.assertEqual(level, b'\x33')  # level-3

        status = await sensor.update(0xB0)
        expected = 'level-3'  # DICT_31_8_LEVELS[0x33] = 'level-3'
        self.assertEqual(status, expected)

    async def test_setDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = BedPresenceSensor("192.168.1.20", api_connector)

        result = await sensor.setDetectionThresholdLevel('level-8')
        self.assertTrue(result)

    async def test_getBedPresenceDetectionStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = BedPresenceSensor("192.168.1.20", api_connector)

        presence_status = await sensor.getBedPresenceDetectionStatus()
        self.assertEqual(presence_status, b'\x41')  # bed present
        status = await sensor.update(0xB1)
        expected = 'bed present'  # BED_PRESENCE_MAP[0x41] = 'bed present'
        self.assertEqual(status, expected)


if __name__ == '__main__':
    unittest.main()