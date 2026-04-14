"""Unit tests for ElectricHeater ECHONET device class."""
import unittest
from pychonet.ElectricHeater import ElectricHeater


class MockECHONETAPIClient:
    """Mock API client for testing ElectricHeater functionality.

    Uses EOJX codes: group=0x01, class=0x42 (Electric heater)
    EPCs cover operation status, temperature settings, and airflow control
    
    Note: Properties return raw bytes from getMessage(). Only update() with 
    EPC_FUNCTIONS applies decoding to return formatted values.
    """

    def __init__(self):
        self._state = {
            "192.168.1.65": {
                "instances": {
                    0x01: {  # EoJGC (Class Group Code) for Electric Heater
                        0x42: {  # EoJCC (Class Code) for Electric Heater
                            0x01: {  # Instance code
                                0x80: b"\x30",  # Operation status: on
                                0xB1: b"\x41",  # Automatic temperature control setting: auto
                                0xB3: b"\x20",  # Temperature setting: 32°C
                                0xBB: b"\x25",  # Measured room temperature: 37°C
                                0xBC: b"\x1E",  # Remotely set temperature: 30°C
                                0xA0: b"\x41",  # Air flow rate setting: auto
                                0x9F: [0x80, 0xB1, 0xB3, 0xBB, 0xBC, 0xA0],  # GETMAP
                                0x9E: [0x80, 0xB1, 0xB3, 0xA0],  # SETMAP
                            }
                        },
                    },
                },
            },
        }

    async def echonetMessage(
        self, host, eojgc, eojcc, eojci, message_type, opc
    ):  # pylint: disable=unused-argument
        """Simulate successful ECHONET message response."""
        return True


class TestElectricHeater(unittest.IsolatedAsyncioTestCase):
    """Test cases for ElectricHeater device class.

    Uses EOJX codes: group=0x01, class=0x42 (Electric heater)
    
    Note: Properties return raw bytes from getMessage(). Only update() with 
    EPC_FUNCTIONS applies decoding to return formatted values.
    """

    async def test_get_operation_status(self):
        """Test getOperationStatus returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricHeater("192.168.1.65", api_connector)

        status = await heater.getOperationStatus()
        self.assertEqual(status, b"\x30")  # on (raw bytes)

    async def test_set_operation_status(self):
        """Test setOperationStatus sets operation status."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricHeater("192.168.1.65", api_connector)

        result = await heater.setOperationStatus(b"\x31")  # off
        self.assertTrue(result)

    async def test_get_temperature_setting(self):
        """Test getTemperatureSetting returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricHeater("192.168.1.65", api_connector)

        temp = await heater.getTemperatureSetting()
        self.assertEqual(temp, b"\x20")  # raw bytes (32°C when decoded)

    async def test_set_temperature_setting(self):
        """Test setTemperatureSetting sets temperature."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricHeater("192.168.1.65", api_connector)

        result = await heater.setTemperatureSetting(b"\x19")  # 25°C (0x19)
        self.assertTrue(result)

    async def test_get_measured_room_temperature(self):
        """Test getMeasuredRoomTemperature returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricHeater("192.168.1.65", api_connector)

        temp = await heater.getMeasuredRoomTemperature()
        self.assertEqual(temp, b"\x25")  # raw bytes (37°C when decoded as signed int)

    async def test_get_air_flow_rate_setting(self):
        """Test getAirFlowRateSetting returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricHeater("192.168.1.65", api_connector)

        flow = await heater.getAirFlowRateSetting()
        self.assertEqual(flow, b"\x41")  # auto (raw bytes)

    async def test_set_air_flow_rate_setting(self):
        """Test setAirFlowRateSetting sets air flow rate."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricHeater("192.168.1.65", api_connector)

        result = await heater.setAirFlowRateSetting(b"\x34")  # level 4
        self.assertTrue(result)

    async def test_get_automatic_temperature_control_setting(self):
        """Test getAutomaticTemperatureControlSetting returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricHeater("192.168.1.65", api_connector)

        setting = await heater.getAutomaticTemperatureControlSetting()
        self.assertEqual(setting, b"\x41")  # auto (raw bytes)

    async def test_set_automatic_temperature_control_setting(self):
        """Test setAutomaticTemperatureControlSetting sets setting."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricHeater("192.168.1.65", api_connector)

        result = await heater.setAutomaticTemperatureControlSetting(b"\x42")  # non-auto
        self.assertTrue(result)

    async def test_get_remotely_set_temperature(self):
        """Test getRemotelySetTemperature returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        heater = ElectricHeater("192.168.1.65", api_connector)

        temp = await heater.getRemotelySetTemperature()
        self.assertEqual(temp, b"\x1E")  # raw bytes (30°C when decoded)


if __name__ == "__main__":
    unittest.main()
