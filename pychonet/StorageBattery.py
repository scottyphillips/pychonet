from pychonet.EchonetInstance import EchonetInstance

def _027de4(edt):
    return {'remaining_electricity_3': int.from_bytes(edt, 'big')}

def _027dcf(edt):
    STATES = {
        0x41: "Rapid charging",
        0x42: "Charging",
        0x43: "Discharging",
        0x44: "Standby",
        0x45: "Test",
        0x46: "Automatic",
        0x48: "Restart",
        0x49: "Effective capacity recalculation processing"
    }

    return {"working_operation_status": STATES[int.from_bytes(edt, 'big')]}

class StorageBattery(EchonetInstance):
    def __init__(self, netif, instance = 0x1):
        self.eojgc = 0x02
        self.eojcc = 0x7d
        EchonetInstance.__init__(self, self.eojgc, self.eojcc, instance, netif)

    def getRemainingStoredElectricity3(self):
        return _027de4(self.getSingleMessageResponse(0xE4))

    def getWorkingOperationStatus(self):
        return _027dcf(self.getSingleMessageResponse(0xCF))
