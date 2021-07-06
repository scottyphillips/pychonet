from EchonetInstance import EchonetInstance
from ..functions import getOpCode

"""Class for Electric Vehicle Charger Objects"""
class ElectricVehicleCharger(EchoNetNode):

    def __init__(self, netif, instance = 0x1):
        self.eojgc = 0x02 # Housing/facility-related device group
        self.eojcc = 0x7e # Electric vehicle charger/discharger’
        EchonetInstance.__init__(self, self.eojgc, self.eojcc, instance, netif)
