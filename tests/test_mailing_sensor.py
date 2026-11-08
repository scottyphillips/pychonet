import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from pychonet import Factory, MailingSensor
from pychonet.lib.const import GET, SETC


class TestMailingSensor(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.properties = {
            0x80: b"\x30",
            0xB0: b"\x31",
            0xB1: b"\x42",
            0x9F: [0x80, 0xB0, 0xB1],
            0x9E: [0x80, 0xB0],
        }
        self.server = SimpleNamespace(
            _state={"device": {"instances": {0x00: {0x0F: {0x02: self.properties}}}}},
            _logger=Mock(),
            echonetMessage=AsyncMock(return_value=True),
        )
        self.sensor = Factory("device", self.server, 0x00, 0x0F, 0x02)

    def test_factory(self):
        self.assertIs(type(self.sensor), MailingSensor)
        self.assertEqual(self.sensor._eojci, 0x02)

    async def test_read_properties(self):
        for getter, epc in [
            (self.sensor.getOperationStatus, 0x80),
            (self.sensor.getDetectionThresholdLevel, 0xB0),
            (self.sensor.getMailingDetectionStatus, 0xB1),
        ]:
            with self.subTest(epc=epc):
                self.assertEqual(await getter(), self.properties[epc])
                self.server.echonetMessage.assert_awaited_with(
                    "device", 0x00, 0x0F, 0x02, GET, [{"EPC": epc, "PDC": 0}]
                )

    async def test_decode_properties(self):
        cases = [
            (0x80, 0x30, "on"),
            (0x80, 0x31, "off"),
            (0xB1, 0x41, "found"),
            (0xB1, 0x42, "not found"),
        ] + [(0xB0, 0x30 + level, f"level-{level}") for level in range(1, 9)]
        for epc, raw, expected in cases:
            with self.subTest(epc=epc, raw=raw):
                self.properties[epc] = bytes([raw])
                self.assertEqual(await self.sensor.update(epc), expected)

    async def test_write_properties(self):
        for setter, epc, value in [
            (self.sensor.setOperationStatus, 0x80, b"\x31"),
            (self.sensor.setDetectionThresholdLevel, 0xB0, b"\x38"),
        ]:
            with self.subTest(epc=epc):
                self.assertTrue(await setter(value))
                self.server.echonetMessage.assert_awaited_with(
                    "device", 0x00, 0x0F, 0x02, SETC,
                    [{"EPC": epc, "PDC": 1, "EDT": value}],
                )

    async def test_cached_notification(self):
        self.properties[0xB1] = b"\x41"
        self.assertEqual(
            await self.sensor.update(0xB1, no_request=True), "found"
        )
        self.server.echonetMessage.assert_not_awaited()

    async def test_failed_requests(self):
        self.server.echonetMessage.return_value = False
        self.assertIsNone(await self.sensor.getMailingDetectionStatus())
        self.assertFalse(await self.sensor.setDetectionThresholdLevel(b"\x31"))
