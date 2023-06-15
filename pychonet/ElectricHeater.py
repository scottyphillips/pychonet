from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _hh_mm, _signed_int

def _014290(data):
    # Logic to interpret data for EPC 0x90
    if data == 0x41:
        return 'Automatic'
    elif data == 0x42:
        return 'Manual'
    else:
        return 'Unknown'

def _0142A0(data):
    # Logic to interpret data for EPC 0xA0
    if data == 0x41:
        return 'Automatic air flow rate control used'
    elif 0x31 <= data <= 0x38:
        return f'Air flow rate: {data.decode()}'
    else:
        return 'Unknown'

def _0142B1(data):
    # Logic to interpret data for EPC 0xB1
    if data == 0x41:
        return 'On'
    elif data == 0x42:
        return 'Off'
    else:
        return 'Unknown'

def _014294(data):
    # Logic to interpret data for EPC 0xB1
    if data == 0x41:
        return 'On'
    elif data == 0x42:
        return 'Off'
    else:
        return 'Unknown'

class ElectricHeater(EchonetInstance):
    EOJGC = 0x01
    EOJCC = 0x42

    EPC_FUNCTIONS = {
        0x80: _int,
        0xB1: _0142B1,
        0xB3: _int,
        0xBB: _signed_int,
        0xBC: _int,
        0xA0: _0142A0,
        0x90: _014290,
        0x91: _hh_mm,
        0x92: _hh_mm,
        0x94: _014294,
        0x95: _hh_mm,
        0x96: _hh_mm,
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = self.EOJGC
        self._eojcc = self.EOJCC
        super().__init__(host, self._eojgc, self._eojcc, instance, api_connector)

    @property
    def operation_status(self):
        return self.getMessage(0x80)

    @operation_status.setter
    def operation_status(self, value):
        self.setMessage(0x80, value)

    @property
    def automatic_temperature_control_setting(self):
        return self.getMessage(0xB1)

    @automatic_temperature_control_setting.setter
    def automatic_temperature_control_setting(self, value):
        self.setMessage(0xB1, value)

    @property
    def temperature_setting(self):
        return self.getMessage(0xB3)

    @temperature_setting.setter
    def temperature_setting(self, value):
        self.setMessage(0xB3, value)

    @property
    def measured_room_temperature(self):
        return self.getMessage(0xBB)

    @measured_room_temperature.setter
    def measured_room_temperature(self, value):
        self.setMessage(0xBB, value)

    @property
    def remotely_set_temperature(self):
        return self.getMessage(0xBC)

    @remotely_set_temperature.setter
    def remotely_set_temperature(self, value):
        self.setMessage(0xBC, value)

    @property
    def air_flow_rate_setting(self):
        return self.getMessage(0xA0)

    @air_flow_rate_setting.setter
    def air_flow_rate_setting(self, value):
        self.setMessage(0xA0, value)
