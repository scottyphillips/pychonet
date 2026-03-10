# ElectricEnergySensor class for Echonet Lite protocol implementation in Python.
# This class represents an electric energy sensor device that can be monitored using the Echonet Lite protocol.
# It provides methods to get the operation status, cumulative amount of electric energy, and various instantaneous electric power measurements.

# Author: [Your Name]
# Date: [Current Date]

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, DICT_30_ON_OFF

class ElectricEnergySensor(EchonetInstance):
    EPC_FUNCTIONS = {
        # Electric energy sensor class
        0x80: [_int, DICT_30_ON_OFF],  # "Operation status"
        0xE0: _int,  # "Cumulative amount of electric energy (0.001kWh)"
        0xE1: _int,  # "Medium-capacity sensor instantaneous electric power (W)"
        0xE2: _int,  # "Small-capacity sensor instantaneous electric power (0.1 W)"
        0xE3: _int,  # "Large-capacity sensor instantaneous electric power (0.1 kW)"
        0xE4: _int,  # "Cumulative amount of electric energy measurement log (0.001kWh) for the past 24 hours"
        0xE5: _int,  # "Effective voltage value (V)"
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x00
        self._eojcc = 0x22
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def getCumulativeElectricEnergy(self):
        return await self.getMessage(0xE0)

    async def getMediumCapacityInstantaneousPower(self):
        return await self.getMessage(0xE1)

    async def getSmallCapacityInstantaneousPower(self):
        return await self.getMessage(0xE2)

    async def getLargeCapacityInstantaneousPower(self):
        return await self.getMessage(0xE3)

    async def getCumulativeElectricEnergyLog(self):
        return await self.getMessage(0xE4)

    async def getEffectiveVoltageValue(self):
        return await self.getMessage(0xE5)