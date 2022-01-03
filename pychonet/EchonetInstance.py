import asyncio
from pychonet.echonetapiclient import ECHONETAPIClient
from pychonet.lib.const import (
    GET, SETC,
    ENL_GETMAP, ENL_SETMAP,
    ENL_STATUS, ENL_OFF, ENL_ON,
    ENL_UID, ENL_MANUFACTURER,
    ENL_INSTANTANEOUS_POWER, ENL_CUMULATIVE_POWER,
    ENL_CUMULATIVE_RUNTIME
)
from pychonet.lib.epc_functions import EPC_SUPER_FUNCTIONS
from pychonet.lib.epc import EPC_CODE, EPC_SUPER

"""
Superclass for Echonet instance objects.
"""
class EchonetInstance:

    EPC_FUNCTIONS = {}
    """
    Constructs an object to represent an Echonet lite instance .

    :param eojgc: Echonet group code
    :param eojcc: Echonet class code
    :param instance: Instance ID
    :param netif: IP address of node
    """
    def __init__(self, host, eojgc, eojcc, instance, api_connector=None):
        self._host = host
        self._eojgc = eojgc
        self._eojcc = eojcc
        self._eojci = instance
        self._api = api_connector

        #TODO self instntiate the API connector for backwards compatability with the older libary

    """
    getMessage is used to fire a single ECHONET get messages to get Node information
    Assumes one EPC is sent per message.

    :param tx_epc: EPC byte code for the request.
    :return: the deconstructed payload for the response

    """
    async def getMessage(self, epc, pdc = 0x00):
        opc = [{'EPC': epc, 'PDC': pdc}]
        response = await self._api.echonetMessage(self._host, self._eojgc, self._eojcc, self._eojci, GET, opc)
        if not response:
            return False
        edt = self._api._state[self._host]["instances"][self._eojgc][self._eojcc][self._eojci][epc]
        return edt

    """
    setMessage is used to fire ECHONET set messages to set Node information
    Assumes one OPC is sent per message.

    :param tx_epc: EPC byte code for the request.
    :param tx_edt: EDT data relevant to the request.
    :return: True if sucessful, false if request message failed
    """
    async def setMessage(self, epc, edt, pdc = 0x01):
        opc = [{'EPC': epc, 'PDC': pdc, 'EDT': edt}]
        response = await self._api.echonetMessage(self._host, self._eojgc, self._eojcc, self._eojci, SETC, opc)
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
    async def setMessages(self, opc):
        response = await self._api.echonetMessage(self._host, self._eojgc, self._eojcc, self._eojci, SETC, opc)
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
    async def update(self, attributes=None):
        opc = []
        if attributes == None:
            attributes = self.getGetProperties()
        if isinstance(attributes, int):
            list_attributes = [attributes]
            attributes = list_attributes
        returned_json_data = {}
        for value in attributes:
          if value in self.getGetProperties():
            opc.append({'EPC': value})
        response = await self._api.echonetMessage(self._host, self._eojgc, self._eojcc, self._eojci, GET, opc)
        if response is not False:
             for epc in attributes:
                 if epc not in list(self._api._state[self._host]["instances"][self._eojgc][self._eojcc][self._eojci].keys()):
                     returned_json_data.update({epc: False})
                     continue
                 elif epc in list(EPC_SUPER_FUNCTIONS.keys()): # check if function is defined in the superset
                     returned_json_data.update({epc: EPC_SUPER_FUNCTIONS[epc](self._api._state[self._host]["instances"][self._eojgc][self._eojcc][self._eojci][epc])})
                     continue
                 elif epc in list(EPC_SUPER.keys()): # return hex value if code exists in superset but no function found
                     returned_json_data.update({epc: self._api._state[self._host]["instances"][self._eojgc][self._eojcc][self._eojci][epc].hex()})
                     continue
                 elif epc in list(self.EPC_FUNCTIONS.keys()): # check the class-specific EPC function table.
                     returned_json_data.update({epc: self.EPC_FUNCTIONS[epc](self._api._state[self._host]["instances"][self._eojgc][self._eojcc][self._eojci][epc])})
                     continue
                 elif epc in list(EPC_CODE[self._eojgc][self._eojcc].keys()): # return hex value if EPC code exists in class but no function found
                     returned_json_data.update({epc: self._api._state[self._host]["instances"][self._eojgc][self._eojcc][self._eojci][epc].hex()})
        for epc in attributes:
             if epc not in list(returned_json_data.keys()):
                 returned_json_data.update({epc: False})
        if(len(returned_json_data)) == 1 and len(attributes) == 1:
             return returned_json_data[attributes[0]]
        elif(len(returned_json_data)) == 0:
             return False
        return returned_json_data

    """
    getIdentificationNumber returns a number used to identify an object uniquely

    :return: Identification number as a string.
    """
    async def getIdentificationNumber(self): # EPC 0x83
        await self._api.getIdentificationNumber(self._host, self._eojgc, self._eojcc, self._eojci)
        return self._api._status[self._host]["instances"][self._eojgc][self._eojcc][self._eojci][ENL_UID]

    """
    getManufacturer returns the manufacturer name if mapped, or Id otherwise

    :return: Manufacturer name as a string or echonet identification number as an int.
    """
    async def getManufacturer(self): # EPC 0x8A
        return await self.update(ENL_MANUFACTURER)

    """
    getInstantaneousPower returns the current number of Wh the node is consuming.
    :return: Instantaneous Wh as an integer.
    """
    async def getInstantaneousPower(self): # EPC 0x84
        return self.update(ENL_INSTANTANEOUS_POWER)

    """
    getCumulativePower returns the total number of Wh the node has used.
    Value should always increment up to 999,999,999 Wh after which resets to 0.
    :return: Cumulative Wh as an integer.
    """
    async def getCumulativePower(self): # EPC 0x85
        return self.update(ENL_CUMULATIVE_POWER)

    """
    getCumulativeRuntime returns the total number of seconds the node has been running.
    :return: Runtime in seconds as an integer.
    """
    async def getCumulativeRuntime(self): # EPC 0x9A
        return await self.update(ENL_CUMULATIVE_RUNTIME)

    """
    getOperationalStatus returns the ON/OFF state of the node

    :return: status as a string.
    """
    async def getOperationalStatus(self): # EPC 0x80
        return await self.getMessage(ENL_STATUS)

    """
    setOperationalStatus sets the ON/OFF state of the node

    :param status: True if On, False if Off.
    """
    async def setOperationalStatus(self, status):
        if status == 'on' or status == ENL_ON or status == True:
            return await self.setMessage(ENL_STATUS, ENL_ON)
        elif status == 'of' or status == ENL_OFF or status == False:
            return await self.setMessage(ENL_STATUS, ENL_OFF)

    """
    On sets the node to ON.

    """
    async def on(self): # EPC 0x80
        return await self.setMessage(ENL_STATUS, ENL_ON)

    """
    Off sets the node to OFF.

    """
    async def off(self): # EPC 0x80
        return await self.setMessage(ENL_STATUS, ENL_OFF)

    def getSetProperties(self): # EPC 0x9E
        return self._api._state[self._host]["instances"][self._eojgc][self._eojcc][self._eojci][ENL_SETMAP]

    def getGetProperties(self): # EPC 0x9F
        return self._api._state[self._host]["instances"][self._eojgc][self._eojcc][self._eojci][ENL_GETMAP]

    async def getAllPropertyMaps(self):
        return await self._api.getAllPropertyMaps(self._host, self._eojgc, self._eojcc, self._eojci)
