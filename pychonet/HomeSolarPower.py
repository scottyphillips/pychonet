from pychonet.EchonetInstance import EchonetInstance

def _0279e0(edt):
        return {'instantaneous_power': int.from_bytes(edt, 'big')}

def _0279e1(edt):
        return {'cumul_power': int.from_bytes(edt, 'big')}

class HomeSolarPower(EchoNetNode):
    def __init__(self, netif, instance = 0x1):
        self.eojgc = 0x02
        self.eojcc = 0x79
        EchonetInstance.__init__(self, self.eojgc, self.eojcc, instance, netif)

    def getMeasuredInstantPower(self):
        raw_data = self.getMessage(0xE0)[0]
        if raw_data['rx_epc'] == 0xE0:
            return _0279e0(raw_data['rx_edt'])

    def getMeasuredCumulPower(self):
        raw_data = self.getMessage(0xE1)[0]
        if raw_data['rx_epc'] == 0xE1:
            return _0279e1(raw_data['rx_edt'])
