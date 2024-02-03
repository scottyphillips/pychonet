from deprecated import deprecated
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import (
    DICT_41_PERMITTED_PROHIBITED,
    _int,
    _signed_int,
    _hh_mm,
    _to_string,
    _yyyy_mm_dd,
)


@deprecated(reason="Scheduled for removal.")
def _permission_setting(edt):
    return _int(
        edt,
        {
            0x41: "permitted",
            0x42: "Prohibited",
        },
    )


@deprecated(reason="Scheduled for removal.")
def _027DC1(edt):
    return _int(
        edt,
        {
            0x00: "other",
            0x01: "maximum",
            0x02: "surplus",
            0x03: "designatedPower",
            0x04: "designatedCurrent",
        },
    )


@deprecated(reason="Scheduled for removal.")
def _027DC2(edt):
    return _int(
        edt,
        {
            0x00: "other",
            0x01: "maximum",
            0x02: "loadFollowing",
            0x03: "designatedPower",
            0x04: "designatedCurrent",
        },
    )


def _max_min_int(edt):
    max = str(int.from_bytes(edt[0:4], "big"))
    min = str(int.from_bytes(edt[4:8], "big"))
    return max + "/" + min


def _max_min_short_int(edt):
    max = str(int.from_bytes(edt[0:2], "big"))
    min = str(int.from_bytes(edt[2:4], "big"))
    return max + "/" + min


@deprecated(reason="Scheduled for removal.")
def _027DCF(edt):
    return _int(
        edt,
        {
            0x41: "rapidCharging",
            0x42: "charging",
            0x43: "discharging",
            0x44: "standby",
            0x45: "test",
            0x46: "auto",
            0x48: "restart",
            0x49: "capacityRecalculation",
            0x40: "Other",
        },
    )


@deprecated(reason="Scheduled for removal.")
def _027DDB(edt):
    return _int(
        edt,
        {
            0x00: "reversePowerFlowAcceptable",
            0x01: "independent",
            0x02: "reversePowerFlowNotAcceptable",
        },
    )


@deprecated(reason="Scheduled for removal.")
def _027DE6(edt):
    return _int(
        edt,
        {
            0x00: "unknown",
            0x01: "lead",
            0x02: "ni_mh",
            0x03: "ni_cd",
            0x04: "Lithium",
            0x05: "zinc",
            0x06: "alkaline",
        },
    )


