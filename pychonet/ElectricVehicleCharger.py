from pychonet.EchonetInstance import EchonetInstance

"""Class for Electric Vehicle Charger Objects"""
class ElectricVehicleCharger(EchonetInstance):

    def __init__(self, host, api_connector = None, instance = 0x1):
        self._eojgc = 0x02 # Housing/facility-related device group
        self._eojcc = 0x7e # Electric vehicle charger/discharger’
        EchonetInstance.__init__(self, host, self._eojgc, self._eojcc, instance, api_connector)
