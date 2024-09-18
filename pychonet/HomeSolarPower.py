from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int


# 0xD0 System-interconnected type
@deprecated(reason="Scheduled for removal.")
def _0279D0(edt):
    return _int(
        edt,
        {
            0x00: "System interconnected (reverse power flow acceptable)",
            0x01: "Independent",
            0x02: "System interconnected (reverse power flow not acceptable)",
            0x03: "Unknown",
        },
    )


# 0xD1 Output power restraint status
@deprecated(reason="Scheduled for removal.")
def _0279D1(edt):
    return _int(
        edt,
        {
            0x41: "Ongoing restraint (output power control)",
            0x42: "Ongoing restraint (except output power control)",
            0x43: "Ongoing restraint (reason for restraint unknown)",
            0x44: "Not restraining",
            0x45: "Unknown",
        },
    )


class HomeSolarPower(EchonetInstance):
    EPC_FUNCTIONS = {
        0xA0: _int,  # "Output power control setting 1",
        0xA1: _int,  # "Output power control setting 2",
        # 0xA2: "Function to control purchase surplus electricity setting",
        # 0xB0: "Output power controlling schedule",
        # 0xB1: "Next access date and time",
        # 0xB2: "Function to control the type of surplus electricity purchase",
        # 0xB3: "Output power change time setting value",
        # 0xB4: "Upper limit clip setting value",
        # 0xC0: "Operation power factor setting value",
        # 0xC1: "FIT contract type",
        # 0xC2: "Self-consumption type",
        # 0xC3: "Capacity approved by equipment",
        # 0xC4: "Conversion coefficient",
        0xD0: [
            _int,
            {
                0x00: "System interconnected (reverse power flow acceptable)",
                0x01: "Independent",
                0x02: "System interconnected (reverse power flow not acceptable)",
                0x03: "Unknown",
            },
        ],
        0xD1: [
            _int,
            {
                0x41: "Ongoing restraint (output power control)",
                0x42: "Ongoing restraint (except output power control)",
                0x43: "Ongoing restraint (reason for restraint unknown)",
                0x44: "Not restraining",
                0x45: "Unknown",
            },
        ],
        0xE0: _int,
        0xE1: _int,
        0xE2: _int,
        0xE3: _int,
        0xE4: _int,
        0xE5: _int,
        0xE6: _int,
        0xE7: _int,
        0xE8: _int,
        0xE9: _int,
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
