from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DICT_41_ON_OFF,
    DICT_LIGHTINGTYPE_40TO43,
    _int,
    _signed_int,
)


# Operation mode enums for releases F-H and I-latest
DICT_COMMERCIALSHOWCASE_OPERATION_MODE = {
    0x41: "cooling",
    0x42: "nonCooling",
    0x43: "defrosting",
    0x44: "draining",
    0x40: "other",
}

# Showcase type enums (EPC 0xD0)
DICT_COMMERCIALSHOWCASE_SHOWCASE_TYPE = {
    0x41: "nonFluorocarbonInverter",
    0x42: "inverter",
    0x40: "other",
}

# Door type enums (EPC 0xD1)
DICT_COMMERCIALSHOWCASE_DOOR_TYPE = {
    0x41: "open",
    0x42: "closed",
}

# Refrigerator type enums (EPC 0xD2)
DICT_COMMERCIALSHOWCASE_REFRIGERATOR_TYPE = {
    0x41: "separate",
    0x42: "builtIn",
}

# Shape type enums (EPC 0xD3)
DICT_COMMERCIALSHOWCASE_SHAPE_TYPE = {
    0x41: "box",
    0x42: "desktop",
    0x43: "tripleGlass",
    0x44: "quadrupleQuintupleGlass",
    0x45: "reachIn",
    0x46: "glassTop",
    0x47: "multistageOpenAndCeilingBlowoff",
    0x48: "multistageOpenAndBacksideBlowoff",
    0x49: "flat",
    0x4A: "walkIn",
    0x40: "other",
}

# Purpose type enums (EPC 0xD4)
DICT_COMMERCIALSHOWCASE_PURPOSE_TYPE = {
    0x41: "refrigeration",
    0x42: "freezing",
}


