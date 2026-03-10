# tests/test_home_air_conditioner.py
import unittest
from unittest.mock import AsyncMock, patch
from pychonet.EchonetInstance import EchonetInstance
from pychonet.HomeAirConditioner import HomeAirConditioner

class MockECHONETAPIClient:
    def __init__(self):
        self._state = {
            "192.168.1.6": {
                "instances": {
                    0x01: {  # Group code for Air Conditioner
                        0x30: {  # Class code for Air Conditioner
                            0x01: {
                                0x80: b'\x31',  # Operation status: 0x30 = 'off'
                                0xB0: b'\x42',  # Operational mode: 0x01 = 'Cooling'
                                0xBB: b'\x20',  # Temperature setting: 0x20 = 26°C
                                0xA0: b'\x34',  # Fan speed: 0x34 = 'medium'
                                0xA1: b'\x41',  # Auto direction: 0x41 = 'auto'
                                0xA3: b'\x41',  # Swing mode: 0x41 = 'vert'
                                0xA4: b'\x41',  # Airflow vertical: 0x41 = 'upper'
                                0xA5: b'\x41',  # Airflow horizontal: 0x41 = 'rc-right'
                                0xB2: b'\x41',  # Silent mode: 0x41 = 'normal'
                                0x9F: [0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87],  # GETMAP
                                0x9E: [0x80, 0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x87],  # SETMAP
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

class TestHomeAirConditioner(unittest.IsolatedAsyncioTestCase):
    async def test_getOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        ac = HomeAirConditioner("192.168.1.6", api_connector)

        status = await ac.getOperationalStatus()
        print(status)
        self.assertEqual(status, b'\x31')  # 'off'

        status = await ac.update(0x80)
        expected = 'off'
        self.assertEqual(status, expected)

    async def test_getMode(self):
        api_connector = MockECHONETAPIClient()
        ac = HomeAirConditioner("192.168.1.6", api_connector)

        mode = await ac.getMode()
        self.assertEqual(mode, b'\x42')  # 'Cooling'

        status = await ac.update(0xB0)
        expected = 'cool'
        self.assertEqual(status, expected)

    async def test_getRoomTemperature(self):
        api_connector = MockECHONETAPIClient()
        ac = HomeAirConditioner("192.168.1.6", api_connector)

        temperature = await ac.getRoomTemperature()
        self.assertEqual(temperature, b'\x20')  # 26°C

    async def test_getFanSpeed(self):
        api_connector = MockECHONETAPIClient()
        ac = HomeAirConditioner("192.168.1.6", api_connector)

        fan_speed = await ac.getFanSpeed()
        self.assertEqual(fan_speed, b'\x34')  # 'low'

        status = await ac.update(0xA0)
        expected = 'medium'
        self.assertEqual(status, expected)

    async def test_getAutoDirection(self):
        api_connector = MockECHONETAPIClient()
        ac = HomeAirConditioner("192.168.1.6", api_connector)

        auto_direction = await ac.getAutoDirection()
        self.assertEqual(auto_direction, b'\x41')  # 'auto'

        status = await ac.update(0xA1)
        expected = 'auto'
        self.assertEqual(status, expected)


    async def test_getSwingMode(self):
        api_connector = MockECHONETAPIClient()
        ac = HomeAirConditioner("192.168.1.6", api_connector)

        swing_mode = await ac.getSwingMode()
        self.assertEqual(swing_mode, b'\x41')  # 'vert'

        status = await ac.update(0xA3)
        expected = 'vert'
        self.assertEqual(status, expected)

    async def test_getAirflowVertical(self):
        api_connector = MockECHONETAPIClient()
        ac = HomeAirConditioner("192.168.1.6", api_connector)

        airflow_vertical = await ac.getAirflowVert()
        self.assertEqual(airflow_vertical, b'\x41')  # 'upper'

        status = await ac.update(0xA4)
        expected = 'upper'
        self.assertEqual(status, expected)

    async def test_getAirflowHorizontal(self):
        api_connector = MockECHONETAPIClient()
        ac = HomeAirConditioner("192.168.1.6", api_connector)

        airflow_horizontal = await ac.getAirflowHoriz()
        self.assertEqual(airflow_horizontal, b'\x41')  # 'rc-right'

        status = await ac.update(0xA5)
        expected = 'rc-right'
        self.assertEqual(status, expected)

    async def test_getSilentMode(self):
        api_connector = MockECHONETAPIClient()
        ac = HomeAirConditioner("192.168.1.6", api_connector)

        silent_mode = await ac.getSilentMode()
        self.assertEqual(silent_mode, b'\x41')  # 'normal'

        status = await ac.update(0xB2)
        expected = 'normal'
        self.assertEqual(status, expected)