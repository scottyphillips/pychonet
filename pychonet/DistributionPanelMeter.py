from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int

ENL_DPM_ENG_NOR = 0xC0
ENL_DPM_ENG_REV = 0xC1
ENL_DPM_ENG_UNIT = 0xC2
ENL_DPM_DAY_GET_HISTORY = 0xC5
ENL_DPM_INSTANT_ENG = 0xC6
ENL_DPM_INSTANT_CUR = 0xC7
ENL_DPM_INSTANT_VOL = 0xC8
ENL_DPM_CHANNEL_SIMPLEX_CUMULATIVE_ENG = 0xB3
ENL_DPM_CHANNEL_SIMPLEX_INSTANT_ENG = 0xB7


def _0287C2(edt):
    """Unit for cumulative amounts of electric energy - returns multiplier."""
    op_mode = int.from_bytes(edt, "big")
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
    return values.get(op_mode, None)


def _0287B3(edt):
    """Measured cumulative amount of electric power consumption list (simplex)."""
    values = []
    for x in range(0, edt[1]):
        values.append(
            int.from_bytes(edt[x * 4 + 2 : (x + 1) * 4 + 2], "big", signed=False)
        )
    return {"start": edt[0], "range": edt[1], "values": values}


def _0287B7(edt):
    """Measured instantaneous power consumption list (simplex)."""
    values = []
    for x in range(0, edt[1]):
        values.append(
            int.from_bytes(edt[x * 4 + 2 : (x + 1) * 4 + 2], "big", signed=True)
        )
    return {"start": edt[0], "range": edt[1], "values": values}


def _0287C7(edt):
    """Measured instantaneous currents - R and T phase in amperes."""
    r_phase = float(int.from_bytes(edt[0:2], "big", signed=True)) / 10  # R Phase
    t_phase = float(int.from_bytes(edt[2:4], "big", signed=True)) / 10  # T Phase
    if t_phase == 3276.6:
        t_phase = None
    return {"r_phase_amperes": r_phase, "t_phase_amperes": t_phase}


def _0287C8(edt):
    """Measured instantaneous voltages - R-S(N) and S(N)-T in volts."""
    r_sn = float(int.from_bytes(edt[0:2], "big", signed=True)) / 10  # R-S(N)
    sn_t = float(int.from_bytes(edt[2:4], "big", signed=True)) / 10  # S(N)-T
    if sn_t == 6553.4:
        sn_t = None
    return {"r_sn_voltage": r_sn, "sn_t_voltage": sn_t}


def _0287D0EF(edt):
    """Measurement channel data (EPC 0xD0-0xEF).
    
    The EPC code itself identifies the channel (0xD0=channel 1, 0xD1=channel 2, etc.).
    This function returns the flat measurement data for the specific channel identified
    by the EPC that was used.
    
    Format: [electric_energy(4 bytes uint32), current_r(2 bytes int16), current_t(2 bytes int16)]
    Total: 8 bytes. Current values divided by 10, 0x7FFE = Not measured.
    """
    electric_energy = int.from_bytes(edt[0:4], "big", signed=False)
    current_r = float(int.from_bytes(edt[4:6], "big", signed=True)) / 10
    current_t = float(int.from_bytes(edt[6:8], "big", signed=True)) / 10
    
    # Handle "Not measured" codes
    if electric_energy == 0xFFFFFFFE:
        electric_energy = None  # Not measured
    if current_r == 3276.6:
        current_r = None
    if current_t == 3276.6:
        current_t = None
    
    return {
        "electric_energy_kwh": electric_energy,
        "current_r_phase_a": current_r,
        "current_t_phase_a": current_t
    }


def _0287B2(edt):
    """Channel range specification for cumulative amount of electric power consumption measurement (simplex).
    
    Format: [start_channel(1 byte), range(1 byte)]
    """
    start_channel = edt[0]
    range_count = edt[1]
    return {"start_channel": start_channel, "range": range_count}


def _0287B4(edt):
    """Channel range specification for instantaneous current measurement (simplex).
    
    Format: [start_channel(1 byte), range(1 byte)]
    """
    start_channel = edt[0]
    range_count = edt[1]
    return {"start_channel": start_channel, "range": range_count}


