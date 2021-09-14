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

    def __init__(self, host, api_connector = None, instance = 0x1):
        self._eojgc = 0x02
        self._eojcc = 0x7d
        EchonetInstance.__init__(self, host, self._eojgc, self._eojcc, instance, api_connector)

    def getRemainingStoredElectricity3(self):
        return self.getMessage(0xE4)

    def getWorkingOperationStatus(self):
        return self.getMessage(0xCF)