class CommercialShowcase(EchonetInstance):
    EOJGC = 0x03
    EOJCC = 0xCE

    EPC_FUNCTIONS = {
        # Operation mode (EPC 0xB0) - releases F-H and I-latest have same enum
        0xB0: [_int, DICT_COMMERCIALSHOWCASE_OPERATION_MODE],
        # Discharge temperature (EPC 0xBD)
        0xBD: _signed_int,
        # Group information (EPC 0xCA) - release dependent
        0xCA: _int,
        # Showcase type (EPC 0xD0)
        0xD0: [_int, DICT_COMMERCIALSHOWCASE_SHOWCASE_TYPE],
        # Door type (EPC 0xD1)
        0xD1: [_int, DICT_COMMERCIALSHOWCASE_DOOR_TYPE],
        # Refrigerator type (EPC 0xD2)
        0xD2: [_int, DICT_COMMERCIALSHOWCASE_REFRIGERATOR_TYPE],
        # Shape type (EPC 0xD3)
        0xD3: [_int, DICT_COMMERCIALSHOWCASE_SHAPE_TYPE],
        # Purpose type (EPC 0xD4)
        0xD4: [_int, DICT_COMMERCIALSHOWCASE_PURPOSE_TYPE],
        # Internal lighting operation status (EPC 0xE0)
        0xE0: [_int, DICT_41_ON_OFF],
        # External lighting operation status (EPC 0xE1)
        0xE1: [_int, DICT_41_ON_OFF],
        # Compressor operation status (EPC 0xE2)
        0xE2: [_int, DICT_41_ON_OFF],
        # Internal temperature (EPC 0xE3)
        0xE3: _signed_int,
        # Rated electric power for freezing (EPC 0xE4)
        0xE4: _int,
        # Rated electric power for defrosting heater (EPC 0xE5)
        0xE5: _int,
        # Rated electric power for fan motor (EPC 0xE6)
        0xE6: _int,
        # Heater operation status (EPC 0xE7)
        0xE7: [_int, DICT_41_ON_OFF],
        # Inside lighting type (EPC 0xEB)
        0xEB: [_int, DICT_LIGHTINGTYPE_40TO43],
        # Outside lighting type (EPC 0xEC)
        0xEC: [_int, DICT_LIGHTINGTYPE_40TO43],
        # Target inside brightness (EPC 0xED)
        0xED: _int,
        # Target outside brightness (EPE 0xEE)
        0xEE: _int,
        # Target inside temperature (EPC 0xEF)
        0xEF: _signed_int,
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        EchonetInstance.__init__(
            self, host, self.EOJGC, self.EOJCC, instance, api_connector
        )

    # Operation mode (EPC 0xB0) - get/set
    async def getOperationMode(self):
        """Get the operation mode of the showcase."""
        return await self.getMessage(0xB0)

    async def setOperationMode(self, mode):
        """Set the operation mode of the showcase.
        
        Args:
            mode: One of 'cooling', 'nonCooling', 'defrosting', 'draining', or 'other'
        """
        return await self.setMessage(0xB0, mode)

    # Discharge temperature (EPC 0xBD) - get only
    async def getDischargeTemperature(self):
        """Get the measured discharge temperature in degrees Celsius."""
        return await self.getMessage(0xBD)

    # Group information (EPC 0xCA) - release dependent
    async def getGroupInformation(self):
        """Get group information to link showcases with outdoor units for showcases.
        
        Note: Required for releases I and later, optional for earlier releases.
        """
        return await self.getMessage(0xCA)

    async def setGroupInformation(self, group_id):
        """Set group information (optional).
        
        Args:
            group_id: Group ID from 1-253 or None to clear
        """
        return await self.setMessage(0xCA, group_id)

    # Showcase type (EPC 0xD0) - get only
    async def getShowcaseType(self):
        """Get the showcase type.
        
        Returns one of: 'nonFluorocarbonInverter', 'inverter', or 'other'
        """
        return await self.getMessage(0xD0)

    # Door type (EPC 0xD1) - get only
    async def getDoorType(self):
        """Get the door type of the showcase.
        
        Returns one of: 'open' or 'closed'
        """
        return await self.getMessage(0xD1)

    # Refrigerator type (EPC 0xD2) - get only
    async def getRefrigeratorType(self):
        """Get the refrigerator type.
        
        Returns one of: 'separate' or 'builtIn'
        """
        return await self.getMessage(0xD2)

    # Shape type (EPC 0xD3) - get only
    async def getShapeType(self):
        """Get the shape type of the showcase.
        
        Returns one of: 'box', 'desktop', 'tripleGlass', 'quadrupleQuintupleGlass',
                        'reachIn', 'glassTop', 'multistageOpenAndCeilingBlowoff',
                        'multistageOpenAndBacksideBlowoff', 'flat', 'walkIn', or 'other'
        """
        return await self.getMessage(0xD3)

    # Purpose type (EPC 0xD4) - get only
    async def getPurposeType(self):
        """Get the purpose of the showcase.
        
        Returns one of: 'refrigeration' or 'freezing'
        """
        return await self.getMessage(0xD4)

    # Internal lighting operation status (EPC 0xE0) - get/set
    async def getInternalLightingOperationStatus(self):
        """Get the on/off status of internal lighting."""
        return await self.getMessage(0xE0)

    async def setInternalLightingOperationStatus(self, status):
        """Set the internal lighting on/off status.
        
        Args:
            status: 'on' or 'off'
        """
        return await self.setMessage(0xE0, status)

    # External lighting operation status (EPC 0xE1) - get/set
    async def getExternalLightingOperationStatus(self):
        """Get the on/off status of external lighting."""
        return await self.getMessage(0xE1)

    async def setExternalLightingOperationStatus(self, status):
        """Set the external lighting on/off status.
        
        Args:
            status: 'on' or 'off'
        """
        return await self.setMessage(0xE1, status)

    # Compressor operation status (EPC 0xE2) - get/set
    async def getCompressorOperationStatus(self):
        """Get the on/off status of compressor when showcase and compressor are a single unit."""
        return await self.getMessage(0xE2)

    async def setCompressorOperationStatus(self, status):
        """Set the compressor on/off status.
        
        Args:
            status: 'on' or 'off'
        """
        return await self.setMessage(0xE2, status)

    # Internal temperature (EPC 0xE3) - get only
    async def getInternalTemperature(self):
        """Get the measured internal temperature inside the showcase in degrees Celsius."""
        return await self.getMessage(0xE3)

    # Rated electric power for freezing (EPC 0xE4) - get only
    async def getRatedElectricPowerForFreezing(self):
        """Get the rated power consumption necessary when showcase is cooling (in watts)."""
        return await self.getMessage(0xE4)

    # Rated electric power for defrosting heater (EPC 0xE5) - get only
    async def getRatedElectricPowerForDefrostingHeater(self):
        """Get the rated power consumption when heater is operating during defrosting (in watts)."""
        return await self.getMessage(0xE5)

    # Rated electric power for fan motor (EPC 0xE6) - get only
    async def getRatedElectricPowerForFanMotor(self):
        """Get the rated power consumption when fan motor is operating (in watts)."""
        return await self.getMessage(0xE6)

    # Heater operation status (EPC 0xE7) - get only
    async def getHeaterOperationStatus(self):
        """Get the on/off status of heater for hot function.
        
        Note: Only available for showcases with hot function, required for those units.
        """
        return await self.getMessage(0xE7)

    # Inside lighting type (EPC 0xEB) - get only
    async def getInsideLightingType(self):
        """Get the type of lighting installed inside the showcase."""
        return await self.getMessage(0xEB)

    # Outside lighting type (EPC 0xEC) - get only
    async def getOutsideLightingType(self):
        """Get the type of lighting installed outside the showcase."""
        return await self.getMessage(0xEC)

    # Target inside brightness (EPC 0xED) - get/set
    async def getTargetInsideBrightness(self):
        """Get the target inside brightness level in percent (0-100%)."""
        return await self.getMessage(0xED)

    async def setTargetInsideBrightness(self, percentage):
        """Set the target inside brightness level.
        
        Args:
            percentage: Brightness level from 0 to 100
        """
        return await self.setMessage(0xED, percentage)

    # Target outside brightness (EPC 0xEE) - get/set
    async def getTargetOutsideBrightness(self):
        """Get the target outside brightness level in percent (0-100%)."""
        return await self.getMessage(0xEE)

    async def setTargetOutsideBrightness(self, percentage):
        """Set the target outside brightness level.
        
        Args:
            percentage: Brightness level from 0 to 100
        """
        return await self.setMessage(0xEE, percentage)

    # Target inside temperature (EPC 0xEF) - get/set
    async def getTargetInsideTemperature(self):
        """Get the target inside temperature setting in degrees Celsius."""
        return await self.getMessage(0xEF)

    async def setTargetInsideTemperature(self, temperature):
        """Set the target inside temperature.
        
        Args:
            temperature: Temperature from -127 to 126 degrees Celsius
        """
        return await self.setMessage(0xEF, temperature)