def _0287B5(edt):
    """Measured instantaneous current list (simplex).
    
    Format: [start_channel(1 byte), range(1 byte), then for each channel: r_phase(2 bytes int16), t_phase(2 bytes int16)]
    Each current value divided by 10, 0x7FFE = Not measured.
    """
    start_channel = edt[0]
    range_count = edt[1]
    currents = []
    for i in range(range_count):
        offset = 2 + i * 4
        r_phase = float(int.from_bytes(edt[offset:offset+2], "big", signed=True)) / 10
        t_phase = float(int.from_bytes(edt[offset+2:offset+4], "big", signed=True)) / 10
        if r_phase == 3276.6:
            r_phase = None
        if t_phase == 3276.6:
            t_phase = None
        currents.append({
            "r_phase_a": r_phase,
            "t_phase_a": t_phase
        })
    return {"start_channel": start_channel, "range": range_count, "currents": currents}


def _0287B6(edt):
    """Channel range specification for instantaneous power consumption measurement (simplex).
    
    Format: [start_channel(1 byte), range(1 byte)]
    """
    start_channel = edt[0]
    range_count = edt[1]
    return {"start_channel": start_channel, "range": range_count}


def _0287B9(edt):
    """Channel range specification for cumulative amount of electric power consumption measurement (duplex).
    
    Format: [start_channel(1 byte), range(1 byte)]
    Max range is 30 for duplex.
    """
    start_channel = edt[0]
    range_count = edt[1]
    return {"start_channel": start_channel, "range": range_count}


def _0287BA(edt):
    """Measured cumulative amount of electric power consumption list (duplex)."""
    values = []
    for x in range(0, edt[1]):
        offset = x * 8 + 2
        normal_dir = int.from_bytes(edt[offset:offset+4], "big", signed=False)
        reverse_dir = int.from_bytes(edt[offset+4:offset+8], "big", signed=False)
        if normal_dir == 0xFFFFFFFE:
            normal_dir = None
        if reverse_dir == 0xFFFFFFFE:
            reverse_dir = None
        values.append({
            "normal_direction_kwh": normal_dir,
            "reverse_direction_kwh": reverse_dir
        })
    return {"start": edt[0], "range": edt[1], "values": values}


def _0287BB(edt):
    """Channel range specification for instantaneous current measurement (duplex).
    
    Format: [start_channel(1 byte), range(1 byte)]
    Max range is 60 for duplex.
    """
    start_channel = edt[0]
    range_count = edt[1]
    return {"start_channel": start_channel, "range": range_count}


def _0287BC(edt):
    """Measured instantaneous current list (duplex).
    
    Format: [start_channel(1 byte), range(1 byte), then for each channel: r_phase(2 bytes int16), t_phase(2 bytes int16)]
    Each current value divided by 10, 0x7FFE = Not measured.
    """
    start_channel = edt[0]
    range_count = edt[1]
    currents = []
    for i in range(range_count):
        offset = 2 + i * 4
        r_phase = float(int.from_bytes(edt[offset:offset+2], "big", signed=True)) / 10
        t_phase = float(int.from_bytes(edt[offset+2:offset+4], "big", signed=True)) / 10
        if r_phase == 3276.6:
            r_phase = None
        if t_phase == 3276.6:
            t_phase = None
        currents.append({
            "r_phase_a": r_phase,
            "t_phase_a": t_phase
        })
    return {"start_channel": start_channel, "range": range_count, "currents": currents}


def _0287BD(edt):
    """Channel range specification for instantaneous power consumption measurement (duplex).
    
    Format: [start_channel(1 byte), range(1 byte)]
    Max range is 60 for duplex.
    """
    start_channel = edt[0]
    range_count = edt[1]
    return {"start_channel": start_channel, "range": range_count}


def _0287BE(edt):
    """Measured instantaneous power consumption list (duplex).
    
    Format: [start_channel(1 byte), range(1 byte), then for each channel: power(4 bytes int32)]
    0x7FFFFFFE = Not measured.
    """
    values = []
    for x in range(0, edt[1]):
        val = int.from_bytes(edt[x * 4 + 2 : (x + 1) * 4 + 2], "big", signed=True)
        if val == 0x7FFFFFFE:
            val = None
        values.append(val)
    return {"start": edt[0], "range": edt[1], "values": values}


def _0287C3(edt):
    """Historical data of measured cumulative amounts of electric energy (normal direction).
    
    Format: [day_high(1 byte), day_low(1 byte), then 48 x 4 bytes for each half-hourly reading]
    Each reading is uint32, multiply by unit from EPC 0xC2.
    0xFFFFFFFE = Not measured.
    """
    if len(edt) < 98:  # 2 (day) + 48*4 (data) = 194 bytes minimum
        return {"error": "Data too short"}
    
    day = int.from_bytes(edt[0:2], "big")
    readings = []
    for i in range(48):
        offset = 2 + i * 4
        reading = int.from_bytes(edt[offset:offset+4], "big", signed=False)
        if reading == 0xFFFFFFFE:
            reading = None  # Not measured
        readings.append(reading)
    return {"day": day, "readings_48_half_hourly": readings}


