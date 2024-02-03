import asyncio
from types import _ReturnT_co
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

    @property
    async def operation_status(self):
        return await self.getMessage(0x80)

    @operation_status.setter
    async def operation_status(self, value):
        await self.setMessage(0x80, value)

    @property
    async def automatic_temperature_control_setting(self):
        return await self.getMessage(0xB1)

    @automatic_temperature_control_setting.setter
    async def automatic_temperature_control_setting(self, value):
        await self.setMessage(0xB1, value)

    @property
    async def temperature_setting(self):
        return await self.getMessage(0xB3)

    @temperature_setting.setter
    async def temperature_setting(self, value):
        await self.setMessage(0xB3, value)

    @property
    async def measured_room_temperature(self):
        return await self.getMessage(0xBB)

    @measured_room_temperature.setter
    async def measured_room_temperature(self, value):
        await self.setMessage(0xBB, value)

    @property
    async def remotely_set_temperature(self):
        return await self.getMessage(0xBC)

    @remotely_set_temperature.setter
    async def remotely_set_temperature(self, value):
        await self.setMessage(0xBC, value)

    @property
    async def air_flow_rate_setting(self):
        return await self.getMessage(0xA0)

    @air_flow_rate_setting.setter
    async def air_flow_rate_setting(self, value):
        await self.setMessage(0xA0, value)
