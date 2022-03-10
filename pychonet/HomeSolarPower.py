from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int

# 0xD0 System-interconnected type
def _0279D0(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x00: "System interconnected (reverse power flow acceptable)",
              0x01: "Independent",
              0x02: "System interconnected (reverse power flow not acceptable)",
              0x03: "Unknown"}
    return values.get(op_mode, "Invalid setting")

# 0xD1 Output power restraint status
def _0279D1(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "Ongoing restraint (output power control)",
              0x42: "Ongoing restraint (except output power control)",
              0x43: "Ongoing restraint (reason for restraint unknown)",
              0x44: "Not restraining",
              0x45: "Unknown"}
    return values.get(op_mode, "Invalid setting")

class HomeSolarPower(EchonetInstance):
    EPC_FUNCTIONS = {
        0xD0: _0279D0,
        0xD1: _0279D1,
        0xE0: _int,
        0xE1: _int,
        0xE2: _int,
        0xE3: _int,
        0xE4: _int,
        0xE5: _int,
        0xE6: _int,
        0xE7: _int,
        0xE8: _int,
        0xE9: _int
    }

    def __init__(self, host, api_connector, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x79
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )

    def getMeasuredInstantPower(self):
        return self.getMessage(0xE0)

    def getMeasuredCumulPower(self):
        return self.getMessage(0xE1)
