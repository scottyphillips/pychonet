import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from pychonet.HomeAirConditioner import HomeAirConditioner
from pychonet.EchonetInstance import EchonetInstance

class TestHomeAirConditioner(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_api_connector = MagicMock()
        self.device = HomeAirConditioner("192.168.1.100", self.mock_api_connector)

    @patch('pychonet.EchonetInstance.EchonetInstance.getMessage')
    async def test_get_operational_temperature(self, mock_get_message):
        # Mock the message retrieval
        mock_get_message.return_value = b'\x00\x14'  # Simulated byte response for 20°C (little-endian)
        
        # Test the getOperationalTemperature method
        temperature = await self.device.getOperationalTemperature()
        self.assertEqual(temperature, b'\x00\x14')  # Expecting bytes for 20°C

    @patch('pychonet.EchonetInstance.EchonetInstance.setMessage')
    async def test_set_operational_temperature(self, mock_set_message):
        # Test the setOperationalTemperature method
        await self.device.setOperationalTemperature(25)
        
        # Verify that setMessage was called with the correct parameters
        mock_set_message.assert_called_once_with(0xB3, int(25))

    @patch('pychonet.EchonetInstance.EchonetInstance.getMessage')
    async def test_get_operational_temperature_error(self, mock_get_message):
        # Simulate an error condition
        mock_get_message.side_effect = Exception("Failed to retrieve temperature")
        
        with self.assertRaises(Exception):
            await self.device.getOperationalTemperature()

if __name__ == '__main__':
    unittest.main()

class TestHomeAirConditionerReal(unittest.IsolatedAsyncioTestCase):
    async def setUp(self):
        self.udp = UDPServer()
        self.loop = asyncio.get_event_loop()
        self.udp.run("0.0.0.0", 3610, loop=self.loop)
        self.server = api(self.udp)
        self.server._debug_flag = False
        self.server._message_timeout = 300
        await self.server.discover("192.168.1.6")
        
        # Wait for discovery to complete
        for x in range(0, 300):
            await asyncio.sleep(0.01)
            if "discovered" in list(self.server._state["192.168.1.6"]):
                break
                
        # Initialize device with real instance
        instances = self.server._state["192.168.1.6"]["instances"]
        for eojgc in instances.keys():
            for eojcc in instances[eojgc].keys():
                for instance in instances[eojgc][eojcc].keys():
                    await self.server.getAllPropertyMaps("192.168.1.6", eojgc, eojcc, 0x00)
                    getmap = [(hex(e), epc2str(eojgc, eojcc, e)) for e in instances[eojgc][eojcc][instance][ENL_GETMAP]]
                    
                    # Find Home Air Conditioner instance
                    if any(epc in ["Operation mode", "Operational temperature"] for epc in getmap):
                        self.device = HomeAirConditioner("192.168.1.6", self.server)
                        return

    @patch('pychonet.EchonetInstance.EchonetInstance.getMessage')
    async def test_get_real_operational_temperature(self, mock_get_message):
        # Test the getOperationalTemperature method on real device
        temperature = await self.device.getOperationalTemperature()
        self.assertIsInstance(temperature, bytes)
        self.assertNotEqual(temperature, b'\x00\x14')  # Should not be mock value

    @patch('pychonet.EchonetInstance.EchonetInstance.getMessage')
    async def test_get_real_operation_mode(self, mock_get_message):
        # Test the getOperationMode method on real device
        mode = await self.device.getOperationMode()
        self.assertIsInstance(mode, bytes)
        self.assertNotEqual(mode, b'\x00\x01')  # Should not be mock value