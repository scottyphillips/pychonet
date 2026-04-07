from typing import Dict, List, Any, Optional, Union, Callable, ClassVar

from pychonet.lib.const import (
    ENL_CUMULATIVE_POWER,
    ENL_CUMULATIVE_RUNTIME,
    ENL_GETMAP,
    ENL_INSTANTANEOUS_POWER,
    ENL_MANUFACTURER,
    ENL_OFF,
    ENL_ON,
    ENL_SETMAP,
    ENL_STATUS,
    ENL_UID,
    GET,
    SETC,
)
from pychonet.lib.epc import EPC_CODE, EPC_SUPER
from pychonet.lib.epc_functions import EPC_SUPER_FUNCTIONS


def call_epc_function(
    epc_function: Any,
    edt: Any,
) -> Any:
    """Call an EPC function with the given EDT data.
    
    Args:
        epc_function: The EPC function to call (can be a function or list)
        edt: The EDT data to pass to the function
        
    Returns:
        The result of calling the function
    """
    if type(epc_function) == list:
        if list(epc_function) == 3:
            data = epc_function[0](
                edt,
                epc_function[1],
                epc_function[2],
            )
        else:
            data = epc_function[0](edt, epc_function[1])
    else:
        data = epc_function(edt)
    return data


"""
Superclass for Echonet instance objects.
"""


