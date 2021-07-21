from datetime import datetime, timezone

#------------ EPC GENERIC FUNCTIONS -------
def _int(edt):
    return int.from_bytes(edt, 'big')

# Check status of Echonnet Instance
#----------------- EPC SUPER FUNCTIONS -----------------------------
def _0080(edt):
    ops_value = int.from_bytes(edt, 'big')
    return ('On' if ops_value == 0x30 else 'Off')

def _009X(edt):
    payload = []
    if len(edt) < 17:
        for i in range (1, len(edt)):
            payload.append(edt[i])
        return payload

    for i in range (1, len(edt)):
        code = i-1
        binary = '{0:08b}'.format(edt[i])[::-1]
        for j in range (0, 8):
            if binary[j] == "1":
                EPC = (j+8) * 0x10 + code
                payload.append(EPC)
    return payload

def _0083(edt):
    if edt is not None:
        if len(edt) > 1:
            ops_value = edt[1:].hex()
        else:
            ops_value = None
        return ops_value
    return None

EPC_SUPER_FUNCTIONS = {
    0x80: _0080,
    0x8A: _int,
    0x83: _0083,
    0x9E: _009X,
    0x9F: _009X
}


# ------- EPC FUNCTIONS -------------------------------------------------
# -----------------------------------------------------------------------

# ----- Tempereature Sensor -------
def _0011E0(edt):
        return float(int.from_bytes(edt, 'big')) / 10


# ----- Home Air conditioner -------
def _0130A0(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
       0x41: 'auto',
       0x31: 'minimum',
       0x32: 'low',
       0x33: 'medium-low',
       0x34: 'medium',
       0x35: 'medium-high',
       0x36: 'high',
       0x37: 'very-high',
       0x38: 'max'
    }
    return values.get(op_mode, "Invalid setting")

# Automatic control of air flow direction setting
def _0130A1(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
       0x41: 'auto',
       0x42: 'non-auto',
       0x43: 'auto-vert',
       0x44: 'auto-horiz'
    }
    return values.get(op_mode, "Invalid setting")

def _0130AA(edt):
    op_mode = int.from_bytes(edt, 'big')
    # print(hex(op_mode))
    values = {
      0x40: 'Normal operation',
      0x41: 'Defrosting',
      0x42: 'Preheating',
      0x43: 'Heat removal'
      }
    # return({'special':hex(op_mode)})
    return values.get(op_mode, "invalid_setting")

# Automatic swing of air flow direction setting
def _0130A3(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
       0x31: 'not-used',
       0x41: 'vert',
       0x42: 'horiz',
       0x43: 'vert-horiz'
    }
    return values.get(op_mode, "invalid_setting")

# Air flow direction (vertical) setting
def _0130A4(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
      0x41: 'upper',
      0x44: 'upper-central',
      0x43: 'central',
      0x45: 'lower-central',
      0x42: 'lower'
      }
    # return({'special':hex(op_mode)})
    return values.get(op_mode, "invalid_setting")

# Air flow direction (horiziontal) setting
def _0130A5(edt):
    # complies with version 2.01 Release a (page 3-88)
    op_mode = int.from_bytes(edt, 'big')
    values = {
      0x41: 'rc-right',
      0x42: 'left-lc',
      0x43: 'lc-center-rc',
      0x44: 'left-lc-rc-right',
      0x51: 'right',
      0x52: 'rc',
      0x54: 'center',
      0x55: 'center-right',
      0x56: 'center-rc',
      0x57: 'center-rc-right',
      0x58: 'lc',
      0x59: 'lc-right',
      0x5A: 'lc-rc',
      0x60: 'left',
      0x61: 'left-right',
      0x62: 'left-rc',
      0x63: 'left-rc-right',
      0x64: 'left-center',
      0x65: 'left-center-right',
      0x66: 'left-center-rc',
      0x67: 'left-center-rc-right',
      0x69: 'left-lc-right',
      0x6A: 'left-lc-rc'
      }
    return values.get(op_mode, "invalid_setting")

# Operation mode
def _0130B0(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
       0x41: 'auto',
       0x42: 'cool',
       0x43: 'heat',
       0x44: 'dry',
       0x45: 'fan_only',
       0x40: 'other'
    }
    return values.get(op_mode, "invalid_setting")

