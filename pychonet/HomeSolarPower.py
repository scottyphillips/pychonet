from pychonet.EchonetInstance import EchonetInstance

class HomeSolarPower(EchonetInstance):
    def __init__(self, host, api_connector, instance = 0x1):
        self._eojgc = 0x02
        self._eojcc = 0x79
        EchonetInstance.__init__(self, host, self._eojgc, self._eojcc, instance, api_connector)

    def getMeasuredInstantPower(self):
        return self.getMessage(0xE0)

    def getMeasuredCumulPower(self):
        return self.getMessage(0xE1)
