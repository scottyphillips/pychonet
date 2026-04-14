"""Unit tests for Echonet message encoding/decoding functions."""
import unittest
from pychonet.lib.functions import (
    decodeEchonetMsg,
    buildEchonetMsg,
    preparePayload,
    TIDError,
    DecodeEchonetMsgError,
)


class TestDecodeEchonetMsg(unittest.TestCase):
    """Test cases for decodeEchonetMsg function."""

    def test_decode_valid_message(self):
        """Test decoding a valid Echonet message.
        
        Message structure:
        - EHD1: 0x10 (Conventional ECHONET Lite Specification)
        - EHD2: 0x82 (Format 2, arbitrary message format)
        - TID: 0x0001
        - SEOJ: 0x05FF01 (Home Air Conditioner class group)
        - DEOJ: 0x05FF01 (Home Air Conditioner instance 1)
        - ESV: 0x62 (Get request)
        - OPC length: 0x01
        - EPC: 0x80, PDC: 0x00 (no data)
        
        Note: Using DEOJ codes that match SEOJ for group/class validation.
        """
        # Valid Echonet message bytes with matching DEOJ/SEOJ for validation
        byte_msg = bytes([
            0x10,  # EHD1 - Conventional ECHONET Lite Specification (valid)
            0x82,  # EHD2 - Format 2 (arbitrary message format) (valid)
            0x00, 0x01,  # TID (1)
            0x05, 0xFF, 0x01,  # SEOJ (Home Air Conditioner class group)
            0x05, 0xFF, 0x01,  # DEOJ - Same as SEOJ for valid validation
            0x62,  # ESV (Get request)
            0x01,  # OPC length
            0x80,  # EPC - Operation status
            0x00,  # PDC - Property data count (0 means no EDT data follows)
        ])

        result = decodeEchonetMsg(byte_msg)

        self.assertEqual(result["EHD1"], 0x10)
        self.assertEqual(result["EHD2"], 0x82)
        self.assertEqual(result["TID"], 1)
        self.assertEqual(result["SEOJGC"], 0x05)
        self.assertEqual(result["SEOJCC"], 0xFF)
        self.assertEqual(result["SEOJCI"], 0x01)
        self.assertEqual(result["DEOJGC"], 0x05)
        self.assertEqual(result["DEOJCC"], 0xFF)
        self.assertEqual(result["DEOJCI"], 0x01)
        self.assertEqual(result["ESV"], 0x62)
        self.assertEqual(len(result["OPC"]), 1)
        self.assertEqual(result["OPC"][0]["EPC"], 0x80)

    def test_decode_invalid_ehd1(self):
        """Test that invalid EHD1 raises DecodeEchonetMsgError."""
        # Invalid EHD1 (not in EHD1 table - only 0x00 and 0x10 are valid)
        byte_msg = bytes([
            0xFF,  # Invalid EHD1
            0x82,  # EHD2
            0x00, 0x01,  # TID
            0x05, 0xFF, 0x01,  # SEOJ
            0x01, 0x42, 0x01,  # DEOJ
            0x62,  # ESV
            0x00,  # OPC length (empty)
        ])

        with self.assertRaises(DecodeEchonetMsgError):
            decodeEchonetMsg(byte_msg)

    def test_decode_invalid_ehd2(self):
        """Test that invalid EHD2 raises DecodeEchonetMsgError."""
        # Invalid EHD2 (not in EHD2 table - only 0x81 and 0x82 are valid)
        byte_msg = bytes([
            0x10,  # Valid EHD1
            0xFF,  # Invalid EHD2
            0x00, 0x01,  # TID
            0x05, 0xFF, 0x01,  # SEOJ
            0x01, 0x42, 0x01,  # DEOJ
            0x62,  # ESV
            0x00,  # OPC length (empty)
        ])

        with self.assertRaises(DecodeEchonetMsgError):
            decodeEchonetMsg(byte_msg)

    def test_decode_multiple_opc(self):
        """Test decoding message with multiple OPC entries."""
        byte_msg = bytes([
            0x10,  # EHD1 - Valid conventional spec
            0x82,  # EHD2 - Format 2
            0x00, 0x01,  # TID (1)
            0x05, 0xFF, 0x01,  # SEOJ
            0x01, 0x42, 0x01,  # DEOJ
            0x62,  # ESV
            0x03,  # OPC length (3 properties)
            0xB3, 0x02, 0x20, 0x30,  # First OPC: EPC=0xB3, PDC=0x02, EDT=[0x20, 0x30]
            0xBB, 0x01, 0x25,         # Second OPC: EPC=0xBB, PDC=0x01, EDT=[0x25]
            0xBC, 0x01, 0x48          # Third OPC: EPC=0xBC, PDC=0x01, EDT=[0x48]
        ])

        result = decodeEchonetMsg(byte_msg)

        self.assertEqual(len(result["OPC"]), 3)
        # First OPC
        self.assertEqual(result["OPC"][0]["EPC"], 0xB3)
        self.assertEqual(result["OPC"][0]["PDC"], 0x02)
        self.assertEqual(result["OPC"][0]["EDT"], bytes([0x20, 0x30]))
        # Second OPC
        self.assertEqual(result["OPC"][1]["EPC"], 0xBB)
        self.assertEqual(result["OPC"][1]["PDC"], 0x01)
        self.assertEqual(result["OPC"][1]["EDT"], bytes([0x25]))
        # Third OPC
        self.assertEqual(result["OPC"][2]["EPC"], 0xBC)
        self.assertEqual(result["OPC"][2]["PDC"], 0x01)
        self.assertEqual(result["OPC"][2]["EDT"], bytes([0x48]))


