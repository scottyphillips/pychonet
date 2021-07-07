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

class StorageBattery(EchoNetNode):
    def __init__(self, netif, instance = 0x1):
        self.eojgc = 0x02
        self.eojcc = 0x7d
        EchonetInstance.__init__(self, self.eojgc, self.eojcc, instance, netif)

    def getRemainingStoredElectricity3(self):
        raw_data = self.getMessage(0xE4)[0]
        if raw_data['rx_epc'] == 0xE4:
            return _027de4(raw_data['rx_edt'])

    def getWorkingOperationStatus(self):
        raw_data = self.getMessage(0xCF)[0]
        if raw_data['rx_epc'] == 0xCF:
            return _027dcf(raw_data['rx_edt'])
