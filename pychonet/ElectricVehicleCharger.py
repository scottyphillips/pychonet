from pychonet.EchonetInstance import EchonetInstance

"""Class for Electric Vehicle Charger Objects"""


class ElectricVehicleCharger(EchonetInstance):
    EPC_FUNCTIONS = {
        # 0xC0: "Dischargeable capacity of vehicle mounted battery 1",
        # 0xC1: "Dischargeable capacity of vehicle mounted battery 2",
        # 0xC2: "Remaining dischargeable capacity of vehicle mounted battery 1",
        # 0xC3: "Remaining dischargeable capacity of vehicle mounted battery 2",
        # 0xC4: "Remaining dischargeable capacity of vehicle mounted battery 3",
        # 0xC5: "Rated charge capacity",
        # 0xC6: "Rated discharge capacity",
        # 0xC7: "Vehicle connection and chargeable/dischargeable status",
        # 0xC8: "Minimum/maximum charging electric energy",
        # 0xC9: "Minimum/maximum discharging electric energy",
        # 0xCA: "Minimum/maximum charging current",
        # 0xCB: "Minimum/maximum discharging current",
        # 0xD0: "Used capacity of vehicle mounted battery 1",
        # 0xD1: "Used capacity of vehicle mounted battery 2",
        # 0xD2: "Rated voltage",
        # 0xD3: "Measured instantaneous charging/discharging electric energy",
        # 0xD4: "Measured instantaneous charging/discharging current",
        # 0xD5: "Measured instantaneous charging/discharging voltage",
        # 0xD6: "Measured cumulative amount of discharging electric energy",
        # 0xD7: "Cumulative amount of discharging electric energy reset setting",
        # 0xD8: "Measured cumulative amount of charging electric energy",
        # 0xD9: "Cumulative amount of charging electric energy reset setting",
        # 0xDA: "Operation mode setting",
        # 0xDB: "System-interconnecte d type",
        # 0xE2: "Remaining stored electricity of vehicle mounted battery 1",
        # 0xE3: "Remaining stored electricity of vehicle mounted battery 2",
        # 0xE4: "Remaining stored electricity of vehicle mounted battery 3",
        # 0xE7: "Charging amount setting 1",
        # 0xE9: "Charging amount setting 2",
        # 0xEB: "Charging electric energy setting",
        # 0xEC: "Discharging electric energy setting",
        # 0xED: "Charging current setting",
        # 0xEE: "Discharging current setting",
        # 0xEF: "Rated voltage (Independent)",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02  # Housing/facility-related device group
        self._eojcc = 0x7E  # Electric vehicle charger/discharger’
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
