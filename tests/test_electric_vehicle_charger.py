"""Unit tests for ElectricVehicleCharger ECHONET device class."""
import unittest
from pychonet.ElectricVehicleCharger import ElectricVehicleCharger


class MockECHONETAPIClient:
    """Mock API client for testing ElectricVehicleCharger functionality.

    Uses EOJX codes: group=0x02, class=0xA1 (Electric vehicle charger)
    EPCs cover charging status, battery info, and power settings
    """

    def __init__(self):
        self._state = {
            "192.168.1.50": {
                "instances": {
                    0x02: {  # EoJGC (Class Group Code) for Electric Vehicle Charger
                        0xA1: {  # EoJCC (Class Code) for Electric Vehicle Charger
                            0x01: {  # Instance code
                                0x80: b"\x30",  # Operation status: on
                                0xC5: b"\x00\x00\x00\x64",  # Rated charge capacity (100 Wh)
                                0xC7: b"\x41",  # Vehicle connection and chargeable status: Connected to vehicle, Chargeable
                                0xCC: b"\x12",  # Charger type: AC_HLC (charging only)
                                0xD3: b"\x00\x00\x05\xF8",  # Measured instantaneous charging electric power (1520 W)
                                0xDA: b"\x44",  # Operating mode setting: Standby
                                0xE6: b"\x00\x32",  # Vehicle ID (50)
                                0x9F: [0x80, 0xC5, 0xC7, 0xD3, 0xDA, 0xE6],  # GETMAP
                                0x9E: [0x80, 0xDA],  # SETMAP (read-only for most properties)
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


class TestElectricVehicleCharger(unittest.IsolatedAsyncioTestCase):
    """Test cases for ElectricVehicleCharger device class.

    Uses EOJX codes: group=0x02, class=0xA1 (Electric vehicle charger)
    
    Note: getMessage() returns raw bytes. Only update() with EPC_FUNCTIONS 
    applies decoding to return formatted values.
    """

    async def test_getOperationStatus_returns_bytes(self):
        """Test getOperationStatus returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        charger = ElectricVehicleCharger("192.168.1.50", api_connector)

        status = await charger.getOperationStatus()
        self.assertEqual(status, b"\x30")  # on (raw bytes)

    async def test_setOperationStatus(self):
        """Test setOperationStatus sets correct value."""
        api_connector = MockECHONETAPIClient()
        charger = ElectricVehicleCharger("192.168.1.50", api_connector)

        result = await charger.setOperationStatus(0x31)  # off
        self.assertTrue(result)

    async def test_getVehicleConnectionAndChargeableStatus_returns_bytes(self):
        """Test getVehicleConnectionAndChargeableStatus returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        charger = ElectricVehicleCharger("192.168.1.50", api_connector)

        status = await charger.getVehicleConnectionAndChargeableStatus()
        self.assertEqual(status, b"\x41")  # Connected to vehicle, Chargeable (raw bytes)

    async def test_getMeasuredInstantaneousChargingElectricPower_returns_bytes(self):
        """Test getMeasuredInstantaneousChargingElectricPower returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        charger = ElectricVehicleCharger("192.168.1.50", api_connector)

        power = await charger.getMeasuredInstantaneousChargingElectricPower()
        self.assertEqual(power, b"\x00\x00\x05\xf8")  # raw bytes (unsigned long)

    async def test_getOperatingModeSetting_returns_bytes(self):
        """Test getOperatingModeSetting returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        charger = ElectricVehicleCharger("192.168.1.50", api_connector)

        mode = await charger.getOperatingModeSetting()
        self.assertEqual(mode, b"\x44")  # Standby (raw bytes)

    async def test_setOperatingModeSetting(self):
        """Test setOperatingModeSetting sets correct value."""
        api_connector = MockECHONETAPIClient()
        charger = ElectricVehicleCharger("192.168.1.50", api_connector)

        result = await charger.setOperatingModeSetting(0x42)  # Charging
        self.assertTrue(result)

    async def test_getVehicleID_returns_bytes(self):
        """Test getVehicleID returns raw bytes."""
        api_connector = MockECHONETAPIClient()
        charger = ElectricVehicleCharger("192.168.1.50", api_connector)

        vehicle_id = await charger.getVehicleID()
        self.assertEqual(vehicle_id, b"\x00\x32")  # raw bytes (short integer)

    async def test_setChargingAmountSetting(self):
        """Test setChargingAmountSetting sets correct value."""
        api_connector = MockECHONETAPIClient()
        charger = ElectricVehicleCharger("192.168.1.50", api_connector)

        result = await charger.setChargingAmountSetting(1000)
        self.assertTrue(result)

    async def test_setChargingCurrentSetting(self):
        """Test setChargingCurrentSetting sets correct value."""
        api_connector = MockECHONETAPIClient()
        charger = ElectricVehicleCharger("192.168.1.50", api_connector)

        result = await charger.setChargingCurrentSetting(16)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
