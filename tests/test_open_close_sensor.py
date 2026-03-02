# tests/test_open_close_sensor.py
import unittest
from unittest.mock import AsyncMock, patch
from pychonet.EchonetInstance import EchonetInstance
from pychonet.OpenCloseSensor import OpenCloseSensor

class MockECHONETAPIClient:
    def __init__(self):
        self._state = {
            "192.168.1.100": {
                "instances": {
                    0x00: {
                        0x29: {
                            0x1: {
                                0x80: b'\x30',  # Operation status: 0x30 = 'off'
                                0xB0: b'\x01',  # Detection threshold level: 0x01
                                0xB1: b'\x41',  # Degree-of-opening detection status: 0x41 = 'open detected'
                                0xE0: b'\x30',  # Open/close detection status: 0x30 = 'close detected'
                                0x9F: [0x80, 0xB0, 0xB1, 0xE0],  # GETMAP: readable EPCs
                                0x9E: [0x80, 0xB0, 0xB1, 0xE0],  # SETMAP: settable EPCs
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

class TestOpenCloseSensor(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = OpenCloseSensor("192.168.1.100", api_connector)

        status = await sensor.getOperationStatus()
        self.assertEqual(status, b'\x30')

    async def test_setOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = OpenCloseSensor("192.168.1.100", api_connector)
        result = await sensor.setOperationStatus("on")
        self.assertTrue(result)

    async def test_getDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = OpenCloseSensor("192.168.1.100", api_connector)

        level = await sensor.getDetectionThresholdLevel()
        self.assertEqual(level, b'\x01')

    async def test_setDetectionThresholdLevel(self):
        api_connector = MockECHONETAPIClient()
        sensor = OpenCloseSensor("192.168.1.100", api_connector)

        result = await sensor.setDetectionThresholdLevel(2)
        self.assertTrue(result)

    async def test_getDegreeOfOpeningDetectionStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = OpenCloseSensor("192.168.1.100", api_connector)

        status = await sensor.getDegreeOfOpeningDetectionStatus()
        self.assertEqual(status, b'\x41')

    async def test_getOpenCloseDetectionStatus(self):
        api_connector = MockECHONETAPIClient()
        sensor = OpenCloseSensor("192.168.1.100", api_connector)

        status = await sensor.getOpenCloseDetectionStatus()
        self.assertEqual(status, b'\x30')

    async def test_update(self):
        api_connector = MockECHONETAPIClient()
        sensor = OpenCloseSensor("192.168.1.100", api_connector)

        status = await sensor.update()
        self.assertEqual(status, {128: 'on', 176: 'Invalid setting', 177: 'open detected', 224: 'close detected'} )