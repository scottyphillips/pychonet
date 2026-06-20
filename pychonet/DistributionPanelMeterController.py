from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    _int, 
    _signed_int,
    _null_padded_optional_string,
    _yyyy_mm_dd,
    _swap_dict,
)


# Lookup dictionaries for enum values
DICT_POWER_SAVING = {0x41: "power-saving", 0x42: "normal"}

DICT_CONNECTION_STATUS = {
    0x41: "connected", 
    0x42: "disconnected", 
    0x43: "not-registered", 
    0x44: "deleted"
}

DICT_DEVICE_FAULT_STATUS = {0x41: "yes", 0x42: "no"}


def _raw_bytes(edt):
    """Return raw bytes as hex string for binary data."""
    return edt.hex() if edt else None


class DistributionPanelMeterController(EchonetInstance):
    """
    ECHONET Lite Controller Device Class
    
    EOJ: 0x05 (Controller Group) / 0xFF (Controller Class)
    
    This class represents a Controller device that manages and controls
    multiple connected devices. It provides properties for device listing,
    configuration, and status monitoring.
    
    Key Properties:
        - Operation status (0x80): ON/OFF (inherited from base class)
        - Installation location (0x81)
        - Identification number (0x83) (inherited from base class)
        - Power limit setting (0x99)
        - Controller ID (0xC0)
        - Device list management (0xC2-0xCB)
        - Connection status (0xC6)
        - Fault status (0x88) (inherited from base class)
    """
    
    EPC_FUNCTIONS = {
        0x81: _raw_bytes,                              # Installation location
        0x82: _int,                                    # Standard version information
        0x86: _signed_int,                             # Manufacturer's fault code
        0x87: _int,                                    # Current limit setting (0-100%)
        0x8B: _raw_bytes,                              # Business facility code (3 bytes)
        0x8D: _null_padded_optional_string,            # Production number
        0x8E: _raw_bytes,                              # Production date code (4 bytes)
        0x8F: [_int, DICT_POWER_SAVING],               # Power-saving operation setting
        0x93: _int,                                    # Remote control setting
        0x98: _yyyy_mm_dd,                             # Current date setting (YYYY:MM:DD format)
        0x99: _int,                                    # Power limit setting (W)
        0xC0: _null_padded_optional_string,            # Controller ID
        0xC1: _int,                                    # Number of devices controlled
        0xC2: _int,                                    # Index (device list index)
        0xC3: _null_padded_optional_string,            # Device ID
        0xC4: _raw_bytes,                              # Device type
        0xC5: _null_padded_optional_string,            # Name
        0xC6: [_int, DICT_CONNECTION_STATUS],          # Connection status
        0xC7: _raw_bytes,                              # Business code of the device to be controlled (3 bytes)
        0xC8: _null_padded_optional_string,            # Product code of the device to be controlled
        0xC9: _raw_bytes,                              # Manufacture date of the device to be controlled (4 bytes)
        0xCA: _raw_bytes,                              # Registered information renewal date (4 bytes)
        0xCB: _int,                                    # Registered information renewal version information
        0xCC: _null_padded_optional_string,            # Place to install device to be controlled
        0xCD: [_int, DICT_DEVICE_FAULT_STATUS],        # Fault status of device to be controlled
        0xCE: _raw_bytes,                              # Set property map for device to be controlled
        0xCF: _raw_bytes,                              # Get property map for device to be controlled
        0xE0: _null_padded_optional_string,            # Address of installation location
    }

    def __init__(self, host, api_connector, instance=0x1):
        self._eojgc = 0x05
        self._eojcc = 0xFF
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    # Connection Status Constants
    CONNECTION_CONNECTED = 0x41
    CONNECTION_DISCONNECTED = 0x42
    CONNECTION_NOT_REGISTERED = 0x43
    CONNECTION_DELETED = 0x44
    
    # Operation Status Constants (inherited from base class)
    OPERATION_ON = 0x30
    OPERATION_OFF = 0x31
    
    # Fault Status Constants (inherited from base class)
    FAULT_OCCURRED = 0x41
    FAULT_NO_OCCURRENCE = 0x42
    
    # Power Saving Mode Constants
    POWER_SAVING_OPERATION = 0x41
    NORMAL_OPERATION = 0x42

    # ===== Device Management Properties (EPC 0xC0 - 0xCF) =====
    
    async def get_controller_id(self):
        """Get the Controller ID (EPC 0xC0)"""
        return await self.getMessage(0xC0)
    
    async def set_controller_id(self, value):
        """Set the Controller ID (EPC 0xC0)"""
        return await self.setMessage(0xC0, value)

    async def get_number_of_devices_controlled(self):
        """Get the number of devices controlled (EPC 0xC1)"""
        return await self.getMessage(0xC1)

    async def get_device_list_index(self):
        """Get the current device list index (EPC 0xC2)"""
        return await self.getMessage(0xC2)
    
    async def set_device_list_index(self, value):
        """Set the device list index (EPC 0xC2)"""
        return await self.setMessage(0xC2, value)

    async def get_device_id(self):
        """Get the ID of the selected device (EPC 0xC3)"""
        return await self.getMessage(0xC3)

    async def get_device_type(self):
        """Get the type of the selected device (EPC 0xC4)"""
        return await self.getMessage(0xC4)

    async def get_device_name(self):
        """Get the name of the selected device (EPC 0xC5)"""
        return await self.getMessage(0xC5)

    async def get_connection_status(self):
        """Get the connection status of the selected device (EPC 0xC6)"""
        return await self.getMessage(0xC6)

    async def get_business_code(self):
        """Get the business code of the selected device (EPC 0xC7)"""
        return await self.getMessage(0xC7)

    async def get_device_product_code(self):
        """Get the product code of the selected device (EPC 0xC8)"""
        return await self.getMessage(0xC8)

    async def get_device_manufacture_date(self):
        """Get the manufacture date of the selected device (EPC 0xC9)"""
        return await self.getMessage(0xC9)

    async def get_renewal_date(self):
        """Get the registered information renewal date (EPC 0xCA)"""
        return await self.getMessage(0xCA)

    async def get_renewal_version_information(self):
        """Get the registered information renewal version information (EPC 0xCB)"""
        return await self.getMessage(0xCB)

    async def get_device_installation_place(self):
        """Get the installation place of the selected device (EPC 0xCC)"""
        return await self.getMessage(0xCC)

    async def get_device_fault_status(self):
        """Get the fault status of the selected device (EPC 0xCD)"""
        return await self.getMessage(0xCD)

    async def get_set_property_map_for_device(self):
        """Get the set property map for the selected device (EPC 0xCE)"""
        return await self.getMessage(0xCE)

    async def get_get_property_map_for_device(self):
        """Get the get property map for the selected device (EPC 0xCF)"""
        return await self.getMessage(0xCF)

    # ===== Device Status Properties (EPC 0x81, 0x86-0x87, 0x8B-0x8F) =====
    
    async def get_installation_location(self):
        """Get the installation location (EPC 0x81)"""
        return await self.getMessage(0x81)
    
    async def set_installation_location(self, value):
        """Set the installation location (EPC 0x81)"""
        return await self.setMessage(0x81, value)

    async def get_standard_version_information(self):
        """Get the standard version information (EPC 0x82)"""
        return await self.getMessage(0x82)

    async def get_manufacturer_fault_code(self):
        """Get the manufacturer's fault code (EPC 0x86)"""
        return await self.getMessage(0x86)

    async def get_current_limit(self):
        """Get the current limit setting in percent (EPC 0x87)"""
        return await self.getMessage(0x87)
    
    async def set_current_limit(self, value):
        """Set the current limit setting in percent (EPC 0x87)"""
        return await self.setMessage(0x87, value)

    async def get_business_facility_code(self):
        """Get the 3-byte business facility code (EPC 0x8B)"""
        return await self.getMessage(0x8B)

    async def get_production_number(self):
        """Get the production number (EPC 0x8D)"""
        return await self.getMessage(0x8D)

    async def get_production_date(self):
        """Get the production date code (EPC 0x8E)"""
        return await self.getMessage(0x8E)

    async def get_power_saving_mode(self):
        """Get the power-saving operation setting (EPC 0x8F)"""
        return await self.getMessage(0x8F)
    
    async def set_power_saving_mode(self, value):
        """Set the power-saving operation setting (EPC 0x8F)"""
        return await self.setMessage(0x8F, value)

    # ===== Configuration Properties (EPC 0x93, 0x98-0x99) =====
    
    async def get_remote_control_setting(self):
        """Get the remote control setting (EPC 0x93)"""
        return await self.getMessage(0x93)
    
    async def set_remote_control_setting(self, value):
        """Set the remote control setting (EPC 0x93)"""
        return await self.setMessage(0x93, value)

    async def get_current_date(self):
        """Get the current date (EPC 0x98)"""
        return await self.getMessage(0x98)
    
    async def set_current_date(self, value):
        """Set the current date (EPC 0x98)"""
        return await self.setMessage(0x98, value)

    async def get_power_limit(self):
        """Get the power limit setting in watts (EPC 0x99)"""
        return await self.getMessage(0x99)
    
    async def set_power_limit(self, value):
        """Set the power limit setting in watts (EPC 0x99)"""
        return await self.setMessage(0x99, value)

    # ===== Installation Address (EPC 0xE0) =====
    
    async def get_installation_address(self):
        """Get the address of installation location (EPC 0xE0)"""
        return await self.getMessage(0xE0)