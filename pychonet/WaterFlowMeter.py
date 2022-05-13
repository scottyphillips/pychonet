from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int, _to_string
import struct

def _0281D0(edt):
    # Water flow meter classification
    op_mode = int.from_bytes(edt, "big")
    values = {0x30: "Running Water",
              0x31: "Recycled Water",
              0x32: "Sewage Water",
              0x33: "Other Water"}
    return values.get(op_mode, "invalid_setting")

def _0281D1(edt):
    # Owner classification
    op_mode = int.from_bytes(edt, "big")
    values = {0x30: "Not specified",
              0x31: "Public waterworks company",
              0x32: "Private sector company",
              0x33: "Individual"}
    return values.get(op_mode, "invalid_setting")

def _0281E1(edt):
      # Unit for measured cumulative amounts of flowing water
    op_mode = int.from_bytes(edt, "big")
    values = {0x00: 1,
              0x01: 0.1,
              0x02: 0.01,
              0x03: 0.001,
              0x04: 0.0001,
              0x05: 0.00001,
              0x06: 0.000001}
    return values.get(op_mode, "invalid_setting")

# 0xE2: "Historical data of measured cumulative amounts of flowing water"
def _0281E2(edt):
      # return array x 48 unsigned long big-endian
      return [x[0] for x in struct.iter_unpack('>L',edt)]

class WaterFlowMeter(EchonetInstance):
    EPC_FUNCTIONS = {
        0xD0: _0281D0,   # "Water flow meter classification"
        0xD1: _0281D1,   # "Owner classification"
        0xE0: _int,      # "Measured  cumulative amount of flowing water"
        0xE1: _0281E1,   # "Unit for measured cumulative amounts of flowing water"
        0xE2: _0281E2,    # "Historical data of measured cumulative amounts of flowing water"
        0xE5: _to_string, # "ID number setting"
        0xE6: _to_string  # "Verification expiration information"
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x81
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
