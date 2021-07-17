from pychonet.EchonetInstance import EchonetInstance

MEASURED_TEMP = 0xE0

class TemperatureSensor(EchonetInstance):
    def __init__(self, netif, instance = 0x1):
        self.eojgc = 0x00
        self.eojcc = 0x11
        EchonetInstance.__init__(self, self.eojgc, self.eojcc, instance, netif)

    def getMeasuredTemperature(self):
        return self.update(MEASURED_TEMP)
