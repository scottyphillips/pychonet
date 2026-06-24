# CombinationMicrowaveOven.py
# Combination Microwave Oven (Electronic Oven) class for ECHONET Lite
# Class group code: 0x03, Class code: 0xB8
# Reference: ECHONET Lite APPENDIX Release R rev.4 (September 26, 2025)
#
# Author: Scott Phillips
# License: MIT
#
# +--------------------------------------------+-------+----------------------------------------------------+-----------+------+---------+-------+---------+
# | Property Name                              | EPC   | Contents (Value Range)                             | Data Type | Size | Access  | Mand. | Announ. |
# +--------------------------------------------+-------+----------------------------------------------------+-----------+------+---------+-------+---------+
# | Operation status                           | 0x80  | ON=0x30, OFF=0x31                                  | u_char    | 1 B  | Set/Get |   O   |    O    |
# | Door open/close status                     | 0xB0  | Open=0x41, Closed=0x42                             | u_char    | 1 B  | Get     |       |         |
# | Heating status                             | 0xB1  | Initial=0x40, Heating=0x41, Suspended=0x42,        | u_char    | 1 B  | Get     |       |         |
# |                                            |       | Cycle complete=0x43, Setting=0x44, Preheating=0x45,|           |      |         |       |         |
# |                                            |       | Preheat maintenance=0x46, Manual stop=0x47          |           |      |         |       |         |
# | Heating setting                            | 0xB2  | Start/restart=0x41, Suspend=0x42, Stop=0x43       | u_char    | 1 B  | Set/Get |       |         |
# | Heating mode setting                       | 0xE0  | Microwave=0x41, Defrost=0x42, Oven=0x43,           | u_char    | 1 B  | Set/Get |       |         |
# |                                            |       | Grill=0x44, Toaster=0x45, Fermenting=0x46,         |           |      |         |       |         |
# |                                            |       | Stewing=0x47, Steaming=0x48,                        |           |      |         |       |         |
# |                                            |       | Two-stage microwave=0x51, No mode=0xFF              |           |      |         |       |         |
# | Automatic heating setting                  | 0xE1  | Automatic=0x41, Manual=0x42, Not specified=0xFF    | u_char    | 1 B  | Set/Get |       |         |
# | Automatic heating level setting            | 0xE2  | 0x31-0x35 (lowest to highest), Not specified=0xFF  | u_char    | 1 B  | Set/Get |       |         |
# | Automatic heating menu setting             | 0xD0  | 0x00-0xFE (cycle code), Not specified=0xFF         | u_char    | 1 B  | Set/Get |       |         |
# | Oven mode setting                          | 0xD1  | Auto=0x40, Convection=0x41, Circulation=0x42,      | u_char    | 1 B  | Set/Get |       |         |
# |                                            |       | Hybrid=0x43, No sub-mode=0xFF                       |           |      |         |       |         |
# | Oven preheating setting                    | 0xD5  | With preheating=0x41, Without=0x42, Not spec=0xFF  | u_char    | 1 B  | Set/Get |       |         |
# | Fermenting mode setting                    | 0xD6  | Auto=0x40, Convection=0x41, Circulation=0x42,      | u_char    | 1 B  | Set/Get |       |         |
# |                                            |       | Hybrid=0x43, Microwave=0x51, No mode=0xFF           |           |      |         |       |         |
# | Chamber temperature setting                | 0xE3  | 0xF554-0x7FFE (-273.2 to 3276.6°C, 0.1°C step)    | s_short   | 2 B  | Set/Get |       |         |
# |                                            |       | 0x8001=Auto, 0x8002=Not specified                   |           |      |         |       |         |
# | Food temperature setting                   | 0xE4  | 0xF554-0x7FFE (-273.2 to 3276.6°C, 0.1°C step)    | s_short   | 2 B  | Set/Get |       |         |
# |                                            |       | 0x8002=Not specified                                |           |      |         |       |         |
# | Heating time setting                       | 0xE5  | HH:MM:SS (0-23h, 0-59m, 0-59s)                     | u_char×3  | 3 B  | Set/Get |       |         |
# | Remaining heating time setting             | 0xE6  | HH:MM:SS (0-23h, 0-59m, 0-59s)                     | u_char×3  | 3 B  | Set/Get |       |         |
# | Microwave heating power setting            | 0xE7  | 0x0000-0xFFFD (0-65533W, 1W step)                  | u_short   | 2 B  | Set/Get |       |         |
# | Prompt message setting                     | 0xE8  | Up to 4 messages: code (1B) + timing % (1B) each   | u_char×2×4| 8 B  | Set/Get |       |         |
# | Accessories setting                        | 0xE9  | 2-byte bitmap of accessories in use                 | u_short   | 2 B  | Set/Get |       |         |
# | Display character string setting           | 0xEA  | Shift-JIS ×20 characters (40 bytes)                 | u_short×20| 40 B | Set     |       |         |
# | Two-stage microwave heating (duration)     | 0xEB  | HH:MM:SS×2 (first + second cycle durations)        | u_char×3×2| 6 B  | Set/Get |       |         |
# | Two-stage microwave heating (power)        | 0xEC  | 0x0000-0xFFFD×2 (first + second cycle powers, 1W)  | u_short×2 | 4 B  | Set/Get |       |         |
# +--------------------------------------------+-------+----------------------------------------------------+-----------+------+---------+-------+---------+

from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.epc_functions import _int, _signed_int, _swap_dict


# Heating status values
HEATING_STATUS = {
    0x40: "initial",
    0x41: "heating",
    0x42: "suspended",
    0x43: "cycle-complete",
    0x44: "setting",
    0x45: "preheating",
    0x46: "preheat-maintenance",
    0x47: "manual-stop",
}

