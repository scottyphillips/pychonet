from deprecated import deprecated

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DICT_30_ON_OFF,
    _hh_mm,
    _int,
    _signed_int,
)


FAN_OPERATION = {0x31: "off", 0x32: "weak", 0x33: "strong"}
HEAT_STORAGE_ABILITY = {0x30: "available", 0x31: "not available"}
RADIATION_METHOD = {0x30: "With fan", 0x31: "Without fan"}
CHILD_LOCK = {0x30: "enabled", 0x31: "disabled"}


def _air_temperature(edt):
    if len(edt) != 1:
        return None
    value = _signed_int(edt)
    return value if -127 <= value <= 125 else None


def _stored_heat_temperature(edt):
    if len(edt) != 2:
        return None
    value = _signed_int(edt)
    return value if -200 <= value <= 1000 else None


def _rated_power(edt):
    if len(edt) != 8:
        return None
    powers = [_int(edt[index : index + 2]) for index in range(0, 8, 2)]
    return {
        name: value if value <= 0xFFFD else None
        for name, value in zip(
            ("heat_storage", "control", "weak_airflow", "strong_airflow"), powers
        )
    }


# Static methods for ElectricStorageHeater
@deprecated(reason="Scheduled for removal.")
def _0155B3(payload):
    return _int(payload)


@deprecated(reason="Scheduled for removal.")
def _0155B8(payload):
    return _int(payload)


@deprecated(reason="Scheduled for removal.")
def _0155BB(payload):
    return _air_temperature(payload)


@deprecated(reason="Scheduled for removal.")
def _0155BE(payload):
    return _air_temperature(payload)


def _0155A0(payload):
    return _int(payload)


@deprecated(reason="Scheduled for removal.")
def _0155A1(payload):
    return _int(payload, FAN_OPERATION)


@deprecated(reason="Scheduled for removal.")
def _0155C0(payload):
    return _int(payload, DICT_30_ON_OFF)


@deprecated(reason="Scheduled for removal.")
def _0155C1(payload):
    return _int(payload)


@deprecated(reason="Scheduled for removal.")
def _0155C2(payload):
    return _stored_heat_temperature(payload)


@deprecated(reason="Scheduled for removal.")
def _0155C3(payload):
    return _int(payload, DICT_30_ON_OFF)


@deprecated(reason="Scheduled for removal.")
def _0155C4(payload):
    return _int(payload, HEAT_STORAGE_ABILITY)


@deprecated(reason="Scheduled for removal.")
def _0155C5(payload):
    return _int(payload)


@deprecated(reason="Scheduled for removal.")
def _0155C6(payload):
    return _hh_mm(payload)


@deprecated(reason="Scheduled for removal.")
def _0155C7(payload):
    return _int(payload, RADIATION_METHOD)


@deprecated(reason="Scheduled for removal.")
def _0155C8(payload):
    return _int(payload, CHILD_LOCK)


@deprecated(reason="Scheduled for removal.")
def _0155D0(payload):
    return _int(payload)


@deprecated(reason="Scheduled for removal.")
def _0155D1(payload):
    return _hh_mm(payload)


@deprecated(reason="Scheduled for removal.")
def _0155D2(payload):
    return _hh_mm(payload)


@deprecated(reason="Scheduled for removal.")
def _0155D3(payload):
    return _int(payload)


