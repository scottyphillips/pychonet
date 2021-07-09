from pychonet.EchonetInstance import EchonetInstance

class StorageBattery(EchonetInstance):

    WORKING_OPERATION_STATES = {
        0x40: "Other",
        0x41: "Rapid charging",
        0x42: "Charging",
        0x43: "Discharging",
        0x44: "Standby",
        0x45: "Test",
        0x46: "Automatic",
        0x48: "Restart",
        0x49: "Effective capacity recalculation processing"
    }

    def __init__(self, netif, instance = 0x1):
        self.eojgc = 0x02
        self.eojcc = 0x7d
        EchonetInstance.__init__(self, self.eojgc, self.eojcc, instance, netif)

    def getRemainingStoredElectricity3(self):
        return int.from_bytes(self.getSingleMessageResponse(0xE4), 'big')

    def getWorkingOperationStatus(self):
        return int.from_bytes(self.getSingleMessageResponse(0xCF), 'big')
