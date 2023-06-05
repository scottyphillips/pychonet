from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int

ENL_SCENE = 0xC0
ENL_SCENE_MAX = 0xC1

class LightingSystem(EchonetInstance):
    EPC_FUNCTIONS = {
        0xB0: _int,  # Illuminance level setting
        0xC0: _int,  # Scene control setting
        0xC1: _int,  # Max scene control setting
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02  # Housing/facility-related device group
        self._eojcc = 0xA3  # Lighting System class
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
