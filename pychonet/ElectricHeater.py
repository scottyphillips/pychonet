import asyncio
from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DATA_STATE_OFF,
    DATA_STATE_ON,
    DICT_41_AUTO_8_SPEEDS,
    DICT_41_AUTO_NONAUTO,
    DICT_41_ON_OFF,
    _int,
    _hh_mm,
    _signed_int,
)


def _014290(data):
    # Logic to interpret data for EPC 0x90
    return _int(data, DICT_41_AUTO_NONAUTO)


def _0142A0(data):
    # Logic to interpret data for EPC 0xA0
    return _int(data, DICT_41_AUTO_8_SPEEDS)


@deprecated(reason="Scheduled for removal.")
def _0142B1(data):
    # Logic to interpret data for EPC 0xB1
    return _int(data, DICT_41_ON_OFF)


@deprecated(reason="Scheduled for removal.")
def _014294(data):
    # Logic to interpret data for EPC 0xB1
    return _int(data, DICT_41_ON_OFF)


class ElectricHeater(EchonetInstance):
    EOJGC = 0x01
    EOJCC = 0x42

    EPC_FUNCTIONS = {
        0x80: _int,
        0xB1: [_int, DICT_41_AUTO_NONAUTO],
        0xB3: _int,
        0xBB: _signed_int,
        0xBC: _int,
        0xA0: [_int, DICT_41_AUTO_8_SPEEDS],
        0x90: [_int, DICT_41_ON_OFF],
        0x91: _hh_mm,
        0x92: _hh_mm,
        0x94: [_int, DICT_41_ON_OFF],
        0x95: _hh_mm,
        0x96: _hh_mm,
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = self.EOJGC
        self._eojcc = self.EOJCC
        super().__init__(host, self._eojgc, self._eojcc, instance, api_connector)

    async def getOperationStatus(self):
        return await self.getMessage(0x80)

    async def setOperationStatus(self, status):
        return await self.setMessage(0x80, status)

    async def getAutomaticTemperatureControlSetting(self):
        return await self.getMessage(0xB1)

    async def setAutomaticTemperatureControlSetting(self, setting):
        return await self.setMessage(0xB1, setting)

    async def getTemperatureSetting(self):
        return await self.getMessage(0xB3)

    async def setTemperatureSetting(self, temperature):
        return await self.setMessage(0xB3, temperature)

    async def getMeasuredRoomTemperature(self):
        return await self.getMessage(0xBB)

    async def setMeasuredRoomTemperature(self, temperature):
        return await self.setMessage(0xBB, temperature)

    async def getRemotelySetTemperature(self):
        return await self.getMessage(0xBC)

    async def setRemotelySetTemperature(self, temperature):
        return await self.setMessage(0xBC, temperature)

    async def getAirFlowRateSetting(self):
        return await self.getMessage(0xA0)

    async def setAirFlowRateSetting(self, flow_rate):
        return await self.setMessage(0xA0, flow_rate)
