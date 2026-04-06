import logging

from .const import EHD1, EHD2, ESV_CODES
from .eojx import EOJX_CLASS, EOJX_GROUP

# Echonet message constants
DEFAULT_EHD = 0x1081       # Default EHD value (EHD1 + EHD2)
DEFAULT_SEOJ = 0x05FF01    # Default SEOJ (Service Object ID)
MAX_TID_VALUE = 0xFFFF     # Maximum Transaction ID (2 bytes)


class TIDError(Exception):
    """Exception raised for invalid Transaction ID."""

    pass


class DecodeEchonetMsgError(Exception):
    """Exception raised when decoding Echonet message fails."""

    pass


logger = logging.getLogger(__name__)


def decodeEchonetMsg(byte):
    data = {}
    try:
        data["EHD1"] = byte[0]
        if data["EHD1"] not in EHD1:
            raise ValueError("EHD1 Header invalid")
        data["EHD2"] = byte[1]
        if data["EHD2"] not in EHD2:
            raise ValueError("EHD2 Header invalid")
        data["TID"] = int.from_bytes(byte[2:4], byteorder="big")

        # Decode SEOJ
        data["SEOJGC"] = byte[4]
        data["SEOJCC"] = byte[5]
        data["SEOJCI"] = byte[6]
        # Decode DEOJ
        data["DEOJGC"] = byte[7]
        data["DEOJCC"] = byte[8]
        data["DEOJCI"] = byte[9]

        # Decode Service property
        data["ESV"] = byte[10]

        i = 0
        epc_pointer = 12
        data["OPC"] = []
        # decode multiple processing properties (OPC)
        while i < (byte[11]):
            OPC = {}
            pdc_pointer = epc_pointer + 1
            edt_pointer = pdc_pointer + 1
            end_pointer = edt_pointer
            OPC["EPC"] = byte[epc_pointer]
            OPC["PDC"] = byte[pdc_pointer]
            pdc_len = byte[pdc_pointer]
            end_pointer += pdc_len
            OPC["EDT"] = byte[edt_pointer:end_pointer]
            epc_pointer = end_pointer
            i += 1
            data["OPC"].append(OPC)

    except ValueError as error:
        logger.error("Failed to decode Echonet message: %s", error)
        raise DecodeEchonetMsgError(f"Failed to decode Echonet message: {error}") from error
    return data


def buildEchonetMsg(data):
    message = DEFAULT_EHD

    # validate TID (set a default value if none provided)
    if "TID" not in data:
        data["TID"] = 0x0001
    elif data["TID"] > MAX_TID_VALUE:
        raise TIDError(f"Transaction ID {data['TID']} exceeds maximum value of {MAX_TID_VALUE:#x}")
    message = (message << 16) + data["TID"]

    # append default SEOJ
    message = (message << 24) + DEFAULT_SEOJ

    # validate DEOJ
    if data["DEOJGC"] in EOJX_GROUP:
        message = (message << 8) + data["DEOJGC"]
    else:
        raise ValueError(
            "Value " + str(hex(data["DEOJGC"])) + " not a valid SEO Group code"
        )

    if data["DEOJCC"] in EOJX_CLASS[data["DEOJGC"]]:
        message = (message << 8) + data["DEOJCC"]
    else:
        raise ValueError(
            "Value " + str(hex(data["DEOJCC"])) + " missing from SEO Class table. Check current ECHONETlite specs for any update."
        )

    message = (message << 8) + data["DEOJCI"]

    # validate ESV by looking up the codes.
    if data["ESV"] in ESV_CODES:
        # ESV code is a string
        message = (message << 8) + data["ESV"]
    else:
        raise ValueError("Value not in ESV code table")

    # validate OPC
    message = (message << 8) + len(data["OPC"])

    # You can have multiple OPC per transaction.
    for values in data["OPC"]:
        # validate EPC
        message = (message << 8) + values["EPC"]
        if "PDC" in values:
            message = (message << 8) + values["PDC"]
            # if PDC has a value then concat EDT to message
            if values["PDC"] > 0:
                message = (message << 8 * values["PDC"]) + values["EDT"]
        else:
            message = (message << 8) + 0x00
    # print(message)
    return bytearray.fromhex(format(int(message), "x"))


def preparePayload(tid, deojgc, deojcc, deojci, esv, opc):
    tx_payload = {
        "TID": tid,  # Transaction ID 1
        "DEOJGC": deojgc,
        "DEOJCC": deojcc,
        "DEOJCI": deojci,
        "ESV": esv,
        "OPC": opc,
    }
    return tx_payload
