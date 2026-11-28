"""Exercise request correlation through the real encoder and receive handler."""

import asyncio
import unittest
from unittest.mock import AsyncMock, Mock

from pychonet.echonetapiclient import ECHONETAPIClient, EchonetMaxOpcError
from pychonet.lib.const import (
    ENL_MANUFACTURER,
    ENL_MULTICAST_ADDRESS,
    ENL_PORT,
    ENL_PRODUCT_CODE,
    ENL_UID,
    GET,
    GETRES,
    GET_SNA,
    INF,
    INFC,
    INFC_RES,
    INFREQ,
    INF_SNA,
    INSTANCE_LIST,
    SETC,
    SETC_SND,
    SETI,
    SETRES,
    SETGET,
    SETGET_RES,
    SETGET_SNA,
)
from pychonet.lib.functions import decodeEchonetMsg


HOST = "172.16.1.3"
OTHER_HOST = "172.16.1.4"
AIRCON = (0x01, 0x30, 0x01)
SHUTTER = (0x02, 0x63, 0x01)
LIGHT = (0x02, 0x90, 0x01)
NODE = (0x0E, 0xF0, 0x01)
PROPERTIES = (0xA4, 0xB4, 0xA5)


def packet(tid, eoj=AIRCON, esv=GETRES, properties=None):
    """Build a device packet with its own SEOJ and arbitrary EDT bytes."""
    if properties is None:
        properties = [(epc, b"\x41") for epc in PROPERTIES]
    data = bytearray(b"\x10\x81")
    data.extend(tid.to_bytes(2, "big"))
    data.extend(eoj)
    data.extend(b"\x05\xff\x01")
    data.extend((esv, len(properties)))
    for epc, edt in properties:
        data.extend((epc, len(edt)))
        data.extend(edt)
    return bytes(data)


