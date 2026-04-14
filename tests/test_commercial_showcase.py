# tests/test_commercial_showcase.py
import unittest
from pychonet.CommercialShowcase import CommercialShowcase
from pychonet.lib.epc_functions import DICT_LIGHTINGTYPE_40TO43

class MockECHONETAPIClient:
    def __init__(self):
        self._state = {
            "192.168.1.100": {
                "instances": {
                    0x03: {  # EOJGC - Commercial Showcase Group Code
                        0xCE: {  # EOJCC - Commercial Showcase Class Code
                            0x01: {
                                0xB0: b'\x41',   # Operation mode: cooling
                                0xBD: b'\x20',   # Discharge temperature: +32°C (signed)
                                0xCA: b'\x05',   # Group information
                                0xD0: b'\x42',   # Showcase type: inverter
                                0xD1: b'\x42',   # Door type: closed
                                0xD2: b'\x41',   # Refrigerator type: separate
                                0xD3: b'\x45',   # Shape type: reachIn
                                0xD4: b'\x41',   # Purpose type: refrigeration
                                0xE0: b'\x41',   # Internal lighting operation status: on
                                0xE1: b'\x42',   # External lighting operation status: off
                                0xE2: b'\x41',   # Compressor operation status: on
                                0xE3: b'\x08',    # Internal temperature: +8°C (signed)
                                0xE4: b'\x64',    # Rated electric power for freezing: 100W
                                0xE5: b'\x78',    # Rated electric power for defrosting heater: 120W
                                0xE6: b'\x3c',    # Rated electric power for fan motor: 60W
                                0xE7: b'\x41',    # Heater operation status: on
                                0xEB: b'\x41',    # Inside lighting type: led
                                0xEC: b'\x42',    # Outside lighting type: fluorescentLamp
                                0xED: b'\x64',    # Target inside brightness: 100% (0x64)
                                0xEE: b'\x32',    # Target outside brightness: 50% (0x32)
                                0xEF: b'\x10',    # Target inside temperature: +16°C (signed)
                                0x9F: [0xB0, 0xBD, 0xCA, 0xD0, 0xD1, 0xD2, 0xD3, 0xD4,
                                       0xE0, 0xE1, 0xE2, 0xE3, 0xE4, 0xE5, 0xE6, 0xE7,
                                       0xEB, 0xEC, 0xED, 0xEE, 0xEF],  # GETMAP
                                0x9E: [0xB0, 0xCA, 0xE0, 0xE1, 0xE2, 0xE7, 0xED, 0xEE, 0xEF],  # SETMAP
                            }
                        }
                    }
                }
            }
        }

    async def echonetMessage(self, host, eojgc, eojcc, eojci, message_type, opc):
        return True

