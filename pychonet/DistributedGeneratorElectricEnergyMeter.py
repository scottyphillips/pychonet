# pychonet/DistributedGeneratorElectricEnergyMeter.py
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    _int,
    _signed_int,
    _yyyy_mm_dd,
)

def _028ED4(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {
        0x00: 1,
        0x01: 0.1,
        0x02: 0.01,
        0x03: 0.001,
        0x04: 0.0001,
        0x0A: 10,
        0x0B: 100,
        0x0C: 1000,
        0x0D: 10000,
    }
    return values.get(op_mode, None)

class DistributedGeneratorElectricEnergyMeter(EchonetInstance):
    EPC_FUNCTIONS = {
        0x80: _int, # "Operation status"
        0x98: _yyyy_mm_dd, # "Current date setting"
        0xD4: _028ED4,  # "Unit for cumulative amount of electric energy"
        0xE0: _int, # "Measured cumulative amount of electric energy (AC input)"
        # 0xE1: "Historical data of measured cumulative amounts of electric energy (AC input)"
        0xE2: _int, # "Measured cumulative amount of electric energy (AC output)"
        # 0xE3: "Historical data of measured cumulative amounts of electric energy (AC output)"
        0xE4: _int, # "Measured cumulative amount of electric energy (output during a power outage)"
        # 0xE5: "Historical data of measured cumulative amounts of electric energy (output during a power outage)"
        # 0xE6: "Cumulative amounts of electric energy measured at fixed time (AC input)"
        # 0xE7: "Cumulative amounts of electric energy measured at every 30 minute (AC output)"
        # 0xE8: "Cumulative amounts of electric energy measured at every 30 minute (output during a power outage)"
        0xE9: _signed_int, # "Measured instantaneous electric power (AC input/output)"
        0xEA: _signed_int, # "Measured instantaneous electric power (independent output)"
    }

    def __init__(self, host, api_connector=None, instance=0x01):
        self._eojgc = 0x02
        self._eojcc = 0x8E
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