def _0260EO(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
       0x41: 'open',
       0x42: 'close',
       0x43: 'stop'
    }
    return values.get(op_mode, "invalid_setting")

# ----- Electric Lock Class -------
def _026FEX(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
       0x41: 'lock',
       0x42: 'unlock'
    }
    return values.get(op_mode, "invalid_setting")

def _026FE3(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
       0x41: 'open',
       0x42: 'closed'
    }
    return values.get(op_mode, "invalid_setting")

def _026FE4(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
       0x41: 'occupant',
       0x42: 'non-occupant'
    }
    return values.get(op_mode, "invalid_setting")

def _026FE5(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
       0x40: 'normal',
       0x41: 'break_open',
       0x42: 'door_open',
       0x43: 'maunal_unlocked',
       0x44: 'tampered'
    }
    return values.get(op_mode, "invalid_setting")

def _026FE6(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
       0x41: 'on',
       0x42: 'off'
    }
    return values.get(op_mode, "invalid_setting")

def _026FE7(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
       0x41: 'normal',
       0x42: 'battery_replacement_notification'
    }
    return values.get(op_mode, "invalid_setting")

  #--- Low voltage smart meter class

def _0288E1(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
        0x00: 1,
        0x01: 0.1,
        0x02: 0.01,
        0x03: 0.001,
        0x04: 0.0001,
        0x0A: 10,
        0x0B: 100,
        0x0C: 1000,
        0x0D: 10000,
    }
    return values.get(op_mode, "invalid_setting")


# ----- Low voltage smart electric energy meter -------
def _0288E7(edt):
    value = int.from_bytes(edt, 'big', signed=True)
    return value


def _0288E8(edt):
    r_phase = float(int.from_bytes(edt[0:2], 'big', signed=True)) / 10 #R Phase
    t_phase = float(int.from_bytes(edt[2:4], 'big', signed=True)) / 10 #T Phase
    return {"r_phase_amps": r_phase, "t_phase_amps": t_phase}

def _0288EA(edt):
    print(edt)
    year = int.from_bytes(edt[0:2], 'big')
    month = int.from_bytes(edt[2:3], 'big')
    day = int.from_bytes(edt[3:4], 'big')
    hour = int.from_bytes(edt[4:5], 'big')
    minute = int.from_bytes(edt[5:6], 'big')
    second = int.from_bytes(edt[6:7], 'big')
    culmative = int.from_bytes(edt[7:], 'big')
    time = datetime(year, month, day, hour,minute,second)
    return {'time': datetime(year, month, day, hour,minute,second).isoformat(), 'culmative_value': culmative}

# ----- General lighting class -------
def _0290B1(edt):
    op_mode = int.from_bytes(edt, 'big')
    values = {
       0x40: 'other',
       0x41: 'incandescent_lamp_color',
       0x42: 'white',
       0x43: 'daylight_white',
       0x43: 'daylight_color',
    }
    return values.get(op_mode, "invalid_setting")

EPC_FUNCTIONS = {
    0x00: {
        0x11:{
            0xE0: _0011E0,
            0XE1: _int
        }
    },
    0x01: {
        0x30:{
        	0xA0: _0130A0,
            0xA1: _0130A1,
            0xA3: _0130A3,
            0xA4: _0130A4,
            0xA5: _0130A5,
            0xAA: _0130AA,
            0xB0: _0130B0,
            0xB3: _int,
            0xBB: _int,
            0xBE: _int
        }
    },
    0x02: {
        0x60: {
            0xE0: _0260EO
        },
        0x6F: {
            0xE0: _026FEX,
            0xE1: _026FEX,
            0xE2: _026FEX,
            0xE3: _026FE3,
            0xE4: _026FE4,
            0xE5: _026FE5,
            0xE6: _026FE6,
            0xE7: _026FE7
        },
        0x79: {
            0xE0: _int,
            0xE1: _int
        },
        0x7d: {
            0xE4: _int,
            0xCF: _int
        },
        0x88: {
            0xd7: _int, #number of effective digits in culmative amout of energy
            0xe0: _int, #measured culmative amount of electricity
            0xe1: _0288E1, #multiplying factor
            # 0xe2:
            0xe5: _int,
            0xe7: _0288E7, #measured instantaneous electric energy
            0xe8: _0288E8, #measured instantanenous currents
            0xea: _0288EA
        },
        0x90: {
            0xB1: _0290B1
        }
    }
}