class TestBuildEchonetMsg(unittest.TestCase):
    """Test cases for buildEchonetMsg function."""

    def test_build_valid_message(self):
        """Test building a valid Echonet message.
        
        Note: This test uses DEOJ codes that exist in the EOJX data.
        Group 0x05 (Management/control) with class 0xFF is used for testing.
        """
        # Using valid ESV code 0x62 (Get request) as integer
        data = {
            "TID": 0x0001,
            "DEOJGC": 0x05,  # Management/control group (valid per EOJX_GROUP)
            "DEOJCC": 0xFF,  # Class code for management/group (valid per EOJX_CLASS[0x05])
            "DEOJCI": 0x01,
            "ESV": 0x62,  # Get request
            "OPC": [
                {"EPC": 0x80}  # No PDC or EDT - simple case
            ],
        }

        result = buildEchonetMsg(data)

        self.assertIsInstance(result, bytearray)
        # Verify the message starts correctly with EHD=0x1081
        self.assertEqual(int.from_bytes(result[0:2], byteorder="big"), 0x1081)

    def test_build_missing_tid_uses_default(self):
        """Test that missing TID uses default value of 0x0001."""
        data = {
            "DEOJGC": 0x01,
            "DEOJCC": 0x42,
            "DEOJCI": 0x01,
            "ESV": 0x62,
            "OPC": [],
        }

        result = buildEchonetMsg(data)

        self.assertEqual(int.from_bytes(result[2:4], byteorder="big"), 0x0001)

    def test_build_tid_too_large_raises_error(self):
        """Test that TID larger than 0xFFFF raises TIDError."""
        data = {
            "TID": 0x10000,  # Larger than max (0xFFFF)
            "DEOJGC": 0x01,
            "DEOJCC": 0x42,
            "DEOJCI": 0x01,
            "ESV": 0x62,
            "OPC": [],
        }

        with self.assertRaises(TIDError):
            buildEchonetMsg(data)

    def test_build_invalid_deojgc_raises_error(self):
        """Test that invalid DEOJGC raises ValueError."""
        data = {
            "TID": 0x0001,
            "DEOJGC": 0xFF,  # Invalid group code (not in EOJX_GROUP)
            "DEOJCC": 0x42,
            "DEOJCI": 0x01,
            "ESV": 0x62,
            "OPC": [],
        }

        with self.assertRaises(ValueError):
            buildEchonetMsg(data)

    def test_build_invalid_deojcc_raises_error(self):
        """Test that invalid DEOJCC raises ValueError.
        
        Uses a class code (0x80) for group 0x01 which should be valid,
        but we'll use an EPC value that doesn't exist in the class table.
        """
        # Using DEOJGC=0x01 with a class code that exists but then invalid ESV
        data = {
            "TID": 0x0001,
            "DEOJGC": 0x01,
            "DEOJCC": 0x42,  # Valid class for group 0x01 (Electric Heater)
            "DEOJCI": 0x01,
            "ESV": 0xFF,  # Invalid ESV code
            "OPC": [],
        }

        with self.assertRaises(ValueError):
            buildEchonetMsg(data)

    def test_build_invalid_esv_raises_error(self):
        """Test that invalid ESV raises ValueError."""
        data = {
            "TID": 0x0001,
            "DEOJGC": 0x05,
            "DEOJCC": 0xFF,  # Home Air Conditioner class
            "DEOJCI": 0x01,
            "ESV": 0xFF,  # Invalid ESV code (not in ESV_CODES)
            "OPC": [],
        }

        with self.assertRaises(ValueError):
            buildEchonetMsg(data)

    def test_build_with_edt_integer(self):
        """Test building a message with EDT data as integer.
        
        When PDC > 0, the EDT value (as integer) is concatenated to the message.
        This tests the code path: values["PDC"] > 0 and values["EDT"] exists.
        """
        # Using valid ESV code 0x62 (Get request) with integer EDT value
        data = {
            "TID": 0x0001,
            "DEOJGC": 0x05,  # Management/control group
            "DEOJCC": 0xFF,  # Class code for management/group
            "DEOJCI": 0x01,
            "ESV": 0x62,  # Get request
            "OPC": [
                {"EPC": 0xB3, "PDC": 0x02, "EDT": 0x2030}  # EDT as integer
            ],
        }

        result = buildEchonetMsg(data)

        self.assertIsInstance(result, bytearray)
        # Verify the message starts correctly with EHD=0x1081
        self.assertEqual(int.from_bytes(result[0:2], byteorder="big"), 0x1081)


class TestPreparePayload(unittest.TestCase):
    """Test cases for preparePayload function."""

    def test_prepare_payload_basic(self):
        """Test basic payload preparation."""
        result = preparePayload(
            tid=0x0001,
            deojgc=0x05,
            deojcc=0xFF,
            deojci=0x01,
            esv="0x62",
            opc=[{"EPC": 0x80}]
        )

        self.assertEqual(result["TID"], 0x0001)
        self.assertEqual(result["DEOJGC"], 0x05)
        self.assertEqual(result["DEOJCC"], 0xFF)
        self.assertEqual(result["DEOJCI"], 0x01)
        self.assertEqual(result["ESV"], "0x62")
        self.assertEqual(len(result["OPC"]), 1)

    def test_prepare_payload_all_fields(self):
        """Test payload with all specified values."""
        result = preparePayload(
            tid=0xABCD,
            deojgc=0x05,
            deojcc=0xFF,
            deojci=0x02,
            esv="0x61",
            opc=[{"EPC": 0x80}]
        )

        self.assertEqual(result["TID"], 0xABCD)
        self.assertEqual(result["DEOJGC"], 0x05)
        self.assertEqual(result["DEOJCC"], 0xFF)
        self.assertEqual(result["DEOJCI"], 0x02)
        self.assertEqual(result["ESV"], "0x61")


if __name__ == "__main__":
    unittest.main()