def _0287C4(edt):
    """Historical data of measured cumulative amounts of electric energy (reverse direction).
    
    Format: [day_high(1 byte), day_low(1 byte), then 48 x 4 bytes for each half-hourly reading]
    Each reading is uint32, multiply by unit from EPC 0xC2.
    0xFFFFFFFE = Not measured.
    """
    if len(edt) < 98:
        return {"error": "Data too short"}
    
    day = int.from_bytes(edt[0:2], "big")
    readings = []
    for i in range(48):
        offset = 2 + i * 4
        reading = int.from_bytes(edt[offset:offset+4], "big", signed=False)
        if reading == 0xFFFFFFFE:
            reading = None  # Not measured
        readings.append(reading)
    return {"day": day, "readings_48_half_hourly": readings}


def _028788(edt):
    """Fault status - indicates whether a fault has occurred.
    
    0x41 = Fault occurred (異常あり / true)
    0x42 = No fault has occurred (異常なし / false)
    """
    if edt == b'\x41':
        return True  # Fault occurred
    elif edt == b'\x42':
        return False  # No fault
    else:
        return None


def _028789(edt):
    """Fault description - describes the type of fault.
    
    Returns a dict with fault code and description.
    """
    if len(edt) < 2:
        return {"code": None, "description": "Invalid data"}
    
    fault_code = int.from_bytes(edt[0:2], "big")
    descriptions = {
        0x0000: "No fault",
        0x0001: "Faults recoverable by turn off power or unplug and reoperate",
        0x0002: "Faults recoverable by pressing reset button",
        0x0003: "Device set incorrectly",
        0x0004: "Supply",
        0x0005: "Cleaning (filters, etc.)",
        0x0006: "Changing the battery",
        0x0007: "Recover operation not required",
        0x0009: "User-definable domain",
    }
    
    # Range-based entries
    if 0x000A <= fault_code <= 0x0013:
        descriptions[fault_code] = "Abnormal event or the tripping of a safety device"
    elif 0x0014 <= fault_code <= 0x001D:
        descriptions[fault_code] = "Fault in a switch"
    elif 0x001E <= fault_code <= 0x003B:
        descriptions[fault_code] = "Fault in the sensor system"
    elif 0x003C <= fault_code <= 0x0059:
        descriptions[fault_code] = "Fault in a component such as an actuator"
    elif 0x005A <= fault_code <= 0x006E:
        descriptions[fault_code] = "Fault in a control circuit board"
    elif 0x006F <= fault_code <= 0x03E8:
        descriptions[fault_code] = "User-definable domain"
    elif fault_code == 0x03E9:
        descriptions[fault_code] = "Repair location unknown"
    elif fault_code == 0x03FF:
        descriptions[fault_code] = "Fault"
    
    return {"code": fault_code, "description": descriptions.get(fault_code, "Unknown fault")}


