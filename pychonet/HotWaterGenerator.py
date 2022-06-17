from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int, _hh_mm

# ----- Hot Water Generator -------

def _0272D0E2(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "Heating",
              0x42: "Not Heating"}
    return values.get(op_mode, "Invalid setting")

def _0272D2(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "Hot water warmer operation",
              0x42: "Hot water warmer operation resetting"}
    return values.get(op_mode, "Invalid setting")

def _0272EX(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "On",
              0x42: "Off"}
    return values.get(op_mode, "Invalid setting")

def _0272D7(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x30: "On",
              0x31: "Off"}
    return values.get(op_mode, "Invalid setting")

def _0272E8(edt):
    op_mode = int.from_bytes(edt, "big")
    values = {0x31: "Level 1",
              0x32: "Level 2",
              0x33: "Level 3",
              0x34: "Level 4",
              0x35: "Level 5",
              0x36: "Level 6",
              0x37: "Level 7",
              0x38: "Level 8"}
    return values.get(op_mode, "Invalid setting")

def _0272DA(edt): # Duration of automatic operation setting
    if edt == 0xffff:
        return "Limitless"
    hh = int.from_bytes(edt[0:1], "big")
    mm = str(int.from_bytes(edt[1:2], "big")).zfill(2)
    return f"{hh}:{mm}"

def _0272DB(edt): # Remaining automatic operation time
    if edt == 0xffff:
        return "Infinite"
    hh = int.from_bytes(edt[0:1], "big")
    mm = str(int.from_bytes(edt[1:2], "big")).zfill(2)
    return f"{hh}:{mm}"

def _0272EF(edt): # "Bath operation status monitor",
    op_mode = int.from_bytes(edt, "big")
    values = {0x41: "Supplying Hot Water",
              0x43: "Keeping Bath Temperature",
              0x42: "Stopped"}
    return values.get(op_mode, "Invalid setting")

class HotWaterGenerator(EchonetInstance):
    EPC_FUNCTIONS = {
         0xD0: _0272D0E2, # Hot water heating status
         0xD1: _int,      # Set value of hot  water temperature
         0xD2: _0272D2,   # Hot water warmer setting
         0xDA: _0272DA,   # Duration of automatic operation setting
         0xDB: _0272DB,   # Remaining automatic operation time
         0xE1: _int,      # Set value of bath of the bath temperature in degrees C
         0xE2: _0272D0E2, # Bath water heater status
         0xE3: _0272EX,   # Bath automatic mode setting
         0xE4: _0272EX,   # Bath additional boil-up operation setting
         0xE5: _0272EX,   # Bath adding hot water operation setting
         0xE6: _0272EX,   # Bath water temperature lowering operation setting
         0xE7: _int,      # Bath hot water volume setting 1
         0xE8: _0272E8,   # Bath hot water volume setting 2
         0xEE: _int,      # Bath hot water volume setting 3
         0xD4: _int,      # Bath hot water volume setting 4
         0xD5: _int,      # Bath hot water volume setting 4 - Maximum settable level
         0xE9: _0272EX,   # "Bathroom priority setting",
         0xEA: _0272EX,   # "Shower hot water supply status",
         0xEB: _0272EX,   # "Kitchen hot water supply status",
         0xEC: _0272EX,   # "Hot water warmer ON timer reservation setting",
         0xED: _hh_mm,    # "Set value of hot water warmer ON timer time",
         0xEF: _0272EF,   # "Bath operation status monitor",
         0x90: _0272EX,   # "ON timer reservation setting",
         0x91: _hh_mm,    # "Set value of ON timer time",
         0x92: _hh_mm,    # "Set value of ON timer relative time",
         0xD6: _int,      # "Volume setting",
         0xD7: _0272D7    # "Mute setting",
    }

    def __init__(self, host, api_connector=None, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x72
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )
