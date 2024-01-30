from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int, _to_string
import struct


@deprecated(reason="Scheduled for removal.")
def _0281D0(edt):
    # Water flow meter classification
    return _int(
        edt,
        {
            0x30: "Running Water",
            0x31: "Recycled Water",
            0x32: "Sewage Water",
            0x33: "Other Water",
        },
    )


@deprecated(reason="Scheduled for removal.")
def _0281D1(edt):
    # Owner classification
    return _int(
        edt,
        {
            0x30: "Not specified",
            0x31: "Public waterworks company",
            0x32: "Private sector company",
            0x33: "Individual",
        },
    )


@deprecated(reason="Scheduled for removal.")
def _0281E1(edt):
    # Unit for measured cumulative amounts of flowing water
    return _int(
        edt,
        {
            0x00: 1,
            0x01: 0.1,
            0x02: 0.01,
            0x03: 0.001,
            0x04: 0.0001,
            0x05: 0.00001,
            0x06: 0.000001,
        },
        None,
    )


# 0xE2: "Historical data of measured cumulative amounts of flowing water"
def _0281E2(edt):
    # return array x 48 unsigned long big-endian
    return [x[0] for x in struct.iter_unpack(">L", edt)]


class WaterFlowMeter(EchonetInstance):
    EPC_FUNCTIONS = {
        0xD0: [
            _int,
            {
                0x30: "Running Water",
                0x31: "Recycled Water",
                0x32: "Sewage Water",
                0x33: "Other Water",
            },
        ],  # "Water flow meter classification"
        0xD1: [
            _int,
            {
                0x30: "Not specified",
                0x31: "Public waterworks company",
                0x32: "Private sector company",
                0x33: "Individual",
            },
        ],  # "Owner classification"
        0xE0: _int,  # "Measured  cumulative amount of flowing water"
        0xE1: [
            _int,
            {
                0x00: 1,
                0x01: 0.1,
                0x02: 0.01,
                0x03: 0.001,
                0x04: 0.0001,
                0x05: 0.00001,
                0x06: 0.000001,
            },
            None,
        ],  # "Unit for measured cumulative amounts of flowing water"
        0xE2: _0281E2,  # "Historical data of measured cumulative amounts of flowing water"
        0xE5: _to_string,  # "ID number setting"
        0xE6: _to_string,  # "Verification expiration information"
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x81
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