class DistributionPanelMeter(EchonetInstance):
    EPC_FUNCTIONS = {
        # Basic properties (0x80-0x9F)
        0x80: _int,  # Operation status
        0x81: _int,  # Installation location
        0x82: _int,  # Standard version information
        0x83: _int,  # Identification number
        0x84: _int,  # Measured instantaneous power consumption
        0x85: _int,  # Measured cumulative electric energy consumption
        0x86: _int,  # Manufacturer's fault code
        0x87: _int,  # Current limit setting
        0x88: _028788,  # Fault status (state: 0x41=Fault, 0x42=No fault)
        0x89: _028789,  # Fault description (2-byte enum with detailed fault types)
        0x8A: _int,  # Manufacturer code
        0x8B: _int,  # Business facility code
        0x8C: _int,  # Product code
        0x8D: _int,  # Production number
        0x8E: _int,  # Production date
        0x8F: _int,  # Power-saving operation setting
        0x93: _int,  # Remote control setting
        0x97: _int,  # Current time setting
        0x98: _int,  # Current date setting
        0x99: _int,  # Power limit setting
        0x9A: _int,  # Cumulative operating time
        0x9D: _int,  # Status change announcement property map (STATMAP)
        0x9E: _int,  # Set property map (SETMAP)
        0x9F: _int,  # Get property map (GETMAP)

        # Simplex metering properties (0xB0-0xB7)
        0xB0: _int,  # Master rated capacity
        0xB1: _int,  # Number of measurement channels (simplex)
        0xB2: _0287B2,  # Channel range specification for cumulative amount of electric power consumption measurement (simplex)
        0xB3: _0287B3,  # Measured cumulative amount of electric power consumption list (simplex)
        0xB4: _0287B4,  # Channel range specification for instantaneous current measurement (simplex)
        0xB5: _0287B5,  # Measured instantaneous current list (simplex)
        0xB6: _0287B6,  # Channel range specification for instantaneous power consumption measurement (simplex)
        0xB7: _0287B7,  # Measured instantaneous power consumption list (simplex)

        # Duplex metering properties (0xB8-0xBE)
        0xB8: _int,  # Number of measurement channels (duplex)
        0xB9: _0287B9,  # Channel range specification for cumulative amount of electric power consumption measurement (duplex)
        # 0xBA: _0287BA,  # Measured cumulative amount of electric power consumption list (duplex)
        # 0xBB: _0287BB,  # Channel range specification for instantaneous current measurement (duplex)
        # 0xBC: _0287BC,  # Measured instantaneous current list (duplex)
        # 0xBD: _0287BD,  # Channel range specification for instantaneous power consumption measurement (duplex)
        # 0xBE: _0287BE,  # Measured instantaneous power consumption list (duplex)

        # Energy/voltage/current properties (0xC0-0xC8)
        0xC0: _int,  # Measured cumulative amount of electric energy (normal direction)
        0xC1: _int,  # Measured cumulative amount of electric energy (reverse direction)
        0xC2: _0287C2,  # Unit for cumulative amounts of electric energy
        0xC3: _0287C3,  # Historical data of measured cumulative amounts of electric energy (normal direction)
        0xC4: _0287C4,  # Historical data of measured cumulative amounts of electric energy (reverse direction)
        0xC5: _int,  # Day for which the historical data of measured cumulative amounts of electric energy is to be retrieved
        0xC6: _signed_int,  # Measured instantaneous amount of electric energy
        0xC7: _0287C7,  # Measured instantaneous currents
        0xC8: _0287C8,  # Measured instantaneous voltages

        # Measurement channels 1-32 (0xD0-0xEF) - 8 bytes each
        # 0xD0: _0287D0EF,  # Measurement channel 1
        # 0xD1: _0287D0EF,  # Measurement channel 2
        # 0xD2: _0287D0EF,  # Measurement channel 3
        # 0xD3: _0287D0EF,  # Measurement channel 4
        # 0xD4: _0287D0EF,  # Measurement channel 5
        # 0xD5: _0287D0EF,  # Measurement channel 6
        # 0xD6: _0287D0EF,  # Measurement channel 7
        # 0xD7: _0287D0EF,  # Measurement channel 8
        # 0xD8: _0287D0EF,  # Measurement channel 9
        # 0xD9: _0287D0EF,  # Measurement channel 10
        # 0xDA: _0287D0EF,  # Measurement channel 11
        # 0xDB: _0287D0EF,  # Measurement channel 12
        # 0xDC: _0287D0EF,  # Measurement channel 13
        # 0xDD: _0287D0EF,  # Measurement channel 14
        # 0xDE: _0287D0EF,  # Measurement channel 15
        # 0xDF: _0287D0EF,  # Measurement channel 16
        # 0xE0: _0287D0EF,  # Measurement channel 17
        # 0xE1: _0287D0EF,  # Measurement channel 18
        # 0xE2: _0287D0EF,  # Measurement channel 19
        # 0xE3: _0287D0EF,  # Measurement channel 20
        # 0xE4: _0287D0EF,  # Measurement channel 21
        # 0xE5: _0287D0EF,  # Measurement channel 22
        # 0xE6: _0287D0EF,  # Measurement channel 23
        # 0xE7: _0287D0EF,  # Measurement channel 24
        # 0xE8: _0287D0EF,  # Measurement channel 25
        # 0xE9: _0287D0EF,  # Measurement channel 26
        # 0xEA: _0287D0EF,  # Measurement channel 27
        # 0xEB: _0287D0EF,  # Measurement channel 28
        # 0xEC: _0287D0EF,  # Measurement channel 29
        # 0xED: _0287D0EF,  # Measurement channel 30
        # 0xEE: _0287D0EF,  # Measurement channel 31
        # 0xEF: _0287D0EF,  # Measurement channel 32
    }

    def __init__(self, host, api_connector, instance=0x1):
        self._eojgc = 0x02
        self._eojcc = 0x87
        EchonetInstance.__init__(
            self, host, self._eojgc, self._eojcc, instance, api_connector
        )