class EchonetInstance:
    """Constructs an object to represent an Echonet lite instance.

    :param host: Host IP address of the device
    :param eojgc: Echonet group code
    :param eojcc: Echonet class code
    :param instance: Instance ID
    :param api_connector: API connector for ECHONET communication
    """

    EPC_FUNCTIONS: ClassVar[Dict[int, Any]] = {}
    _host: str
    _eojgc: int
    _eojcc: int
    _eojci: int
    _api: Any
    _epc_data: Dict[int, bytes]

    def __init__(self, host, eojgc, eojcc, instance, api_connector=None):
        self._host = host
        self._eojgc = eojgc
        self._eojcc = eojcc
        self._eojci = instance
        self._api = api_connector
        self._epc_data = self._api._state[self._host]["instances"][self._eojgc][
            self._eojcc
        ][self._eojci]

        # TODO self instantiate the API connector for backwards compatability with the older library

    """
    getMessage is used to fire a single ECHONET get messages to get Node information
    Assumes one EPC is sent per message.

    :param tx_epc: EPC byte code for the request.
    :return: the deconstructed payload for the response

    """

    async def getMessage(self, epc: int, pdc: int = 0) -> Optional[Any]:
        """Get a property value from the device.

        Args:
            epc: EPC byte code for the request
            pdc: Property Data Count (default: 0)

        Returns:
            The property value or None if not found
        """
        opc = [{"EPC": epc, "PDC": pdc}]
        response = await self._api.echonetMessage(
            self._host, self._eojgc, self._eojcc, self._eojci, GET, opc
        )
        if not response:
            return None
        edt = self._api._state[self._host]["instances"][self._eojgc][self._eojcc][
            self._eojci
        ][epc]
        return edt

    """
    setMessage is used to fire ECHONET set messages to set Node information
    Assumes one OPC is sent per message.

    :param tx_epc: EPC byte code for the request.
    :param tx_edt: EDT data relevant to the request.
    :return: True if sucessful, false if request message failed
    """

    async def setMessage(self, epc: int, edt: Any, pdc: int = 1) -> bool:
        """Set a property value on the device.

        Args:
            epc: EPC byte code for the request
            edt: EDT data relevant to the request
            pdc: Property Data Count (default: 1)

        Returns:
            True if successful, False if request failed
        """
        opc = [{"EPC": epc, "PDC": pdc, "EDT": edt}]
        response = await self._api.echonetMessage(
            self._host, self._eojgc, self._eojcc, self._eojci, SETC, opc
        )
        if not response:
            return False
        return True

    """
    setMessage is used to fire ECHONET set messages to set Node information
    Assumes one OPC is sent per message.

    :param tx_epc: EPC byte code for the request.
    :param tx_edt: EDT data relevant to the request.
    :return: True if sucessful, false if request message failed
    """

    async def setMessages(self, opc: List[Dict[str, Any]]) -> bool:
        """Set multiple property values on the device.

        Args:
            opc: List of OPC dictionaries with EPC, PDC, and EDT

        Returns:
            True if successful, False if request failed
        """
        response = await self._api.echonetMessage(
            self._host, self._eojgc, self._eojcc, self._eojci, SETC, opc
        )
        if not response:
            return False
        return True

    """
    update is used as a way of producing a dict useful for API polling etc
    Data will either be formatted if you are using a specific class (e.g HomeAirConditioner)
    or returned as hex string values if you are using EchonetInstance

    :param attributes: optional list of EPC codes. eg [0x80, 0xBF], or a single code eg 0x80

    :return dict: A dict with the following attributes:
    {128: 'On', 160: 'medium-high', 176: 'heat', 129: '00', 130: '00004300',
    131: '0000060104a0c9a0fffe069719013001', 179: 19, 134: '06000006000000020000', 136: '42', 137: '0000'}

    :return string: if attribute is a single code then return value directly:
    eg:
    update(0x80)
    'on'

    """

    async def update(
        self,
        attributes: Optional[Union[int, List[int]]] = None,
        no_request: bool = False,
    ) -> Optional[Any]:
        """Update and return property values.

        Args:
            attributes: Optional list of EPC codes, or a single EPC code
            no_request: If True, skip network request (use cached data)

        Returns:
            Dictionary with property values, or None if no attributes specified
        """
        opc: List[Dict[str, Any]] = []
        if attributes is None:
            attributes = self.getGetProperties()
        if isinstance(attributes, int):
            list_attributes = [attributes]
            attributes = list_attributes
        returned_json_data: Dict[int, Any] = {}
        if no_request:
            response = True
        else:
            for value in attributes:
                if value in self.getGetProperties():
                    opc.append({"EPC": value})
            response = await self._api.echonetMessage(
                self._host, self._eojgc, self._eojcc, self._eojci, GET, opc
            )
        if response is not False:
            for epc in attributes:
                if epc not in list(
                    self._api._state[self._host]["instances"][self._eojgc][self._eojcc][
                        self._eojci
                    ].keys()
                ):
                    returned_json_data.update({epc: None})
                    continue
                elif epc in list(
                    EPC_SUPER_FUNCTIONS.keys()
                ):  # check if function is defined in the superset
                    returned_json_data.update(
                        {
                            epc: call_epc_function(
                                EPC_SUPER_FUNCTIONS[epc],
                                self._api._state[self._host]["instances"][self._eojgc][
                                    self._eojcc
                                ][self._eojci][epc],
                            )
                        }
                    )
                    continue
                elif epc in list(
                    EPC_SUPER.keys()
                ):  # return hex value if code exists in superset but no function found
                    returned_json_data.update(
                        {
                            epc: self._api._state[self._host]["instances"][self._eojgc][
                                self._eojcc
                            ][self._eojci][epc].hex()
                        }
                    )
                    continue
                elif epc in list(
                    self.EPC_FUNCTIONS.keys()
                ):  # check the class-specific EPC function table.
                    returned_json_data.update(
                        {
                            epc: call_epc_function(
                                self.EPC_FUNCTIONS[epc],
                                self._api._state[self._host]["instances"][self._eojgc][
                                    self._eojcc
                                ][self._eojci][epc],
                            )
                        }
                    )
                    # returned_json_data.update(
                    #     {
                    #         epc: self.EPC_FUNCTIONS[epc](
                    #             self._api._state[self._host]["instances"][self._eojgc][
                    #                 self._eojcc
                    #             ][self._eojci][epc]
                    #         )
                    #     }
                    # )
                    continue
                elif epc in list(
                    EPC_CODE[self._eojgc][self._eojcc].keys()
                ):  # return hex value if EPC code exists in class but no function found
                    returned_json_data.update(
                        {
                            epc: self._api._state[self._host]["instances"][self._eojgc][
                                self._eojcc
                            ][self._eojci][epc].hex()
                        }
                    )
        else:
            # Timeout Error
            raise TimeoutError("Pychonet UDP request timeout.")

        for epc in attributes:
            if epc not in list(returned_json_data.keys()):
                returned_json_data.update({epc: None})
        if (len(returned_json_data)) == 1 and len(attributes) == 1:
            return returned_json_data[attributes[0]]
        elif (len(returned_json_data)) == 0:
            return None
        return returned_json_data

    """
    getIdentificationNumber returns a number used to identify an object uniquely

    :return: Identification number as a string.
    """

    async def getIdentificationNumber(self) -> Optional[Any]:  # EPC 0x83
        """Get device identification number.

        Returns:
            Device UID, or None if not available
        """
        await self._api.getIdentificationNumber(
            self._host, self._eojgc, self._eojcc, self._eojci
        )
        return self._api._status[self._host]["instances"][self._eojgc][self._eojcc][
            self._eojci
        ][ENL_UID]

    """
    getManufacturer returns the manufacturer name if mapped, or Id otherwise

    :return: Manufacturer name as a string or echonet identification number as an int.
    """

    async def getManufacturer(self) -> Optional[Any]:  # EPC 0x8A
        """Get device manufacturer name.

        Returns:
            Manufacturer name or UID as string
        """
        return await self.update(ENL_MANUFACTURER)

    """
    getInstantaneousPower returns the current number of Wh the node is consuming.
    :return: Instantaneous Wh as an integer.
    """

    async def getInstantaneousPower(self) -> Optional[Any]:  # EPC 0x84
        """Get instantaneous power consumption.

        Returns:
            Instantaneous power in Wh, or None if not available
        """
        return await self.update(ENL_INSTANTANEOUS_POWER)

    """
    getCumulativePower returns the total number of Wh the node has used.
    Value should always increment up to 999,999,999 Wh after which resets to 0.
    :return: Cumulative Wh as an integer.
    """

    async def getCumulativePower(self) -> Optional[Any]:  # EPC 0x85
        """Get cumulative power consumption.

        Returns:
            Cumulative power in Wh, or None if not available
        """
        return await self.update(ENL_CUMULATIVE_POWER)

    """
    getCumulativeRuntime returns the total number of seconds the node has been running.
    :return: Runtime in seconds as an integer.
    """

    async def getCumulativeRuntime(self) -> Optional[Any]:  # EPC 0x9A
        """Get cumulative runtime.

        Returns:
            Runtime in seconds, or None if not available
        """
        return await self.update(ENL_CUMULATIVE_RUNTIME)

    """
    getOperationalStatus returns the ON/OFF state of the node

    :return: status as a string.
    """

    async def getOperationalStatus(self) -> Optional[Any]:  # EPC 0x80
        """Get operational status (on/off).

        Returns:
            Status string, or None if not available
        """
        return await self.getMessage(ENL_STATUS)

    """
    On sets the node to ON.

    """

    async def on(self) -> bool:  # EPC 0x80
        """Turn device on.

        Returns:
            True if successful
        """
        return await self.setMessage(ENL_STATUS, ENL_ON)

    """
    Off sets the node to OFF.

    """

    async def off(self) -> bool:  # EPC 0x80
        """Turn device off.

        Returns:
            True if successful
        """
        return await self.setMessage(ENL_STATUS, ENL_OFF)

    def getSetProperties(self) -> Any:  # EPC 0x9E
        """Get list of writable properties.

        Returns:
            List of EPC codes that can be written
        """
        return self._api._state[self._host]["instances"][self._eojgc][self._eojcc][
            self._eojci
        ][ENL_SETMAP]

    def getGetProperties(self) -> Any:  # EPC 0x9F
        """Get list of readable properties.

        Returns:
            List of EPC codes that can be read
        """
        return self._api._state[self._host]["instances"][self._eojgc][self._eojcc][
            self._eojci
        ][ENL_GETMAP]

    async def getAllPropertyMaps(self) -> Any:
        """Get all property maps.

        Returns:
            Dictionary of property maps, or None
        """
        return await self._api.getAllPropertyMaps(
            self._host, self._eojgc, self._eojcc, self._eojci
        )

    def register_async_update_callbacks(self, fn: Callable[[], Any]) -> None:
        """Register an async update callback.

        Args:
            fn: Callback function to be called on updates
        """
        self._api.register_async_update_callbacks(
            self._host, self._eojgc, self._eojcc, self._eojci, fn
        )