class StorageBattery(EchonetInstance):
    DICT_OPERATION_MODE = {
        0x41: "rapidCharging",
        0x42: "charging",
        0x43: "discharging",
        0x44: "standby",
        0x45: "test",
        0x46: "auto",
        0x48: "restart",
        0x49: "capacityRecalculation",
        0x40: "Other",
    }
    EPC_FUNCTIONS = {
        0x83: _to_string,  # Identification number
        0x97: _hh_mm,  # Current time setting
        0x98: _yyyy_mm_dd,  # Current date setting
        0xA0: _int,  # AC effective capacity (charging)
        0xA1: _int,  # AC effective capacity (discharging)
        0xA2: _int,  # AC chargeable capacity
        0xA3: _int,  # AC dischargeable capacity
        0xA4: _int,  # AC chargeable electric energy
        0xA5: _int,  # AC dischargeable electric energy
        0xA6: _int,  # AC charge upper limit setting
        0xA7: _int,  # AC discharge lower limit setting
        0xA8: _int,  # AC measured cumulative charging electric energy
        0xA9: _int,  # AC measured cumulative discharging electric energy"
        0xAA: _int,  # AC charge amount setting value
        0xAB: _int,  # AC discharge amount setting value
        0xC1: [
            _int,
            {
                0x00: "other",
                0x01: "maximum",
                0x02: "surplus",
                0x03: "designatedPower",
                0x04: "designatedCurrent",
            },
        ],  # Charging method
        0xC2: [
            _int,
            {
                0x00: "other",
                0x01: "maximum",
                0x02: "loadFollowing",
                0x03: "designatedPower",
                0x04: "designatedCurrent",
            },
        ],  # Discharging method
        0xC7: _int,  # AC rated electric energy
        0xC8: _max_min_int,  # Minimum/maximum charging electric power
        0xC9: _max_min_int,  # Minimum/maximum discharging electric power
        0xCA: _max_min_short_int,  # Minimum/maximum charging currentt
        0xCB: _max_min_short_int,  # Minimum/maximum discharging current
        0xCC: [
            _int,
            DICT_41_PERMITTED_PROHIBITED,
        ],  # Re-interconnection permission setting
        0xCD: [
            _int,
            DICT_41_PERMITTED_PROHIBITED,
        ],  # "Operation permission setting
        0xCE: [
            _int,
            DICT_41_PERMITTED_PROHIBITED,
        ],  # "Independent operation permission setting
        0xCF: [_int, DICT_OPERATION_MODE],  # Working operation status
        0xD0: _int,  # Rated electric energy
        0xD1: _int,  # Rated capacity
        0xD2: _int,  # Rated voltage
        0xD3: _signed_int,  # Measured instantaneous charging/discharging electric energy
        0xD4: _signed_int,  # Measured instantaneous charging/discharging current
        0xD5: _signed_int,  # Measured instantaneous charging/discharging voltage
        0xD6: _int,  # Measured cumulative discharging electric energy
        # set only 0xD7: "Measured cumulative discharging electric energy” reset setting",
        0xD8: _int,  # Measured cumulative charging electric energy
        # set only 0xD9: "Measured cumulative charging electric energy” reset setting",
        0xDA: [_int, DICT_OPERATION_MODE],  # Operation mode setting
        0xDB: [
            _int,
            {
                0x00: "reversePowerFlowAcceptable",
                0x01: "independent",
                0x02: "reversePowerFlowNotAcceptable",
            },
        ],  # System-interconnected type
        0xDC: _max_min_int,  # Minimum/maxim um charging power (Independent)
        0xDD: _max_min_int,  # Minimum/maxim um discharging power (Independent)
        0xDE: _max_min_short_int,  # Minimum/maxim um charging current (Independent)
        0xDF: _max_min_short_int,  # Minimum/maxim um discharging current (Independent)
        0xE0: _signed_int,  # Charging/discharging amount setting 1
        0xE1: _signed_int,  # Charging/discharging amount setting 2
        0xE2: _int,  # Remaining stored electricity 1
        0xE3: _int,  # Remaining stored electricity 2
        0xE4: _int,  # Remaining stored electricity 3
        0xE5: _int,  # Battery state of health
        0xE6: [
            _int,
            {
                0x00: "unknown",
                0x01: "lead",
                0x02: "ni_mh",
                0x03: "ni_cd",
                0x04: "Lithium",
                0x05: "zinc",
                0x06: "alkaline",
            },
        ],  # Battery type
        0xE7: _int,  # Charging amount setting 1
        0xE8: _int,  # Discharging amount setting 1
        0xE9: _int,  # Charging amount setting 2
        0xEA: _int,  # Discharging amount setting 2
        0xEB: _int,  # Charging electric energy setting
        0xEC: _int,  # Discharging electric energy setting
        0xED: _int,  # Charging current setting
        0xEE: _int,  # Discharging current setting
        0xEF: _int,  # Rated voltage (Independent)
    }

    # WORKING_OPERATION_STATES = {
    #     0x40: "Other",
    #     0x41: "Rapid charging",
    #     0x42: "Charging",
    #     0x43: "Discharging",
    #     0x44: "Standby",
    #     0x45: "Test",
    #     0x46: "Automatic",
    #     0x48: "Restart",
    #     0x49: "Effective capacity recalculation processing",
    # }

    # def _permission_setting(edt):
    #     op_mode = int.from_bytes(edt, "big")
    #     values = {
    #         0x41: "permitted",
    #         0x42: "Prohibited",
    #     }
    #     return values.get(op_mode, "Invalid setting")

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x7D
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
