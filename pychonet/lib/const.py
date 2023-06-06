from pychonet.version import __version__ as VERSION
# Echonetlite message format:
#
# - EDT0     |Property value data             |01 ..|01 01 30 01
#  - NUM     |Total number of instances       |01   |1
#  - EOJ     |ECHONET Lite object specificat..|01 ..|01 30 01
#    - EOJX1 |Class group code                |01   |Air conditioner-related device class group
#    - EOJX2 |Class code                      |30   |Home air conditioner class
#    - EOJX3 |Instance code                   |01   |1

ENL_PORT = 3610
ENL_MULTICAST_ADDRESS = "224.0.23.0"
MESSAGE_TIMEOUT = 200


# ------------------------------------------------------------------
# EHD1: ECHONET Lite Header 1
# ---------------------------------------------------------------- */
EHD1 = {0x00: "Not available", 0x10: "Conventional ECHONET Lite Specification"}

# ------------------------------------------------------------------
# EHD1: ECHONET Lite Header 2
# ---------------------------------------------------------------- */
EHD2 = {
    0x81: "Format 1 (specified message format)",
    0x82: "Format 2 (arbitrary message format)",
}

# ------------------------------------------------------------------
# ESV
# ------------------------------------------------------------------
GETC = 0x60 # Deprecated, for backward compatibility
SETI = 0x60
SETC = 0x61
GET = 0x62
INFREQ = 0x63
SETGET = 0x6E
SETRES = 0x71
GETRES = 0x72
INF = 0x73
INFC = 0x74
INFC_RES = 0x7A
SETGET_RES = 0x7E
SETI_SNA = 0x50
SETC_SND = 0x51
GET_SNA = 0x52
INF_SNA = 0x53
SETGET_SNA = 0x5E
INSTANCE_LIST = 0xD6

ESV_CODES = {
    0x60: {
        "name": "SetI",
        "description": "Property value write request (no response required)",
    },
    0x61: {
        "name": "SetC",
        "description": "Property value write request (response required)",
    },
    0x62: {"name": "Get", "description": "Property value read request"},
    0x63: {"name": "INF_REQ", "description": "Property value notification request"},
    0x6E: {"name": "SetGet", "description": "Property value write & read request"},
    0x71: {
        "name": "Set_Res",
        "description": "Property value Property value write response",
    },
    0x72: {"name": "Get_Res", "description": "Property value read response"},
    0x73: {"name": "INF", "description": "Property value notification"},
    0x74: {
        "name": "INFC",
        "description": "Property value notification (response required)",
    },
    0x7A: {"name": "INFC_Res", "description": "Property value notification response"},
    0x7E: {"name": "SetGet_Res", "description": "Property value write & read response"},
    0x50: {
        "name": "SetI_SNA",
        "description": "Property value write request (response not possible)",
    },
    0x51: {
        "name": "SetC_SNA",
        "description": "Property value write request (response not possible)",
    },
    0x52: {
        "name": "Get_SNA",
        "description": "Property value read (response not possible)",
    },
    0x53: {
        "name": "INF_SNA",
        "description": "Property value notification (response not possible)",
    },
    0x5E: {
        "name": "SetGet_SNA",
        "description": "Property value write & read (response not possible)",
    },
}