class ElectricStorageHeater(EchonetInstance):
    class_codes = {"class_group_code": 0x01, "class_code": 0x55}

    EPC_FUNCTIONS = {
        0xB3: _int,
        0xB8: _rated_power,
        0xBB: _air_temperature,
        0xBE: _air_temperature,
        0xA0: _int,
        0xA1: [_int, FAN_OPERATION],
        0xC0: [_int, DICT_30_ON_OFF],
        0xC1: _int,
        0xC2: _stored_heat_temperature,
        0xC3: [_int, DICT_30_ON_OFF],
        0xC4: [_int, HEAT_STORAGE_ABILITY],
        0xC5: _int,
        0xC6: _int,
        0xC7: [_int, RADIATION_METHOD],
        0xC8: [_int, CHILD_LOCK],
        0xD0: _int,
        0xD1: _hh_mm,
        0xD2: _hh_mm,
        0xD3: _int,
        0xD4: _hh_mm,
        0xD5: _hh_mm,
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = self.class_codes["class_group_code"]
        self._eojcc = self.class_codes["class_code"]
        super().__init__(host, self._eojgc, self._eojcc, instance, api_connector)

    async def getTemperatureSetting(self):
        return await self.getMessage(0xB3)

    async def getRatedPowerConsumption(self):
        return await self.getMessage(0xB8)

    async def getMeasuredIndoorTemperature(self):
        return await self.getMessage(0xBB)

    async def getMeasuredOutdoorTemperature(self):
        return await self.getMessage(0xBE)

    async def getAirFlowRateSetting(self):
        return await self.getMessage(0xA0)

    async def setAirFlowRateSetting(self, setting):
        await self.setMessage(0xA0, setting)

    async def getFanOperationStatus(self):
        return await self.getMessage(0xA1)

    async def setFanOperationStatus(self, status):
        await self.setMessage(0xA1, status)

    async def getHeatStorageOperationStatus(self):
        return await self.getMessage(0xC0)

    async def setHeatStorageOperationStatus(self, status):
        await self.setMessage(0xC0, status)

    async def getHeatStorageTemperatureSetting(self):
        return await self.getMessage(0xC1)

    async def setHeatStorageTemperatureSetting(self, temperature):
        await self.setMessage(0xC1, temperature, pdc=2)

    async def getMeasuredStoredHeatTemperature(self):
        return await self.getMessage(0xC2)

    async def getDaytimeHeatStorageSetting(self):
        return await self.getMessage(0xC3)

    async def setDaytimeHeatStorageSetting(self, setting):
        await self.setMessage(0xC3, setting)

    async def getDaytimeHeatStorageAbility(self):
        return await self.getMessage(0xC4)

    async def getMidnightPowerDurationSetting(self):
        return await self.getMessage(0xC5)

    async def setMidnightPowerDurationSetting(self, duration):
        await self.setMessage(0xC5, duration)

    async def getMidnightPowerStartTimeSetting(self):
        return await self.getMessage(0xC6)

    async def setMidnightPowerStartTimeSetting(self, time):
        await self.setMessage(0xC6, time)

    async def getRadiationMethod(self):
        return await self.getMessage(0xC7)

    async def setRadiationMethod(self, method):
        await self.setMessage(0xC7, method)

    async def getChildLockSetting(self):
        return await self.getMessage(0xC8)

    async def setChildLockSetting(self, setting):
        await self.setMessage(0xC8, setting)

    async def getFanTimer1Setting(self):
        return await self.getMessage(0xD0)

    async def setFanTimer1Setting(self, setting):
        await self.setMessage(0xD0, setting)

    async def getFanTimer1ONTimeSetting(self):
        return await self.getMessage(0xD1)

    async def setFanTimer1ONTimeSetting(self, time):
        await self.setMessage(0xD1, time, pdc=2)

    async def getFanTimer1OFFTimeSetting(self):
        return await self.getMessage(0xD2)

    async def setFanTimer1OFFTimeSetting(self, time):
        await self.setMessage(0xD2, time, pdc=2)

    async def getFanTimer2Setting(self):
        return await self.getMessage(0xD3)

    async def setFanTimer2Setting(self, setting):
        await self.setMessage(0xD3, setting)

    async def getFanTimer2ONTimeSetting(self):
        return await self.getMessage(0xD4)

    async def setFanTimer2ONTimeSetting(self, time):
        await self.setMessage(0xD4, time, pdc=2)

    async def getFanTimer2OFFTimeSetting(self):
        return await self.getMessage(0xD5)

    async def setFanTimer2OFFTimeSetting(self, time):
        await self.setMessage(0xD5, time, pdc=2)
