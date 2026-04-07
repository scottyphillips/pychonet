# tests/test_fuel_cell.py
import unittest
from pychonet.FuelCell import FuelCell


class MockECHONETAPIClient:
    def __init__(self):
        # Raw byte values that simulate device responses
        # EPC 0xC1: Measured temperature
        # EPC 0xC2: Rated power generation output
        # EPC 0xCA: Power generation setting (ON/OFF)
        # EPC 0xCB: Power generation status
        # EPC 0xCC: Measured in-house instantaneous power consumption
        self._state = {
            "192.168.1.50": {
                "instances": {
                    0x02: {  # Class group code for fuel cell
                        0x7C: {  # Class code for fuel cell
                            0x01: {
                                0xC1: b'\x2a',  # Measured temperature: 42°C
                                0xC2: b'\x3c',  # Rated power: 60W
                                0xC4: b'\x14',  # Instantaneous power: 20W
                                0xCA: b'\x41',  # Power generation setting: ON
                                0xCB: b'\x42',  # Power generation status: Stopped
                                0xCC: b'\x05',  # Instantaneous power consumption: 5W
                                0xD0: b'\x01',  # System interconnected type
                                0x9F: [0xC1, 0xC2, 0xC4, 0xCA, 0xCB, 0xCC, 0xD0],  # GETMAP
                                0x9E: [0xCA, 0xC1, 0xC2, 0xC4, 0xCC, 0xD0],  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        # Simulate a successful response
        return True


class TestFuelCell(unittest.IsolatedAsyncioTestCase):
    async def test_getMeasuredTemperature(self):
        api_connector = MockECHONETAPIClient()
        cell = FuelCell("192.168.1.50", api_connector)

        temp = await cell.getMessage(0xC1)
        self.assertEqual(temp, b'\x2a')  # 42°C

        temp = await cell.update(0xC1)
        expected = 42  # _int() returns integer value
        self.assertEqual(temp, expected)

    async def test_getRatedPowerGenerationOutput(self):
        api_connector = MockECHONETAPIClient()
        cell = FuelCell("192.168.1.50", api_connector)

        power = await cell.getMessage(0xC2)
        self.assertEqual(power, b'\x3c')  # 60W

        power = await cell.update(0xC2)
        expected = 60  # _int() returns integer value
        self.assertEqual(power, expected)

    async def test_getPowerGenerationSetting(self):
        api_connector = MockECHONETAPIClient()
        cell = FuelCell("192.168.1.50", api_connector)

        setting = await cell.getMessage(0xCA)
        self.assertEqual(setting, b'\x41')  # ON

        setting = await cell.update(0xCA)
        expected = 'on'  # DICT_41_ON_OFF[0x41] = 'on'
        self.assertEqual(setting, expected)

    async def test_getPowerGenerationStatus(self):
        api_connector = MockECHONETAPIClient()
        cell = FuelCell("192.168.1.50", api_connector)

        status = await cell.getMessage(0xCB)
        self.assertEqual(status, b'\x42')  # Stopped

        status = await cell.update(0xCB)
        expected = 'Stopped'  # Power generation status dict
        self.assertEqual(status, expected)

    async def test_getMeasuredInstantaneousPowerConsumption(self):
        api_connector = MockECHONETAPIClient()
        cell = FuelCell("192.168.1.50", api_connector)

        power = await cell.getMessage(0xCC)
        self.assertEqual(power, b'\x05')  # 5W

        power = await cell.update(0xCC)
        expected = 5  # _int() returns integer value
        self.assertEqual(power, expected)


if __name__ == '__main__':
    unittest.main()