MANUFACTURERS = {
    0x000001: "Hitachi",
    0x000005: "Sharp",
    0x000006: "Mitsubishi Electric",
    0x000008: "DAIKIN INDUSTRIES",
    0x000009: "NEC",
    0x00000B: "Panasonic",
    0x00000D: "Panasonic System Networks",
    0x000012: "Oi",
    0x000015: "Daikin Systems & Solutions Laboratory",
    0x000016: "Toshiba",
    0x000017: "Toshiba Carrier",
    0x00001B: "Toshiba Lighting & Technology",
    0x000022: "Hitach Appliance",
    0x000023: "NTT Comware",
    0x000025: "LIXIL",
    0x00002C: "AFT",
    0x00002E: "SHIKOKU INSTRUMENTATION",
    0x00002F: "AIPHONE",
    0x000034: "MITSUBISHI ELECTRIC ENGINEERING",
    0x000035: "Toshiba Toko Meter Systems",
    0x000036: "NISSIN SYSTEMS",
    0x000038: "Adosol Nissin",
    0x000039: "Sanden",
    0x00003A: "Sekisui House",
    0x00003B: "Kyocera",
    0x00003C: "Denso",
    0x00003D: "Sumitomo Electric Industries",
    0x00003E: "Sumitomo Electric Networks",
    0x000040: "Hitach Hi-Tech Solutions",
    0x000041: "Enegate",
    0x000043: "Toshiba Digital Media Engineering",
    0x000044: "Hitach Industrial Equipment Systems",
    0x000045: "TIS",
    0x000047: "NTT East",
    0x000048: "Oki Electric Industry",
    0x00004D: "INABA DENKI SANGYO",
    0x00004E: "Fujitsu",
    0x00004F: "Daiwa House Industry",
    0x000050: "TOTO",
    0x000051: "Fuji IT",
    0x000052: "Osaki Electric",
    0x000053: "Ubiquitous",
    0x000054: "Noritz",
    0x000055: "Familynet Japan",
    0x000056: "iND",
    0x000057: "Elii Power",
    0x000058: "Mediotech",
    0x000059: "Rinnai",
    0x00005C: "Transboot",
    0x00005E: "GWSOLAR",
    0x000060: "Sony CSL",
    0x000061: "NTT Data Intellilink",
    0x000063: "Kawamura Electric",
    0x000064: "OMRON",
    0x000067: "CORONA",
    0x000068: "Aisin Seiki",
    0x000069: "Toshiba Lifestyle Products & Services",
    0x00006A: "Okaya",
    0x00006B: "ISB",
    0x00006C: "Nichicon",
    0x00006E: "Soundvision",
    0x00006F: "Buffalo",
    0x000070: "CEC",
    0x000071: "Nihon Sangyo",
    0x000072: "Eneres",
    0x000073: "NEC Platforms",
    0x000075: "RICOH IT Solutions",
    0x000076: "TSP",
    0x000077: "Kanagawa Institute of Technology",
    0x000078: "Hitach Maxell",
    0x000079: "ANRITSU Engineering",
    0x00007A: "Zuken Elmic",
    0x00007C: "Nihon Systemware",
    0x00007E: "SMK",
    0x00007F: "Anritsu Customer Support",
    0x000080: "Tabuchi Electric",
    0x000081: "Iwatsu Electric",
    0x000082: "Purpose",
    0x000083: "Melco Techno Yokohama",
    0x000084: "Rohm",
    0x000085: "Takaoka Toko",
    0x000086: "NTT West",
    0x000087: "IO Data Device",
    0x000088: "Chofu Seisakusho",
    0x000089: "Hokkaido Electric Industries",
    0x00008A: "Fujitsu General",
    0x00008C: "Kyuden Technosystems",
    0x00008D: "NTT",
    0x00008E: "Yamaha",
    0x00008F: "Glamo",
    0x000090: "Fujitsu Component",
    0x000091: "NEC Engineering",
    0x000092: "LSIS",
    0x000093: "Satori Electric",
    0x000095: "Yamato Denki",
    0x000096: "Azbil",
    0x000097: "Future Technology Laboratories",
    0x000099: "Tokyo Electric Power Company Holdings",
    0x00009A: "The Kansai Electric Power Company",
    0x00009B: "Gastar",
    0x00009C: "Diamond Electric Mfg",
    0x00009E: "Yaskawa Electric",
    0x00009F: "GS Yuasa International",
    0x0000A0: "NTT Advance Technology",
    0x0000A1: "Honda R&D",
    0x0000A2: "Renaisance",
    0x0000A3: "Chubu Electric Power Company",
    0x0000A5: "Nichibei",
    0x0000A7: "Jel System",
    0x0000A8: "Smart Power System",
    0x0000A9: "Onkyo Development & Manufacturing",
    0x0000AA: "Ten Feet Wright",
    0x0000AC: "IDEC",
    0x0000AD: "Delta Electronics",
    0x0000AE: "Shikoku Electric Power Company",
    0x0000AF: "Takara Standard",
    0x0000B0: "Naltec",
    0x0000B1: "Internet Initiative Japan",
    0x0000B2: "NF",
    0x0000B3: "Toppers Project",
    0x0000B4: "4R Energy",
    0x0000B5: "The Chugoku Electric Power Company",
    0x0000B6: "Bunka Shutter",
    0x0000B7: "Nitto Kogyo",
    0x0000B8: "Hokkaido Electric Power Company",
    0x0000B9: "Energy Demand Side Service Development",
    0x0000BA: "Sankyo Tateyama",
    0x0000BB: "Hokuriku Electric Power Company",
    0x0000BC: "Tohoku Electric Power Company",
    0x0000BE: "Denken",
    0x0000BF: "Kyushyu Electric Power Company",
    0x0000C1: "Tsuken Electric Ind",
    0x0000C2: "Tohoku Electric Meter Industry",
    0x0000C3: "JEMIC",
    0x0000C5: "Sanwa Shutter",
    0x0000C9: "Kikusui",
    0x0000CA: "JSP",
    0x0000CB: "Fuji Electric",
    0x0000CC: "Hitach-Johnson Controls Air Conditioning",
    0x0000CD: "Toclas",
    0x0000CE: "Shindengen Electric Manufacturing",
    0x0000D0: "Tsubamoto Chain",
    0x0000D1: "Takebishi",
    0x0000D2: "Chofukosan",
    0x0000D4: "Murata Manufacturing",
    0x0000D5: "Chosyu Industry",
    0x0000D6: "Sassor",
    0x0000D7: "Kaga Electronics",
    0x0000D8: "Osaki Datatech",
    0x0000D9: "Toshiba IT Control Systems",
    0x0000DA: "Panasonic Commercial Equipment Systems",
    0x0000DB: "Santech Power Japan",
    0x0000DC: "Nihon Techno",
    0x0000DD: "EneStone",
    0x0000DE: "Fuji Xerox Hokkaido",
    0x0000E0: "Looop",
    0x0000E1: "Softbank",
    0x0000E2: "NextDrive",
    0x0000E3: "DDL",
    0x0000E4: "Technoeyes",
    0x0000E5: "Hitach Power Solutions",
    0x0000E6: "Hokkaido Electrical Safty Services Foundation",
    0x0000E7: "Infometis",
    0x0000E8: "Koizumi Lighting Technology",
    0x0000E9: "NTT Smile Energy",
    0x0000EA: "SI Solar",
    0x0000EB: "Nichicon Kameoka",
    0x0000EC: "Toshiba Energy Systems & Solutions",
    0x0000ED: "Infini",
    0x0000EE: "Tessera Technology",
    0x0000EF: "Toyoda industories",
    0x0000F0: "Kaneka",
    0x0000F1: "Laplace Systems",
    0x0000F2: "Energy Solutions",
    0x0000F3: "Energy Gateway",
    0x0000F4: "Denso Aircool",
    0x0000F6: "Field Logic",
    0x0000F7: "JCity",
    0x0000F8: "Avenir",
    0x0000F9: "Toho Electronics",
    0x0000FA: "Plat Home",
    0x0000FB: "CICO",
    0x0000FC: "Fuji Industrial",
    0x0000FD: "Bellnix",
    0x0000FE: "Panasonic Ecology Systems",
    0x0000FF: "TEPCO Energy Partner",
    0x000100: "Smart Solar",
    0x000101: "Sunpot",
    0x000102: "NICHICON (KUSATSU)",
    0x000103: "Data Technology",
    0x000104: "Next Energy & Resources",
    0x000105: "Mitsubishi Electric Lighting",
    0x000106: "Nature",
    0x000107: "SEIKO ELECTRIC",
    0x000108: "SOUSEI Technology",
    0x000109: "DENSO",
    0x00010A: "ENERGY GAP",
    0x00010B: "KITANIHON ELECTRIC CABLE",
    0x00010C: "MAX",
    0x00010D: "Shizen Energy",
    0x00010E: "SANIX INCORPORATED",
    0x00010F: "Iwatani",
    0x000110: "ASUKA SOLUTION",
    0x000111: "Topre",
    0x000112: "NICHIEI INTEC",
    0x000113: "EBARA JITSUGYO POWER",
    0x000114: "OkayaKiden",
    0x000115: "HUAWEI TECHNOLOGIES JAPAN",
    0x000116: "Sungrow Power Supply",
    0x000117: "WWB",
    0x000118: "NEC Magnus Communications",
    0x000119: "DAIHEN",
    0x00011A: "ACCESS",
    0x00011B: "SolaX Power Network Technology (Zhe jiang)",
    0x00011C: "SANDEN RETAIL SYSTEMS",
    0x00011D: "mui Lab",
    0x00011E: "SAKAIGAWA",
    0x00011F: "TOYOTA TSUSHO",
    0x000120: "Meisei electric",
    0x000121: "TOYOTA MOTOR",
    0x000122: "Hanwha Q CELLS Japan",
    0x000123: "Contec",
    0x000125: "LiveSmart",
    0x000126: "Togami Electric Mfg",
    0x000127: "Paloma",
    0x000128: "SAIKOH ENGINEERING",
    0x000129: "GoodWe Japan",
    0x00012A: "Monochrome",
    0x00012B: "DENSO WAVE INCORPORATED",
    0x00012C: "Onamba",
    0x00012E: "Eneres",
    0x00012F: "FORMOSA BIO AND ENERGY CORP JAPAN",
    0xFFFFFE: "Undefined",
    0xFFFFFF: "Experimental",
}

ENL_ON = 0x30
ENL_OFF = 0x31
ENL_STATUS = 0x80
ENL_UID = 0x83
ENL_INSTANTANEOUS_POWER = 0x84
ENL_CUMULATIVE_POWER = 0x85
ENL_MANUFACTURER = 0x8A
ENL_PRODUCT_CODE = 0x8C
ENL_CUMULATIVE_RUNTIME = 0x9A
ENL_STATMAP = 0x9D
ENL_SETMAP = 0x9E
ENL_GETMAP = 0x9F
