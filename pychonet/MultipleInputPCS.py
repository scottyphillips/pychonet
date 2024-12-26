from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int


class MultipleInputPCS(EchonetInstance):
    EPC_FUNCTIONS = {
        0xD0: [
            _int,
            {
                0x00: "System interconnected (reverse power flow acceptable)",
                0x01: "Output during a power outage",
                0x02: "System interconnected (reverse power flow not acceptable)",
            },
        ],  # "Grid connection status"
        0xE0: _int,  # "Measured cumulative amount of electric energy (normal direction)",
        0xE3: _int,  # "Measured cumulative amount of electric energy (reverse direction)",
        0xE7: _signed_int,  # "Measured instantaneous amount of electricity",
        # 0xE8: "Connected devices",
    }

    def __init__(self, host, api_connector, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0xA5
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