class TestRequestCorrelation(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.sent = asyncio.Queue()
        self.server = Mock()
        self.server.send.side_effect = lambda data, addr: self.sent.put_nowait(
            (decodeEchonetMsg(data), addr)
        )
        self.api = ECHONETAPIClient(self.server)
        self.api.configure(message_timeout=10, logger=Mock())
        self.api._next_tx_tid = 23949
        for host in (HOST, OTHER_HOST):
            for eoj in (AIRCON, SHUTTER, LIGHT, (1, 0x30, 2)):
                self.api.register_instance(host, *eoj, [], [0x80], list(PROPERTIES))

    async def track(self, coroutine):
        task = asyncio.create_task(coroutine)

        async def finish():
            if not task.done():
                task.cancel()
            await asyncio.gather(task, return_exceptions=True)

        self.addAsyncCleanup(finish)
        return task

    async def start_request(self, host=HOST, eoj=AIRCON, esv=GET, opc=None):
        if opc is None:
            opc = [{"EPC": epc} for epc in PROPERTIES]
        task = await self.track(self.api.echonetMessage(host, *eoj, esv, opc))
        sent, addr = await asyncio.wait_for(self.sent.get(), 1)
        self.assertEqual(addr, (host, ENL_PORT))
        return task, sent["TID"]

    async def receive(self, data, host=HOST):
        await self.api.echonetMessageReceived(data, (host, ENL_PORT))

    def assert_clean(self):
        self.assertEqual(self.api._message_list, {})
        self.assertEqual(self.api._opc_counts, {})
        self.assertEqual(self.api._failure_list, {})
        self.assertTrue(all(count == 0 for count in self.api._waiting.values()))

    async def test_shutter_inf_collision_preserves_get_and_push(self):
        for eoj, expected_tid in ((AIRCON, 23950), (LIGHT, 23951)):
            with self.subTest(eoj=eoj):
                update = AsyncMock()
                receive = AsyncMock()
                self.api.register_async_update_callbacks(HOST, *SHUTTER, update)
                self.api.register_async_receive_callbacks(HOST, *SHUTTER, receive)
                task, tid = await self.start_request(eoj=eoj)
                self.assertEqual(tid, expected_tid)
                pending = self.api._message_list[tid]
                # A different value ensures an update notification each time.
                edt = bytes((expected_tid % 256,))
                await self.receive(packet(tid, SHUTTER, INF, [(0xE0, edt)]))
                self.assertIs(self.api._message_list.get(tid), pending)
                self.assertEqual(self.api._opc_counts, {})
                self.assertEqual(self.api._failure_list, {})
                self.assertFalse(task.done())
                self.assertEqual(
                    self.api.state[HOST]["instances"][2][0x63][1][0xE0], edt
                )
                update.assert_awaited_once_with(True)
                receive.assert_awaited_once_with(True)
                await self.receive(packet(tid, eoj))
                self.assertEqual(self.api._opc_counts[tid], 3)
                self.assertEqual(self.api._failure_list[tid], 0)
                self.assertTrue(await task)
                self.assert_clean()

    async def test_wrong_ip_eoj_or_esv_does_not_consume_get(self):
        cases = [
            (OTHER_HOST, AIRCON, GETRES),
            (HOST, SHUTTER, GETRES),
            (HOST, (1, 0x30, 2), GETRES),
            (HOST, AIRCON, INF),
            (HOST, AIRCON, SETRES),
            (HOST, AIRCON, SETGET_RES),
            (HOST, AIRCON, INFC_RES),
        ]
        for host, eoj, esv in cases:
            with self.subTest(host=host, eoj=eoj, esv=esv):
                task, tid = await self.start_request()
                pending = self.api._message_list[tid]
                await self.receive(packet(tid, eoj, esv), host)
                self.assertIs(self.api._message_list.get(tid), pending)
                self.assertEqual(self.api._opc_counts, {})
                self.assertEqual(self.api._failure_list, {})
                await self.receive(packet(tid))
                self.assertTrue(await task)
                self.assert_clean()

    async def test_same_eoj_inf_preserves_get_counts_and_push(self):
        update = AsyncMock()
        receive = AsyncMock()
        self.api.register_async_update_callbacks(HOST, *AIRCON, update)
        self.api.register_async_receive_callbacks(HOST, *AIRCON, receive)
        task, tid = await self.start_request()
        pending = self.api._message_list[tid]
        await self.receive(packet(tid, esv=INF, properties=[(0xA4, b"\x42")]))
        self.assertIs(self.api._message_list.get(tid), pending)
        self.assertEqual(self.api._opc_counts, {})
        self.assertEqual(self.api._failure_list, {})
        self.assertEqual(self.api.state[HOST]["instances"][1][0x30][1][0xA4], b"\x42")
        update.assert_awaited_once_with(True)
        receive.assert_awaited_once_with(True)
        await self.receive(packet(tid))
        self.assertEqual(self.api._opc_counts[tid], 3)
        self.assertEqual(self.api._failure_list[tid], 0)
        self.assertTrue(await task)
        self.assertEqual(receive.await_args_list[-1].args, (False,))
        self.assert_clean()

    async def test_unsolicited_inf_updates_state_and_callbacks(self):
        update = AsyncMock()
        receive = AsyncMock()
        self.api.register_async_update_callbacks(HOST, *SHUTTER, update)
        self.api.register_async_receive_callbacks(HOST, *SHUTTER, receive)
        await self.receive(packet(123, SHUTTER, INF, [(0xE0, b"\x41")]))
        self.assertEqual(self.api.state[HOST]["instances"][2][0x63][1][0xE0], b"\x41")
        update.assert_awaited_once_with(True)
        receive.assert_awaited_once_with(True)
        self.assert_clean()

    async def test_normal_get(self):
        receive = AsyncMock()
        self.api.register_async_receive_callbacks(HOST, *AIRCON, receive)
        task, tid = await self.start_request()
        await self.receive(packet(tid))
        self.assertTrue(await task)
        receive.assert_awaited_once_with(False)
        self.assert_clean()

    async def test_get_sna_preserves_failure_and_partial_success(self):
        for values, expected in (
            ([(epc, b"") for epc in PROPERTIES], False),
            ([(0xA4, b"\x41"), (0xB4, b""), (0xA5, b"")], True),
        ):
            with self.subTest(expected=expected):
                task, tid = await self.start_request()
                await self.receive(packet(tid, esv=GET_SNA, properties=values))
                self.assertEqual(await task, expected)
                self.assertTrue(self.api.state[HOST]["available"])
                self.assert_clean()

    async def test_set_response_and_sna(self):
        for esv, edt, expected in (
            (SETRES, b"", True),
            (SETC_SND, b"\x30", False),
        ):
            with self.subTest(esv=esv):
                task, tid = await self.start_request(
                    esv=SETC, opc=[{"EPC": 0x80, "PDC": 1, "EDT": 0x30}]
                )
                pending = self.api._message_list[tid]
                await self.receive(packet(tid, esv=GETRES))
                self.assertIs(self.api._message_list.get(tid), pending)
                await self.receive(packet(tid, esv=esv, properties=[(0x80, edt)]))
                self.assertEqual(await task, expected)
                if expected:
                    self.assertEqual(
                        self.api.state[HOST]["instances"][1][0x30][1][0x80], b"\x30"
                    )
                self.assert_clean()

    async def test_seti_does_not_wait_for_response(self):
        task, _ = await self.start_request(
            esv=SETI, opc=[{"EPC": 0x80, "PDC": 1, "EDT": 0x30}]
        )
        self.assertTrue(await task)
        self.assert_clean()

    async def test_short_matching_response_still_raises_max_opc_error(self):
        task, tid = await self.start_request()
        await self.receive(packet(tid, properties=[(0xA4, b"\x41")]))
        with self.assertRaises(EchonetMaxOpcError):
            await task
        self.assert_clean()

    async def test_timeout_after_unrelated_inf(self):
        self.api.configure(message_timeout=1)
        task, tid = await self.start_request()
        await self.receive(packet(tid, SHUTTER, INF, [(0xE0, b"\x41")]))
        self.assertFalse(await task)
        self.assertFalse(self.api.state[HOST]["available"])
        self.assert_clean()

    async def test_timeout_and_late_response(self):
        self.api.configure(message_timeout=1)
        task, tid = await self.start_request()
        self.assertFalse(await task)
        self.assertFalse(self.api.state[HOST]["available"])
        self.assert_clean()
        await self.receive(packet(tid))
        self.assert_clean()

    async def test_unknown_host_collision_preserves_request(self):
        discover = AsyncMock()
        self.api.configure(discover_callback=discover)
        task, tid = await self.start_request()
        pending = self.api._message_list[tid]
        await self.receive(packet(tid), "172.16.1.99")
        discover.assert_awaited_once_with("172.16.1.99")
        self.assertIs(self.api._message_list.get(tid), pending)
        self.assertEqual(self.api._opc_counts, {})
        self.assertEqual(self.api._failure_list, {})
        await self.receive(packet(tid))
        self.assertTrue(await task)
        self.assert_clean()

    async def test_discovery_response(self):
        for host in (HOST, ENL_MULTICAST_ADDRESS):
            with self.subTest(host=host):
                self.api.state[HOST].pop("discovered", None)
                task = await self.track(self.api.discover(host))
                sent, _ = await asyncio.wait_for(self.sent.get(), 1)
                tid = sent["TID"]
                pending = self.api._message_list[tid]
                await self.receive(packet(tid, SHUTTER, INF, [(0xE0, b"\x41")]))
                self.assertIs(self.api._message_list.get(tid), pending)
                # Discovery accepts a unicast reply to a multicast request.
                properties = [(INSTANCE_LIST, b"\x01\x01\x30\x01")]
                if host == HOST:
                    properties = [
                        (ENL_MANUFACTURER, b"\x00\x00\x01"),
                        (ENL_PRODUCT_CODE, b"TEST"),
                        (ENL_UID, b"\xfe" + b"\x01" * 16),
                    ] + properties
                await self.receive(
                    packet(tid, NODE, GETRES, properties)
                )
                self.assertTrue(await task)
                self.assertTrue(self.api.state[HOST]["discovered"])
                self.assert_clean()

    async def test_concurrent_hosts_keep_separate_requests(self):
        first, first_tid = await self.start_request()
        second, second_tid = await self.start_request(host=OTHER_HOST)
        await self.receive(packet(first_tid), OTHER_HOST)
        self.assertIn(first_tid, self.api._message_list)
        self.assertIn(second_tid, self.api._message_list)
        await self.receive(packet(second_tid), OTHER_HOST)
        await self.receive(packet(first_tid))
        self.assertEqual(await asyncio.gather(first, second), [True, True])
        self.assert_clean()

    async def test_inf_during_response_callback_does_not_overwrite_result(self):
        entered = asyncio.Event()
        release = asyncio.Event()

        async def block(_is_push):
            entered.set()
            await release.wait()

        self.api.register_async_receive_callbacks(HOST, *AIRCON, block)
        task, tid = await self.start_request()
        receiver = await self.track(self.receive(packet(tid)))
        await asyncio.wait_for(entered.wait(), 1)
        counts = dict(self.api._opc_counts)
        failures = dict(self.api._failure_list)
        await self.receive(packet(tid, SHUTTER, INF, [(0xE0, b"\x41")]))
        self.assertEqual(self.api._opc_counts, counts)
        self.assertEqual(self.api._failure_list, failures)
        release.set()
        await receiver
        self.assertTrue(await task)
        self.assert_clean()

    async def test_timeout_during_callback_does_not_delete_reused_tid(self):
        entered = asyncio.Event()
        release = asyncio.Event()

        async def block(_is_push):
            entered.set()
            await release.wait()

        self.api.configure(message_timeout=1)
        self.api.register_async_receive_callbacks(HOST, *AIRCON, block)
        task, tid = await self.start_request()
        receiver = await self.track(self.receive(packet(tid)))
        await asyncio.wait_for(entered.wait(), 1)
        self.assertFalse(await task)
        self.assert_clean()
        self.api.unregister_async_receive_callbacks(HOST, *AIRCON)
        self.api._next_tx_tid = tid - 1
        replacement, reused_tid = await self.start_request()
        self.assertEqual(reused_tid, tid)
        pending = self.api._message_list[tid]
        release.set()
        await receiver
        self.assertIs(self.api._message_list.get(tid), pending)
        self.assertEqual(self.api._opc_counts, {})
        self.assertEqual(self.api._failure_list, {})
        await self.receive(packet(tid))
        self.assertTrue(await replacement)
        self.assert_clean()

    async def test_cancellation_cleans_pending_request(self):
        task, _ = await self.start_request()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assert_clean()

    async def test_rollover_skips_pending_tid(self):
        self.api._next_tx_tid = 0
        first, first_tid = await self.start_request()
        pending = self.api._message_list[first_tid]
        self.api._next_tx_tid = 0xFFFF
        second, second_tid = await self.start_request(host=OTHER_HOST)
        self.assertEqual((first_tid, second_tid), (1, 2))
        self.assertIs(self.api._message_list[first_tid], pending)
        await self.receive(packet(second_tid), OTHER_HOST)
        await self.receive(packet(first_tid))
        self.assertEqual(await asyncio.gather(first, second), [True, True])
        self.assert_clean()

    async def test_rollover_skips_result_before_sender_consumes_it(self):
        self.api._next_tx_tid = 0
        first, first_tid = await self.start_request()
        await self.receive(packet(first_tid))
        self.assertNotIn(first_tid, self.api._message_list)
        self.assertEqual(self.api._opc_counts[first_tid], 3)
        self.api._next_tx_tid = 0xFFFF
        second, second_tid = await self.start_request(host=OTHER_HOST)
        self.assertEqual((first_tid, second_tid), (1, 2))
        await self.receive(packet(second_tid), OTHER_HOST)
        self.assertEqual(await asyncio.gather(first, second), [True, True])
        self.assert_clean()

    async def test_rollover_without_collision(self):
        self.api._next_tx_tid = 0xFFFE
        first, first_tid = await self.start_request()
        second, second_tid = await self.start_request(host=OTHER_HOST)
        self.assertEqual((first_tid, second_tid), (0xFFFF, 1))
        await self.receive(packet(first_tid))
        await self.receive(packet(second_tid), OTHER_HOST)
        self.assertEqual(await asyncio.gather(first, second), [True, True])
        self.assert_clean()

    async def test_timeout_cleanup_preserves_other_requests_result(self):
        entered = asyncio.Event()
        release = asyncio.Event()

        async def block(_is_push):
            entered.set()
            await release.wait()

        self.api.configure(message_timeout=1)
        self.api.register_async_update_callbacks(HOST, *AIRCON, block)
        self.api._next_tx_tid = 0
        first, first_tid = await self.start_request()
        await asyncio.wait_for(entered.wait(), 1)
        self.api._next_tx_tid = 0xFFFF
        second, second_tid = await self.start_request(host=OTHER_HOST)
        await self.receive(packet(second_tid), OTHER_HOST)
        release.set()
        self.assertFalse(await first)
        self.assertEqual(self.api._opc_counts.get(second_tid), 3)
        self.assertEqual(self.api._failure_list.get(second_tid), 0)
        self.assertNotEqual(first_tid, second_tid)
        self.assertTrue(await second)
        self.assert_clean()

    async def test_cancellation_preserves_other_requests_result(self):
        first, _ = await self.start_request()
        second, second_tid = await self.start_request(host=OTHER_HOST)
        await self.receive(packet(second_tid), OTHER_HOST)
        first.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await first
        self.assertEqual(self.api._opc_counts.get(second_tid), 3)
        self.assertEqual(self.api._failure_list.get(second_tid), 0)
        self.assertTrue(await second)
        self.assert_clean()

    async def test_cancelled_receiver_cannot_consume_reused_tid(self):
        entered = asyncio.Event()
        release = asyncio.Event()

        async def block(_is_push):
            entered.set()
            await release.wait()

        self.api.register_async_receive_callbacks(HOST, *AIRCON, block)
        first, tid = await self.start_request()
        receiver = await self.track(self.receive(packet(tid)))
        await asyncio.wait_for(entered.wait(), 1)
        first.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await first
        self.assert_clean()
        self.api.unregister_async_receive_callbacks(HOST, *AIRCON)
        self.api._next_tx_tid = tid - 1
        second, second_tid = await self.start_request()
        self.assertEqual(tid, second_tid)
        await self.receive(packet(second_tid))
        release.set()
        await receiver
        self.assertEqual(self.api._opc_counts.get(second_tid), 3)
        self.assertEqual(self.api._failure_list.get(second_tid), 0)
        self.assertTrue(await second)
        self.assert_clean()

    async def test_tid_exhaustion_returns_queue_busy_without_overwrite(self):
        self.api._opc_counts.update(dict.fromkeys(range(1, 0x10000), 3))
        result = await self.api.echonetMessage(
            HOST, *AIRCON, GET, [{"EPC": 0xA4}]
        )
        self.assertIsNone(result)
        self.assertTrue(self.sent.empty())
        self.assertEqual(len(self.api._opc_counts), 0xFFFF)
        self.assertEqual(self.api._message_list, {})
        self.assertEqual(self.api._waiting[HOST], 0)
        self.api._opc_counts.clear()
        self.assert_clean()

    async def test_inf_request_responses_preserve_existing_behavior(self):
        for esv, edt, expected in ((INF, b"\x41", True), (INF_SNA, b"", False)):
            with self.subTest(esv=esv):
                task, tid = await self.start_request(esv=INFREQ, opc=[{"EPC": 0xA4}])
                await self.receive(packet(tid, esv=esv, properties=[(0xA4, edt)]))
                self.assertEqual(await task, expected)
                self.assert_clean()

    async def test_infc_res_preserves_existing_zero_opc_limitation(self):
        task, tid = await self.start_request(
            esv=INFC, opc=[{"EPC": 0xA4, "PDC": 1, "EDT": 0x41}]
        )
        await self.receive(packet(tid, esv=INFC_RES, properties=[]))
        self.assertNotIn(tid, self.api._message_list)
        self.assertEqual(self.api._opc_counts[tid], 0)
        with self.assertRaises(EchonetMaxOpcError) as error:
            await task
        self.assertEqual(error.exception.args, (0,))
        self.assert_clean()

    async def test_setget_res_preserves_existing_second_opc_limitation(self):
        for esv in (SETGET_RES, SETGET_SNA):
            with self.subTest(esv=esv):
                task, tid = await self.start_request(
                    esv=SETGET, opc=[{"EPC": 0x80, "PDC": 1, "EDT": 0x30}]
                )
                # The legacy decoder reads only the first (SET) OPC block.
                data = packet(tid, esv=esv, properties=[(0x80, b"")])
                data += b"\x01\xa4\x01\x41"  # GET OPC=1, EPC=A4, EDT=41
                await self.receive(data)
                self.assertEqual(self.api._opc_counts[tid], 1)
                self.assertTrue(await task)
                state = self.api.state[HOST]["instances"][1][0x30][1]
                self.assertNotIn(0x80, state)
                self.assertNotIn(0xA4, state)
                self.assert_clean()
