from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import DICT_41_ON_OFF, _int

# ----- Fuel Cell -------


@deprecated(reason="Scheduled for removal.")
def _027CCA(edt):
    return _int(edt, DICT_41_ON_OFF)


@deprecated(reason="Scheduled for removal.")
def _027CCB(edt):
    return _int(
        edt,
        {
            0x41: "Generating",
            0x42: "Stopped",
            0x43: "Starting",
            0x44: "Stopping",
            0x45: "Idling",
        },
    )


@deprecated(reason="Scheduled for removal.")
def _027CD0(edt):
    return _int(
        edt,
        {
            0x01: "System interconnected (reverse power flow acceptable)",
            0x02: "Independent",
            0x03: " System interconnected (reverse power flow not acceptable)",
        },
    )


class FuelCell(EchonetInstance):
    EPC_FUNCTIONS = {
        0xC1: _int,  # Measured temperature of water in water heater
        0xC2: _int,  # Rated power generation output
        0xC3: _int,  # Heating value of hot water storage tank
        0xC4: _int,  # Measured instantaneous power generation output
        0xC5: _int,  # Measured cumulative power generation output
        # set only 0xC6: # Cumulative power generation output reset setting
        0xC7: _int,  # Measured instantaneous gas consumption
        0xC8: _int,  # Measured cumulative gas consumption
        # set only 0xC9: # Cumulative gas consumption reset setting
        0xCA: [_int, DICT_41_ON_OFF],  # Power generation setting
        0xCB: [
            _int,
            {
                0x41: "Generating",
                0x42: "Stopped",
                0x43: "Starting",
                0x44: "Stopping",
                0x45: "Idling",
            },
        ],  # Power generation status
        0xCC: _int,  # Measured in-house instantaneous power consumption
        0xCD: _int,  # Measured in-house cumulative power consumption
        # set only 0xCE: # In-house cumulative power consumption reset
        0xD0: [
            _int,
            {
                0x01: "System interconnected (reverse power flow acceptable)",
                0x02: "Independent",
                0x03: " System interconnected (reverse power flow not acceptable)",
            },
        ],  # System interconnected type
        0xE1: _int,  # Measured remaining hot water amount
        0xE2: _int,  # Tank capacity
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x7C
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
