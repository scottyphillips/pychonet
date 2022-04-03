from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int
import struct

# 0xE2: "Cumulative amount of gas consumption measurement log"
def _0282E2(edt):
      # return array x 48 unsigned long big-endian
      return [x[0] for x in struct.iter_unpack('>L',edt)]


class GasMeter(EchonetInstance):
    EPC_FUNCTIONS = {
        0xE0: _int,  # 0xE0: "Cumulative amount of gas consumption measurement value"
        0xE2: _0282E2  #_0282E2
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x82
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
