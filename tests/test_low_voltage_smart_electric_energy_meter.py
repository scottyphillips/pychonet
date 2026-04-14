# tests/test_low_voltage_smart_electric_energy_meter.py
import unittest
from pychonet.LowVoltageSmartElectricEnergyMeter import LowVoltageSmartElectricEnergyMeter


class MockECHONETAPIClient:
    def __init__(self):
        # The library's custom parser functions use specific byte interpretations:
        # _0288E0: _int() interprets 2 bytes (unsigned int)
        # _0288E1: _int() with dict interprets 1 byte
        # _0288E7: _signed_int() interprets 2 bytes (signed int)
        # _0288E8: returns dict with 2 bytes per phase (signed int each), divided by 10
        self._state = {
            "192.168.1.230": {
                "instances": {
                    0x02: {
                        0x88: {
                            0x01: {
                                0xD3: b'\x01',  # Coefficient
                                0xD7: b'\x02',  # Number of effective digits
                                0xE0: b'\x50',  # 2 bytes = 0x0050 = 80
                                0xE1: b'\x03',  # Unit: 0.001
                                0xE3: b'\x28',  # 2 bytes = 0x0028 = 40
                                0xE7: b'\x50',  # 2 bytes = 0x0050 = 80
                                0xE8: b'\x03\xe0',  # R phase: 0x03e0/10=99.2, T phase: 0/10=0.0
                                0x9F: list(range(0xD3, 0xE8, 0x01)),
                                0x9E: [0xD3, 0xD7, 0xE0, 0xE1, 0xE3, 0xE7, 0xE8],
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        return True


class TestLowVoltageSmartElectricEnergyMeter(unittest.IsolatedAsyncioTestCase):
    async def test_getCoefficient(self):
        api_connector = MockECHONETAPIClient()
        meter = LowVoltageSmartElectricEnergyMeter("192.168.1.230", api_connector)

        coef = await meter.getMessage(0xD3)
        self.assertEqual(coef, b'\x01')
        coef = await meter.update(0xD3)
        self.assertEqual(coef, 1)

    async def test_getNumberOfWorkingDigits(self):
        api_connector = MockECHONETAPIClient()
        meter = LowVoltageSmartElectricEnergyMeter("192.168.1.230", api_connector)

        digits = await meter.getMessage(0xD7)
        self.assertEqual(digits, b'\x02')
        digits = await meter.update(0xD7)
        self.assertEqual(digits, 2)

    async def test_getMeasuredCumulativeEnergyNormal(self):
        api_connector = MockECHONETAPIClient()
        meter = LowVoltageSmartElectricEnergyMeter("192.168.1.230", api_connector)

        energy = await meter.getMessage(0xE0)
        self.assertEqual(energy, b'\x50')

        energy = await meter.update(0xE0)
        self.assertEqual(energy, 80)

    async def test_getUnitForCumulativeEnergy(self):
        api_connector = MockECHONETAPIClient()
        meter = LowVoltageSmartElectricEnergyMeter("192.168.1.230", api_connector)

        unit = await meter.getMessage(0xE1)
        self.assertEqual(unit, b'\x03')

        unit = await meter.update(0xE1)
        expected = 0.001
        self.assertEqual(unit, expected)

    async def test_getMeasuredCumulativeEnergyReverse(self):
        api_connector = MockECHONETAPIClient()
        meter = LowVoltageSmartElectricEnergyMeter("192.168.1.230", api_connector)

        energy = await meter.getMessage(0xE3)
        self.assertEqual(energy, b'\x28')

        energy = await meter.update(0xE3)
        self.assertEqual(energy, 40)

    async def test_getMeasuredInstantaneousElectricEnergy(self):
        api_connector = MockECHONETAPIClient()
        meter = LowVoltageSmartElectricEnergyMeter("192.168.1.230", api_connector)

        energy = await meter.getMessage(0xE7)
        self.assertEqual(energy, b'\x50')

        energy = await meter.update(0xE7)
        self.assertEqual(energy, 80)

    async def test_getMeasuredInstantaneousCurrents(self):
        api_connector = MockECHONETAPIClient()
        meter = LowVoltageSmartElectricEnergyMeter("192.168.1.230", api_connector)

        current = await meter.getMessage(0xE8)
        self.assertEqual(current, b'\x03\xe0')

        current = await meter.update(0xE8)
        # R phase: 0x03e0 / 10 = 99.2, T phase: 0 / 10 = 0.0
        expected = {"r_phase_amperes": 99.2, "t_phase_amperes": 0.0}
        self.assertEqual(current, expected)


if __name__ == '__main__':
    unittest.main()