from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int

ENL_DPM_ENG_NOR = 0xC0
ENL_DPM_ENG_REV = 0xC1
ENL_DPM_ENG_UNIT = 0xC2
ENL_DPM_DAY_GET_HISTORY = 0xC5
ENL_DPM_INSTANT_ENG = 0xC6
ENL_DPM_INSTANT_CUR = 0xC7
ENL_DPM_INSTANT_VOL = 0xC8
ENL_DPM_CHANNEL_SIMPLEX_CUMULATIVE_ENG = 0xB3
ENL_DPM_CHANNEL_SIMPLEX_INSTANT_ENG = 0xB7


def _0287C2(edt):
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


def _0287B3(edt):
    values = []
    for x in range(0, edt[1]):
        values.append(
            int.from_bytes(edt[x * 4 + 2 : (x + 1) * 4 + 2], "big", signed=False)
        )
    return {"start": edt[0], "range": edt[1], "values": values}


def _0287B7(edt):
    values = []
    for x in range(0, edt[1]):
        values.append(
            int.from_bytes(edt[x * 4 + 2 : (x + 1) * 4 + 2], "big", signed=True)
        )
    return {"start": edt[0], "range": edt[1], "values": values}


# def _0287xx(edt):
#     return "Not implemented"
#
# def _0287D0EF(edt):
#     return "Measurement channels not implemented"


def _0287C7(edt):
    r_phase = float(int.from_bytes(edt[0:2], "big", signed=True)) / 10  # R Phase
    t_phase = float(int.from_bytes(edt[2:4], "big", signed=True)) / 10  # T Phase
    if t_phase == 3276.6:
        t_phase = None
    return {"r_phase_amperes": r_phase, "t_phase_amperes": t_phase}


def _0287C8(edt):
    r_sn = float(int.from_bytes(edt[0:2], "big", signed=True)) / 10  # R Phase
    sn_t = float(int.from_bytes(edt[2:4], "big", signed=True)) / 10  # T Phase
    if sn_t == 6553.4:
        sn_t = None
    return {"r_sn_voltage": r_sn, "sn_t_voltage": sn_t}


class DistributionPanelMeter(EchonetInstance):
    EPC_FUNCTIONS = {
        0xC0: _int,  # "Measured cumulative amount of electric energy (normal direction)"
        0xC1: _int,  # "Measured cumulative amount of electric energy (reverse direction)"
        0xC2: _0287C2,  # "Unit for cumulative amounts of electric energy"
        #       0xC3: _0287xx,     # "Historical data of measured cumulative amounts of electric energy (normal direction)"
        #       0xC4: _0287xx,     # "Historical data of measured cumulative amounts of electric energy (reverse direction)"
        0xC5: _int,  # "Day for which the historical data of measured cumulative amounts of electric energy is to be retrieved"
        0xC6: _signed_int,  # "Measured instantaneous amount of electric energy"
        0xC7: _0287C7,  # "Measured instantaneous currents"
        0xC8: _0287C8,  # "Measured instantaneous voltages"
        #       0xD0: _0287D0EF,   # "Measurement channel 1"
        #       0xD1: _0287D0EF,   # "Measurement channel 2"
        #       0xD2: _0287D0EF,   # "Measurement channel 3"
        #       0xD3: _0287D0EF,   # "Measurement channel 4"
        #       0xD4: _0287D0EF,   # "Measurement channel 5"
        #       0xD5: _0287D0EF,   # "Measurement channel 6"
        #       0xD6: _0287D0EF,   # "Measurement channel 7"
        #       0xD7: _0287D0EF,   # "Measurement channel 8"
        #       0xD8: _0287D0EF,   # "Measurement channel 9"
        #       0xD9: _0287D0EF,   # "Measurement channel 10"
        #       0xDA: _0287D0EF,   # "Measurement channel 11"
        #       0xDB: _0287D0EF,   # "Measurement channel 12"
        #       0xDC: _0287D0EF,   # "Measurement channel 13"
        #       0xDD: _0287D0EF,   # "Measurement channel 14"
        #       0xDE: _0287D0EF,   # "Measurement channel 15"
        #       0xDF: _0287D0EF,   # "Measurement channel 16"
        #       0xE0: _0287D0EF,   # "Measurement channel 17"
        #       0xE1: _0287D0EF,   # "Measurement channel 18"
        #       0xE2: _0287D0EF,   # "Measurement channel 19"
        #       0xE3: _0287D0EF,   # "Measurement channel 20"
        #       0xE4: _0287D0EF,   # "Measurement channel 21"
        #       0xE5: _0287D0EF,   # "Measurement channel 22"
        #       0xE6: _0287D0EF,   # "Measurement channel 23"
        #       0xE7: _0287D0EF,   # "Measurement channel 24"
        #       0xE8: _0287D0EF,   # "Measurement channel 25"
        #       0xE9: _0287D0EF,   # "Measurement channel 26"
        #       0xEA: _0287D0EF,   # "Measurement channel 27"
        #       0xEB: _0287D0EF,   # "Measurement channel 28"
        #       0xEC: _0287D0EF,   # "Measurement channel 29"
        #       0xED: _0287D0EF,   # "Measurement channel 30"
        #       0xEE: _0287D0EF,   # "Measurement channel 31"
        #       0xEF: _0287D0EF,   # "Measurement channel 32"
        0xB0: _int,  # "Master rated capacity"
        0xB1: _int,  # "Number of measurement channels (simplex)"
        #       0xB2: _0287xx,     # "Channel range specification for cumulative amount of electric power consumption measurement (simplex)"
        0xB3: _0287B3,  # "Measured cumulative amount of electric power consumption list (simplex)"
        #       0xB4: _0287xx,     # "Channel range specification for instantaneous current measurement (simplex)"
        #       0xB5: _0287xx,     # "Measured instantaneous current list (simplex)"
        #       0xB6: _0287xx,     # "Channel range specification for instantaneous power consumption measurement (simplex)"
        0xB7: _0287B7,  # "Measured instantaneous power consumption list (simplex)"
        0xB8: _int,  # "Number of measurement channels (duplex)"
        #       0xB9: _0287xx,     # "Channel range specification for cumulative amount of electric power consumption measurement (duplex)"
        #       0xBA: _0287xx,     # "Measured cumulative amount of electric power consumption list (duplex)"
        #       0xBB: _0287xx,     # "Channel range specification for instantaneous current measurement (duplex)"
        #       0xBC: _0287xx,     # "Measured instantaneous current list (duplex)"
        #       0xBD: _0287xx,     # "Channel range specification for instantaneous power consumption measurement (duplex)"
        #       0xBE: _0287xx,     # "Measured instantaneous power consumption list (duplex)"
    }

    def __init__(self, host, api_connector, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x87
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
