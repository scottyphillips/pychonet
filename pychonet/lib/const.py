VERSION = "2.0.11"
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

# ------------------------------------------------------------------
# EHD1: ECHONET Lite Header 1
# ---------------------------------------------------------------- */
EHD1 = {
    0x00: 'Not available',
    0x10: 'Conventional ECHONET Lite Specification'
}

# ------------------------------------------------------------------
# EHD1: ECHONET Lite Header 2
# ---------------------------------------------------------------- */
EHD2 = {
    0x81: 'Format 1 (specified message format)',
    0x82: 'Format 2 (arbitrary message format)'
}

# ------------------------------------------------------------------
# ESV
# ------------------------------------------------------------------
GETC = 			0x60
SETC = 			0x61
GET  = 			0x62
INFREQ =		0x63
SETGET = 		0x6E
SETRES =		0x71
GETRES =		0x72
INF =			0x73
INFC = 			0x74
INFC_RES =		0x7A
SETGET_RES =	0x7E
SETI_SNA = 		0x50
SETC_SND =		0x51
GET_SNA = 		0x52
INF_SNA = 		0x53
SETGET_SNA =	0x5E
INSTANCE_LIST = 0xD6

ESV_CODES = {
	0x60: {'name': 'GetC', 'description': 'Property value write request (no response required)'},
	0x61: {'name': 'SetC', 'description': 'Property value write request (response required)'},
	0x62: {'name': 'Get', 'description': 'Property value read request'},
	0x63: {'name': 'INF_REQ', 'description': 'Property value notification request'},
	0x6E: {'name': 'SetGet', 'description': 'Property value write & read request'},
	0x71: {'name': 'Set_Res', 'description': 'Property value Property value write response'},
	0x72: {'name': 'Get_Res' , 'description': 'Property value read response'},
	0x73: {'name': 'INF' , 'description': 'Property value notification'},
	0x74: {'name': 'INFC', 'description': 'Property value notification (response required)'},
	0x7A: {'name': 'INFC_Res' , 'description': 'Property value notification response'},
	0x7E: {'name': 'SetGet_Res' , 'description': 'Property value write & read response'},
	0x50: {'name': 'SetI_SNA', 'description': 'Property value write request (response not possible)'},
	0x51: {'name': 'SetC_SNA' , 'description': 'Property value write request (response not possible)'},
	0x52: {'name': 'Get_SNA', 'description': 'Property value read (response not possible)'},
	0x53: {'name': 'INF_SNA', 'description': 'Property value notification (response not possible)'},
    0x5E: {'name': 'SetGet_SNA', 'description': 'Property value write & read (response not possible)'}
}

MANUFACTURERS = {
    0x000005: 'Sharp Corporation',
    0x000006: 'Mitsubishi Electric Corp.',
    0x000008: 'DAIKIN INDUSTRIES, LTD.',
    0x000009: 'NEC Corporation',
    0x00000B: 'Panasonic Corporation',
    0x000017: 'Toshiba Carrier Corporation',
    0x00001B: 'TOSHIBA LIGHTING & TECHNOLOGY CORPORATION',
    0x000022: 'Hitachi Global Life Solutions, Inc.',
    0x00002F: 'AIPHONE CO., LTD.',
    0x00004E: 'FUJITSU LIMITED',
    0x000053: 'Ubiquitous Corporation',
    0x000059: 'Rinnai Corporation',
    0x00005E: 'GWSOLAR Corporation',
    0x000063: 'Kawamura Electric Inc.',
    0x000064: 'OMRON Corporation',
    0x000069: 'Toshiba Lifestyle Products & Services Corporation',
    0x00006F: 'BUFFALO INC.',
    0x000072: 'Eneres Co., Ltd.',
    0x000077: 'Kanagawa Institute of Technology',
    0x000078: 'Hitachi Maxell, Ltd.',
    0x00007D: 'POWERTECH INDUSTRIAL CO., LTD.',
    0x000081: 'IWATSU ELECTRIC CO., LTD.',
    0x000086: 'NIPPON TELEGRAPH AND TELEPHONE WEST CORPORATION',
    0x00008A: 'FUJITSU GENERAL LIMITED',
    0x00008C: 'Kyuden Technosystems Corporation',
    0x000097: 'Future Technology Laboratories',
    0x0000AA: 'TEN FEET WRIGHT INC.',
    0x0000B6: 'Bunka Shutter Co., Ltd.',
    0xFFFFFF: 'Experimental',
    0xFFFFFE: 'Undefined'
}

ENL_ON = 0x30
ENL_OFF = 0x31
ENL_STATUS = 0x80
ENL_UID = 0x83
ENL_CUMULATIVE_POWER = 0x85
ENL_MANUFACTURER = 0x8A
ENL_CUMULATIVE_RUNTIME = 0x9A
ENL_SETMAP = 0x9E
ENL_GETMAP = 0x9F
