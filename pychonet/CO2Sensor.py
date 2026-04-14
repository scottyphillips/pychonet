from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int


class CO2Sensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # CO2 sensor class
        0x80: [_int, {0x30: 'ON', 0x31: 'OFF'}],  # "Operation status",
        0xE0: _int,  # "Measured value of CO2 concentration (ppm)",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x1B
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        return await self.setMessage(0x80, status)

    async def getCO2Concentration(self):
        return await self.getMessage(0xE0)