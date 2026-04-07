# tests/test_multiple_input_pcs.py
import unittest
from pychonet.MultipleInputPCS import MultipleInputPCS


class MockECHONETAPIClient:
    def __init__(self):
        # MultipleInputPCS EPC_FUNCTIONS behavior:
        # 0xD0: [_int, dict] - Grid connection status - 1 byte
        # 0xE0: _int - 2 bytes for cumulative energy
        # 0xE3: _int - 2 bytes for reverse cumulative energy
        # 0xE7: _signed_int - 2 bytes for instantaneous electricity
        self._state = {
            "192.168.1.240": {
                "instances": {
                    0x02: {
                        0xA5: {
                            0x01: {
                                0xD0: b'\x00',  # System interconnected
                                0xE0: b'\x50',  # 2 bytes = 0x0050 = 80
                                0xE3: b'\x28',  # 2 bytes = 0x0028 = 40
                                0xE7: b'\x50',  # 2 bytes = 0x0050 = 80
                                0x9F: [0xD0, 0xE0, 0xE3, 0xE7],  # GETMAP
                                0x9E: [0xD0, 0xE0, 0xE3, 0xE7],  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        return True


class TestMultipleInputPCS(unittest.IsolatedAsyncioTestCase):
    async def test_getGridConnectionStatus(self):
        api_connector = MockECHONETAPIClient()
        pcs = MultipleInputPCS("192.168.1.240", api_connector)

        status = await pcs.getMessage(0xD0)
        self.assertEqual(status, b'\x00')
        status = await pcs.update(0xD0)
        expected = 'System interconnected (reverse power flow acceptable)'
        self.assertEqual(status, expected)

    async def test_getMeasuredCumulativeEnergyNormal(self):
        api_connector = MockECHONETAPIClient()
        pcs = MultipleInputPCS("192.168.1.240", api_connector)

        energy = await pcs.getMessage(0xE0)
        self.assertEqual(energy, b'\x50')
        energy = await pcs.update(0xE0)
        self.assertEqual(energy, 80)

    async def test_getMeasuredCumulativeEnergyReverse(self):
        api_connector = MockECHONETAPIClient()
        pcs = MultipleInputPCS("192.168.1.240", api_connector)

        energy = await pcs.getMessage(0xE3)
        self.assertEqual(energy, b'\x28')
        energy = await pcs.update(0xE3)
        self.assertEqual(energy, 40)

    async def test_getMeasuredInstantaneousAmountOfElectricity(self):
        api_connector = MockECHONETAPIClient()
        pcs = MultipleInputPCS("192.168.1.240", api_connector)

        electricity = await pcs.getMessage(0xE7)
        self.assertEqual(electricity, b'\x50')
        electricity = await pcs.update(0xE7)
        self.assertEqual(electricity, 80)


if __name__ == '__main__':
    unittest.main()