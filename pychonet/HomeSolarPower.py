from pychonet.EchonetInstance import EchonetInstance

class HomeSolarPower(EchonetInstance):
    def __init__(self, netif, instance = 0x1):
        self.eojgc = 0x02
        self.eojcc = 0x79
        EchonetInstance.__init__(self, self.eojgc, self.eojcc, instance, netif)

    def getMeasuredInstantPower(self):
        return int.from_bytes(self.getSingleMessageResponse(0xE0), 'big')

    def getMeasuredCumulPower(self):
        return int.from_bytes(self.getSingleMessageResponse(0xE1), 'big')