# Heating mode values
HEATING_MODES = {
    0x41: "microwave",
    0x42: "defrost",
    0x43: "oven",
    0x44: "grill",
    0x45: "toaster",
    0x46: "fermenting",
    0x47: "stewing",
    0x48: "steaming",
    0x51: "two-stage-microwave",
    0xFF: "no-mode",
}

# Oven mode sub-modes
OVEN_MODES = {
    0x40: "auto",
    0x41: "convection",
    0x42: "circulation",
    0x43: "hybrid",
    0xFF: "no-sub-mode",
}

# Fermenting mode sub-modes
FERMENTING_MODES = {
    0x40: "auto",
    0x41: "convection",
    0x42: "circulation",
    0x43: "hybrid",
    0x51: "microwave",
    0xFF: "no-mode",
}


def _chamber_temperature(edt: bytes):
    """Decode chamber temperature setting (0.1°C resolution, signed short).

    Special values:
      0x8001 = Automatic
      0x8002 = Not specified
    """
    raw = int.from_bytes(edt[0:2], "big", signed=False)
    if raw == 0x8001:
        return "auto"
    if raw == 0x8002:
        return None
    return int.from_bytes(edt[0:2], "big", signed=True) / 10.0


def _food_temperature(edt: bytes):
    """Decode food temperature setting (0.1°C resolution, signed short).

    Special value:
      0x8002 = Not specified
    """
    raw = int.from_bytes(edt[0:2], "big", signed=False)
    if raw == 0x8002:
        return None
    return int.from_bytes(edt[0:2], "big", signed=True) / 10.0


def _hh_mm_ss(edt: bytes):
    """Decode HH:MM:SS duration from 3 unsigned bytes."""
    hh = int(edt[0])
    mm = int(edt[1])
    ss = int(edt[2])
    return f"{hh:02d}:{mm:02d}:{ss:02d}"


def _microwave_power(edt: bytes):
    """Decode microwave heating power in watts (unsigned short)."""
    raw = int.from_bytes(edt[0:2], "big", signed=False)
    if raw == 0xFFFE:
        return None  # not specified
    return raw  # watts


def _prompt_messages(edt: bytes):
    """Decode up to 4 prompt messages (code + timing % each, 2 bytes per message)."""
    messages = []
    for i in range(4):
        code = edt[i * 2]
        timing = edt[i * 2 + 1]
        if code != 0xFF:
            messages.append({"code": code, "timing_pct": timing})
    return messages if messages else None


def _accessories_bitmap(edt: bytes):
    """Decode accessories bitmap (2 bytes)."""
    return int.from_bytes(edt[0:2], "big", signed=False)


def _two_stage_duration(edt: bytes):
    """Decode two-stage microwave heating durations (HH:MM:SS × 2)."""
    return {
        "first": _hh_mm_ss(edt[0:3]),
        "second": _hh_mm_ss(edt[3:6]),
    }


def _two_stage_power(edt: bytes):
    """Decode two-stage microwave heating powers (2 × unsigned short, 1W steps)."""
    first = int.from_bytes(edt[0:2], "big", signed=False)
    second = int.from_bytes(edt[2:4], "big", signed=False)
    return {
        "first_W": first if first != 0xFFFE else None,
        "second_W": second if second != 0xFFFE else None,
    }


class CombinationMicrowaveOven(EchonetInstance):
    """ECHONET Lite Combination Microwave Oven (Electronic Oven) class.

    Class group code: 0x03
    Class code:       0xB8

    Reference: ECHONET Lite APPENDIX Release R rev.4, Section 3.4.3
    """

    EPC_FUNCTIONS = {
        # --- Standard device properties ---
        0x80: [_int, {0x30: "on", 0x31: "off"}],           # Operation status
        # --- Device-specific properties ---
        0xB0: [_int, {0x41: "open", 0x42: "closed"}],      # Door open/close status
        0xB1: [_int, HEATING_STATUS],                        # Heating status
        0xB2: [_int, {                                       # Heating setting
            0x41: "start",
            0x42: "suspend",
            0x43: "stop",
        }],
        0xE0: [_int, HEATING_MODES],                         # Heating mode setting
        0xE1: [_int, {                                       # Automatic heating setting
            0x41: "automatic",
            0x42: "manual",
            0xFF: None,
        }],
        0xE2: [_int, {                                       # Automatic heating level
            0x31: 1,
            0x32: 2,
            0x33: 3,
            0x34: 4,
            0x35: 5,
            0xFF: None,
        }],
        0xD0: _int,                                          # Automatic heating menu (raw code)
        0xD1: [_int, OVEN_MODES],                            # Oven mode setting
        0xD5: [_int, {                                       # Oven preheating setting
            0x41: "with-preheating",
            0x42: "without-preheating",
            0xFF: None,
        }],
        0xD6: [_int, FERMENTING_MODES],                      # Fermenting mode setting
        0xE3: _chamber_temperature,                          # Chamber temperature (°C)
        0xE4: _food_temperature,                             # Food temperature (°C)
        0xE5: _hh_mm_ss,                                     # Heating time (HH:MM:SS)
        0xE6: _hh_mm_ss,                                     # Remaining heating time
        0xE7: _microwave_power,                              # Microwave heating power (W)
        0xE8: _prompt_messages,                              # Prompt message setting
        0xE9: _accessories_bitmap,                           # Accessories bitmap
        # 0xEA: display string (Set only — not decoded on GET)
        0xEB: _two_stage_duration,                           # Two-stage durations
        0xEC: _two_stage_power,                              # Two-stage powers (W)
    }

    def __init__(self, host: str, api, instance: int = 0x01):
        super().__init__(host, 0x03, 0xB8, instance, api)