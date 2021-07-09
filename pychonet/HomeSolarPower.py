from pychonet.EchonetInstance import EchonetInstance

def _0279e0(edt):
        return {'instantaneous_power': int.from_bytes(edt, 'big')}

def _0279e1(edt):
        return {'cumul_power': int.from_bytes(edt, 'big')}

class HomeSolarPower(EchonetInstance):
    def __init__(self, netif, instance = 0x1):
        self.eojgc = 0x02
        self.eojcc = 0x79
        EchonetInstance.__init__(self, self.eojgc, self.eojcc, instance, netif)

    def getMeasuredInstantPower(self):
        return _0279e0(self.getSingleMessageResponse(0xE0))

    def getMeasuredCumulPower(self):
        return _0279e1(self.getSingleMessageResponse(0xE1))
