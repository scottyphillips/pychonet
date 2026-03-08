# pychonet/DistributedGeneratorElectricEnergyMeter.py
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    _int,
    _signed_int,
    _to_string,
    _yyyy_mm_dd,
    _hh_mm,
)

#ENL_DGEEM_COEF = 0xD3
#ENL_DGEEM_DIGITS = 0xD7
ENL_DGEEM_ENG_UNIT = 0xD4
ENL_DGEEM_ENG_ACI = 0xE0
ENL_DGEEM_ENG_ACO = 0xE2
ENL_DGEEM_ENG_INO = 0xE4
ENL_DGEEM_INSTANT_AIO = 0xE9
ENL_DGEEM_INSTANT_INO = 0xEA


class DistributedGeneratorElectricEnergyMeter(EchonetInstance):
    """
    ECHONET Lite: 0x02-0x8E
    Distributed generator electric energy meter（分布型発電電力量計）
    02,8E,01,分散型電源電力量メータ,72,D4,Unit for cumulative amount of electric energy,?,unsignedChar
    02,8E,01,分散型電源電力量メータ,72,E0,Measured cumulative amount of electric energy (AC input),W,unsignedLong
    02,8E,01,分散型電源電力量メータ,72,E2,Measured cumulative amount of electric energy (AC output),W,unsignedLong
    02,8E,01,分散型電源電力量メータ,72,E4,Measured cumulative amount of electric energy (independent output),W,unsignedLong
    02,8E,01,分散型電源電力量メータ,72,E9,Measured instantaneous electric power (AC input/output),W,signedLong
    02,8E,01,分散型電源電力量メータ,72,EA,Measured instantaneous electric power (independent output),W,signedLong
    """

    EPC_FUNCTIONS = {
        0x80: _int, # Operation status
        0x98: _yyyy_mm_dd, # Current date setting
        0xD1: _to_string, # Device ID
        0xD4: [
            _int,
            {
                0x00: 1,
                0x01: 0.1,
                0x02: 0.01,
                0x03: 0.001,
                0x04: 0.0001,
                0x0A: 10,
                0x0B: 100,
                0x0C: 1000,
                0x0D: 10000,
            },
        ], # Unit for cumulative amount of electric energy
        0xE0: _int,         # Measured cumulative amount of electric energy (AC input)
        0xE2: _int,         # Measured cumulative amount of electric energy (AC output)
        0xE4: _int,         # Measured cumulative amount of electric energy (independent output)
        0xE9: _signed_int,  # Measured instantaneous electric power (AC input/output)
        0xEA: _signed_int,  # Measured instantaneous electric power (independent output)
    }

    def __init__(self, host, api_connector=None, instance=0x01):
        self._eojgc = 0x02
        self._eojcc = 0x8E
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    async def getUnit(self):
        return await self.getMessage(ENL_DGEEM_ENG_UNIT)