class TestCommercialShowcase(unittest.IsolatedAsyncioTestCase):
    """Unit tests for CommercialShowcase device class."""
    
    async def test_getOperationMode(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        mode = await cs.getOperationMode()
        self.assertEqual(mode, b'\x41')  # 'cooling'

        status = await cs.update(0xB0)
        expected = 'cooling'
        self.assertEqual(status, expected)

    async def test_getDischargeTemperature(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        temp = await cs.getDischargeTemperature()
        self.assertEqual(temp, b'\x20')  # +32°C (signed int: 0x20 = 32)

    async def test_getGroupInformation(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        group_info = await cs.getGroupInformation()
        self.assertEqual(group_info, b'\x05')  # Group ID: 5

    async def test_getShowcaseType(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        showcase_type = await cs.getShowcaseType()
        self.assertEqual(showcase_type, b'\x42')  # 'inverter'

    async def test_getDoorType(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        door_type = await cs.getDoorType()
        self.assertEqual(door_type, b'\x42')  # 'closed'

    async def test_getRefrigeratorType(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        fridge_type = await cs.getRefrigeratorType()
        self.assertEqual(fridge_type, b'\x41')  # 'separate'

    async def test_getShapeType(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        shape_type = await cs.getShapeType()
        self.assertEqual(shape_type, b'\x45')  # 'reachIn'

    async def test_getPurposeType(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        purpose_type = await cs.getPurposeType()
        self.assertEqual(purpose_type, b'\x41')  # 'refrigeration'

    async def test_getInternalLightingOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        status = await cs.getInternalLightingOperationStatus()
        self.assertEqual(status, b'\x41')  # 'on'

    async def test_getExternalLightingOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        status = await cs.getExternalLightingOperationStatus()
        self.assertEqual(status, b'\x42')  # 'off'

    async def test_getCompressorOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        status = await cs.getCompressorOperationStatus()
        self.assertEqual(status, b'\x41')  # 'on'

    async def test_getInternalTemperature(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        temp = await cs.getInternalTemperature()
        self.assertEqual(temp, b'\x08')  # +8°C (signed int: 0x08 = 8)

    async def test_getRatedElectricPowerForFreezing(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        power = await cs.getRatedElectricPowerForFreezing()
        self.assertEqual(power, b'\x64')  # 100W (0x64 = 100)

    async def test_getRatedElectricPowerForDefrostingHeater(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        power = await cs.getRatedElectricPowerForDefrostingHeater()
        self.assertEqual(power, b'\x78')  # 120W (0x78 = 120)

    async def test_getRatedElectricPowerForFanMotor(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        power = await cs.getRatedElectricPowerForFanMotor()
        self.assertEqual(power, b'\x3c')  # 60W (0x3c = 60)

    async def test_getHeaterOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        status = await cs.getHeaterOperationStatus()
        self.assertEqual(status, b'\x41')  # 'on'

    async def test_getInsideLightingType(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        lighting_type = await cs.getInsideLightingType()
        self.assertEqual(lighting_type, b'\x41')  # 'led' (from DICT_LIGHTINGTYPE_40TO43)

    async def test_getOutsideLightingType(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        lighting_type = await cs.getOutsideLightingType()
        self.assertEqual(lighting_type, b'\x42')  # 'fluorescentLamp' (from DICT_LIGHTINGTYPE_40TO43)

    async def test_getTargetInsideBrightness(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        brightness = await cs.getTargetInsideBrightness()
        self.assertEqual(brightness, b'\x64')  # 100% (0x64 = 100)

    async def test_getTargetOutsideBrightness(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        brightness = await cs.getTargetOutsideBrightness()
        self.assertEqual(brightness, b'\x32')  # 50% (0x32 = 50)

    async def test_getTargetInsideTemperature(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        temp = await cs.getTargetInsideTemperature()
        self.assertEqual(temp, b'\x10')  # +16°C (signed int: 0x10 = 16)


# Tests for update() method - setting properties
class TestCommercialShowcaseUpdate(unittest.IsolatedAsyncioTestCase):
    """Unit tests for CommercialShowcase update/set methods."""

    async def test_update_operationMode(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        # Test get first - current value is 'cooling' (0x41)
        mode = await cs.getOperationMode()
        self.assertEqual(mode, b'\x41')  # 'cooling'

        # Test update/set operation mode - returns the property name mapping
        status = await cs.update(0xB0)
        expected = 'cooling'
        self.assertEqual(status, expected)

    async def test_update_internalLightingOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        # Test get first - current value is 'on' (0x41)
        status = await cs.getInternalLightingOperationStatus()
        self.assertEqual(status, b'\x41')  # 'on'

        # Test update/set internal lighting - returns the property name mapping
        result = await cs.update(0xE0)
        expected = 'on'
        self.assertEqual(result, expected)

    async def test_update_externalLightingOperationStatus(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        # Test get first - current value is 'off' (0x42)
        status = await cs.getExternalLightingOperationStatus()
        self.assertEqual(status, b'\x42')  # 'off'

        # Test update/set external lighting - returns the property name mapping
        result = await cs.update(0xE1)
        expected = 'off'
        self.assertEqual(result, expected)

    async def test_update_targetInsideBrightness(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        # Test get first - current value is 100% (0x64)
        brightness = await cs.getTargetInsideBrightness()
        self.assertEqual(brightness, b'\x64')  # 100%

        # Test update/set target inside brightness - returns the property name mapping
        result = await cs.update(0xED)
        expected = 100
        self.assertEqual(result, expected)

    async def test_update_targetOutsideBrightness(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        # Test get first - current value is 50% (0x32)
        brightness = await cs.getTargetOutsideBrightness()
        self.assertEqual(brightness, b'\x32')  # 50%

        # Test update/set target outside brightness - returns the property name mapping
        result = await cs.update(0xEE)
        expected = 50
        self.assertEqual(result, expected)

    async def test_update_targetInsideTemperature(self):
        api_connector = MockECHONETAPIClient()
        cs = CommercialShowcase("192.168.1.100", api_connector)

        # Test get first - current value is +16°C (0x10)
        temp = await cs.getTargetInsideTemperature()
        self.assertEqual(temp, b'\x10')  # +16°C

        # Test update/set target inside temperature - returns the property name mapping
        result = await cs.update(0xEF)
        expected = 16
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
