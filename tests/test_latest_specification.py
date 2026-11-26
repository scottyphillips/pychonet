import asyncio
import json
import unittest
from importlib.resources import files

from pychonet import (
    ActivityAmountSensor,
    CigaretteSensor,
    DistributedGeneratorElectricEnergyMeter,
    ECHONETAPIClient,
    EchonetInstance,
    ElectricHeater,
    ElectricStorageHeater,
    EmergencyButton,
    Factory,
    FanHeater,
    FireSensor,
    FirstAidSensor,
    FrequencyRegulation,
    MicromotionSensor,
    OdorSensor,
    RiceCooker,
    VisitorSensor,
)
from pychonet.lib.const import (
    ENL_BROADCAST_ADDRESS,
    ENL_GETMAP,
    ENL_MANUFACTURER,
    ENL_MULTICAST_ADDRESS,
    ENL_PORT,
    ENL_PRODUCT_CODE,
    ENL_SETMAP,
    ENL_STATMAP,
    ENL_UID,
    GET,
    GETRES,
    INF,
    INFREQ,
    INSTANCE_LIST,
    INSTANCE_LIST_NOTIFICATION,
    SETC,
    SETC_SND,
    SETRES,
)
from pychonet.echonetapiclient import EchonetMaxOpcError
from pychonet.lib.epc import EPC_CODE
from pychonet.lib.epc_functions import EPC_SUPER_FUNCTIONS
from pychonet.lib.functions import decodeEchonetMsg


HOST = "192.0.2.10"
OTHER_HOST = "192.0.2.11"


def response(request, service, properties):
    entries = properties.items() if isinstance(properties, dict) else properties
    opcs = b"".join(
        bytes((epc, len(edt))) + edt for epc, edt in entries
    )
    return request[:4] + request[7:10] + request[4:7] + bytes(
        (service, len(properties))
    ) + opcs


class SimulatedUDP:
    def __init__(self, reply):
        self.reply = reply
        self.sent = []
        self.pending = []

    def subscribe(self, receiver):
        self.receive = receiver

    def send(self, payload, address):
        request = bytes(payload)
        self.sent.append((request, address))
        for packet, host in self.reply(request, address):
            self.pending.append(
                asyncio.create_task(self.receive(packet, (host, ENL_PORT)))
            )

    async def finish(self):
        await asyncio.gather(*self.pending)


def simulated_client(reply, discover_callback=None):
    udp = SimulatedUDP(reply)
    api = ECHONETAPIClient(udp)
    api.configure(
        message_timeout=2,
        logger=lambda _message: None,
        discover_callback=discover_callback,
    )
    return api, udp


def simulated_device(class_code, properties, settable=(), *, group=0x02):
    def reply(request, address):
        message = decodeEchonetMsg(request)
        epcs = [opc["EPC"] for opc in message["OPC"]]
        if message["ESV"] == SETC:
            return [(response(request, SETRES, dict.fromkeys(epcs, b"")), address[0])]
        result = {epc: properties[epc] for epc in epcs}
        return [(response(request, GETRES, result), address[0])]

    api, udp = simulated_client(reply)
    api.register_instance(HOST, group, class_code, 1, [], list(settable), list(properties))
    return Factory(HOST, api, group, class_code), udp


class TestIPv4Discovery(unittest.IsolatedAsyncioTestCase):
    async def test_broadcast_discovery_pairs_with_multicast(self):
        discovered = []

        async def discover_callback(host):
            discovered.append(host)

        def reply(request, address):
            edt = bytes.fromhex("02 028e01 02a701")
            packet = response(request, GETRES, {INSTANCE_LIST: edt})
            if address[0] == ENL_MULTICAST_ADDRESS:
                return [(request, "192.0.2.1"), (packet, HOST)]
            return [(packet, HOST), (packet, OTHER_HOST)]

        api, udp = simulated_client(reply, discover_callback)
        self.assertTrue(await api.discover(broadcast=True))
        await udp.finish()

        request, multicast = udp.sent[0]
        self.assertEqual(udp.sent, [
            (request, (ENL_MULTICAST_ADDRESS, ENL_PORT)),
            (request, (ENL_BROADCAST_ADDRESS, ENL_PORT)),
        ])
        message = decodeEchonetMsg(request)
        self.assertEqual(message["ESV"], GET)
        self.assertEqual(message["OPC"], [{"EPC": INSTANCE_LIST, "PDC": 0, "EDT": b""}])
        self.assertCountEqual(discovered, [HOST, OTHER_HOST])

    async def test_multicast_is_the_default_and_broadcast_requires_it(self):
        api, udp = simulated_client(lambda _request, _address: [])
        api.configure(message_timeout=1)
        multicast = ENL_MULTICAST_ADDRESS.encode().decode()
        self.assertFalse(await api.discover(multicast))
        with self.assertRaisesRegex(ValueError, "multicast node discovery"):
            await api.discover(HOST, broadcast=True)

        (request, address), = udp.sent
        self.assertEqual(address, (multicast, ENL_PORT))
        self.assertEqual([opc["EPC"] for opc in decodeEchonetMsg(request)["OPC"]],
                         [INSTANCE_LIST])

    async def test_broadcast_address_also_multicasts_and_records_the_peer(self):
        def reply(request, address):
            if address[0] == ENL_BROADCAST_ADDRESS:
                return [(response(request, GETRES, {INSTANCE_LIST: b"\x01\x01\x5a\x02"}), HOST)]
            return []

        api, udp = simulated_client(reply)
        with self.assertRaisesRegex(ValueError, "discover"):
            await api.echonetMessage(
                ENL_BROADCAST_ADDRESS, 0x01, 0x5A, 1, SETC,
                [{"EPC": 0xA0, "EDT": b"\x34"}],
            )
        self.assertTrue(await api.discover(ENL_BROADCAST_ADDRESS))
        await udp.finish()
        self.assertEqual(
            [address for _, address in udp.sent],
            [(ENL_MULTICAST_ADDRESS, ENL_PORT), (ENL_BROADCAST_ADDRESS, ENL_PORT)],
        )
        self.assertIn(2, api.state[HOST]["instances"][1][0x5A])
        self.assertNotIn(ENL_MULTICAST_ADDRESS, api.state)

    async def test_late_discovery_responses_are_delivered_once_per_host(self):
        discovered = []

        async def on_discovered(host):
            discovered.append(host)

        def reply(request, address):
            if address[0] == ENL_MULTICAST_ADDRESS:
                return [(response(request, GETRES, {INSTANCE_LIST: b"\x01\x01\x5a\x02"}), HOST)]
            return []

        api, udp = simulated_client(reply, on_discovered)
        api.configure(message_timeout=10)
        self.assertTrue(await api.discover(broadcast=True))
        await udp.finish()

        request = udp.sent[0][0]
        delayed = response(request, GETRES, {INSTANCE_LIST: b"\x01\x01\x5a\x02"})
        await api.echonetMessageReceived(delayed, (HOST, ENL_PORT))
        await api.echonetMessageReceived(delayed, (OTHER_HOST, ENL_PORT))
        self.assertEqual(discovered, [HOST, OTHER_HOST])
        self.assertIn(OTHER_HOST, api.state)

    async def test_large_node_merges_partial_d6_and_all_d5_lists(self):
        first_entries = b"".join(bytes((0x01, 0x5A, index)) for index in range(1, 85))

        def reply(request, _address):
            if decodeEchonetMsg(request)["ESV"] == INFREQ:
                return [(response(request, INF, [
                    (INSTANCE_LIST_NOTIFICATION, bytes((84,)) + first_entries),
                    (INSTANCE_LIST_NOTIFICATION, b"\x01\x01\x5a\x55"),
                ]), HOST)]
            return [(response(request, GETRES, {
                INSTANCE_LIST: bytes((85,)) + first_entries,
            }), HOST)]

        for destination in (HOST, ENL_MULTICAST_ADDRESS):
            with self.subTest(destination=destination):
                api, udp = simulated_client(reply)
                self.assertTrue(await api.discover(destination))
                await udp.finish()
                self.assertEqual(api.state[HOST]["instance_count"], 85)
                self.assertEqual(set(api.state[HOST]["instances"][1][0x5A]), set(range(1, 86)))
                followup = decodeEchonetMsg(udp.sent[1][0])
                self.assertEqual(followup["ESV"], INFREQ)
                self.assertEqual(followup["OPC"][0]["EPC"], INSTANCE_LIST_NOTIFICATION)


class TestPropertyTransactions(unittest.IsolatedAsyncioTestCase):
    async def test_set_ignores_other_hosts_and_notifications_with_the_same_tid(self):
        send_ack = False

        def reply(request, address):
            notices = [
                (response(request, INF, {0xA0: b"\x31"}), address[0]),
                (response(request, SETRES, {0xA0: b""}), OTHER_HOST),
            ]
            if send_ack:
                notices.append((response(request, SETRES, {0xA0: b""}), address[0]))
            return notices

        api, udp = simulated_client(reply)
        for host in (HOST, OTHER_HOST):
            api.register_instance(host, 1, 0x5A, 1, [0xA0], [0xA0], [0xA0])
        device = Factory(HOST, api, 1, 0x5A)
        self.assertFalse(await device.setMessage(0xA0, b"\x34"))
        self.assertEqual(await device.update(0xA0, no_request=True), "31")
        self.assertIsNone(await Factory(OTHER_HOST, api, 1, 0x5A).update(0xA0, no_request=True))

        send_ack = True
        self.assertTrue(await device.setMessage(0xA0, b"\x34"))
        self.assertEqual(await device.update(0xA0, no_request=True), "34")
        await udp.finish()

    async def test_set_batch_keeps_confirmed_cache_and_rejects_partial_success(self):
        def reply(request, address):
            return [(response(request, SETC_SND, {0xA0: b"", 0xBF: b"\x41"}), address[0])]

        api, udp = simulated_client(reply)
        api.register_instance(HOST, 1, 0x5A, 1, [], [0xA0, 0xBF], [0xA0, 0xBF])
        device = Factory(HOST, api, 1, 0x5A)
        self.assertFalse(await device.setMessages([
            {"EPC": 0xA0, "EDT": b"\x34"},
            {"EPC": 0xBF, "EDT": b"\x41"},
        ]))
        self.assertEqual(await device.update([0xA0, 0xBF], no_request=True),
                         {0xA0: "34", 0xBF: None})
        await udp.finish()

    async def test_invalid_batch_and_read_only_map_do_not_send_writes(self):
        api, udp = simulated_client(lambda _frame, _address: [])
        api.register_instance(HOST, 1, 0x5A, 1, [], [0xA0], [0xA0, 0xC2])
        api.register_instance(HOST, 1, 0x5A, 2, [], [], [0xA0])
        writable = Factory(HOST, api, 1, 0x5A, 1)
        read_only = Factory(HOST, api, 1, 0x5A, 2)

        self.assertFalse(await writable.setMessages([
            {"EPC": 0xA0, "EDT": b"\x34"},
            {"EPC": 0xC2, "EDT": b"\x00\x10"},
        ]))
        self.assertFalse(await read_only.setMessage(0xA0, b"\x34"))
        self.assertEqual(udp.sent, [])

    async def test_short_get_retains_limit_hint_and_confirmed_value(self):
        def reply(request, address):
            return [(response(request, GETRES, {0xA0: b"\x32"}), address[0])]

        api, udp = simulated_client(reply)
        api.register_instance(HOST, 1, 0x5A, 1, [], [], [0xA0, 0xC2])
        device = Factory(HOST, api, 1, 0x5A)
        with self.assertRaises(EchonetMaxOpcError):
            await device.update([0xA0, 0xC2])
        self.assertEqual(await device.update([0xA0, 0xC2], no_request=True),
                         {0xA0: "32", 0xC2: None})
        await udp.finish()


class TestDeviceAppendix(unittest.IsolatedAsyncioTestCase):
    async def test_distributed_generator_reads_latest_energy_properties(self):
        count = bytes.fromhex("00003039")
        no_data = bytes.fromhex("fffffffe")
        history = b"\x00\x01" + count + no_data * 47
        timestamp = bytes.fromhex("07ea 0b 1a 0c 1e 00")
        device, udp = simulated_device(0x8E, {
            0xA0: count,
            0xA1: history,
            0xA2: timestamp + count,
            0xB4: no_data,
            0xB6: b"\xff\xff" + no_data * 48,
            0xB7: timestamp + no_data,
            0xD4: b"\x02",
            0xD7: b"\x03",
            0xD8: b"\xff",
            0xD9: b"\x07",
            0xE0: count,
        })
        self.assertIsInstance(device, DistributedGeneratorElectricEnergyMeter)
        result = await device.update()
        await udp.finish()

        self.assertEqual(result, {
            0xA0: 12345,
            0xA1: {"day": 1, "readings_48_half_hourly": [12345] + [None] * 47},
            0xA2: {"time": "2026-11-26T12:30:00", "electric_energy": 12345},
            0xB4: None,
            0xB6: {"day": None, "readings_48_half_hourly": [None] * 48},
            0xB7: {"time": "2026-11-26T12:30:00", "electric_energy": None},
            0xD4: 0.01,
            0xD7: "n3",
            0xD8: "other",
            0xD9: "n7",
            0xE0: 12345,
        })
        new_epcs = set(range(0xA0, 0xAC)) | set(range(0xB0, 0xB8)) | {0xD7, 0xD8, 0xD9}
        self.assertTrue(new_epcs <= EPC_CODE[0x02][0x8E].keys())
        self.assertTrue(new_epcs <= device.EPC_FUNCTIONS.keys())

    async def test_frequency_regulation_decodes_history_and_settings(self):
        timestamp = bytes.fromhex("07ea 0b 1a 0c 1e")
        power = bytes.fromhex("0000002a fffffff6 7ffffffe 80000000 7fffffff")
        device, udp = simulated_device(0xA7, {
            0x98: timestamp[:4],
            0xC8: b"\x30",
            0xC9: timestamp[4:] + b"\x05",
            0xCA: b"\x01",
            0xCB: b"\x00\x01\x00\x0a" + timestamp * 2,
            0xCC: b"\x31",
            0xCD: timestamp,
            0xCE: timestamp + power + b"\x00" * (55 * 4),
            0xD0: b"\x07\xd0",
            0xD1: b"\x02\x79\x01",
            0xD5: b"\x01\x03\x80\x02",
        }, settable=(0xCD,))
        self.assertIsInstance(device, FrequencyRegulation)
        result = await device.update()
        await udp.finish()

        self.assertEqual(result, {
            0x98: "2026:11:26",
            0xC8: "on",
            0xC9: "12:30:05",
            0xCA: "time synchronization successful",
            0xCB: {
                "stored_entries": 1,
                "capacity": 10,
                "oldest": "2026-11-26T12:30",
                "latest": "2026-11-26T12:30",
            },
            0xCC: "disabled",
            0xCD: "2026-11-26T12:30",
            0xCE: {
                "time": "2026-11-26T12:30",
                "readings_w": [42, -10, None, None, None] + [0] * 55,
            },
            0xD0: 20_000,
            0xD1: "027901",
            0xD5: {"available_modes": 0x0103, "active_modes": 0x8002},
        })

        new_timestamp = bytes.fromhex("07ea 0b 19 01 02")
        self.assertTrue(await device.setMessage(0xCD, int.from_bytes(new_timestamp, "big"), 6))
        await udp.finish()
        self.assertEqual(await device.update(0xCD, no_request=True), "2026-11-25T01:02")

    def test_fault_description_recognizes_combined_codes(self):
        decode = EPC_SUPER_FUNCTIONS[0x89]
        self.assertEqual(decode(b"\x03\xe9")["fault classification"], "Repair location unknown")
        self.assertEqual(
            decode(b"\x03\xff")["fault classification"],
            "Recovery method or fault location unknown",
        )
        self.assertEqual(
            decode(b"\x10\x07"),
            {"fault classification": "Recover operation no required", "error code": 0x10},
        )


class TestExistingDeviceCoverage(unittest.IsolatedAsyncioTestCase):
    def test_factory_routes_existing_classes_to_the_requested_eoj(self):
        classes = {
            0x0003: EmergencyButton,
            0x0004: FirstAidSensor,
            0x0008: VisitorSensor,
            0x0019: FireSensor,
            0x001A: CigaretteSensor,
            0x0020: OdorSensor,
            0x0026: MicromotionSensor,
            0x002A: ActivityAmountSensor,
            0x0142: ElectricHeater,
            0x0143: FanHeater,
            0x0155: ElectricStorageHeater,
            0x03BB: RiceCooker,
        }
        api, _udp = simulated_client(lambda _request, _address: [])
        for eoj, device_class in classes.items():
            with self.subTest(eoj=hex(eoj)):
                group, code = eoj >> 8, eoj & 0xFF
                api.register_instance(HOST, group, code, 3, [], [], [])
                instance = Factory(HOST, api, group, code, 3)
                self.assertIs(type(instance), device_class)
                self.assertEqual(
                    (instance._eojgc, instance._eojcc, instance._eojci),
                    (group, code, 3),
                )

    def test_property_catalog_includes_bundled_mra_and_appendix_entries(self):
        devices = files("pychonet").joinpath("mraData").joinpath("devices")
        for source in devices.iterdir():
            if not source.name.endswith(".json"):
                continue
            contents = json.loads(source.read_text(encoding="utf-8"))
            eoj = int(contents["eoj"], 16)
            eoj = 0x000D if eoj == 0x00D0 else eoj
            epcs = {int(item["epc"], 16) for item in contents["elProperties"]}
            with self.subTest(eoj=hex(eoj)):
                self.assertTrue(epcs <= EPC_CODE[eoj >> 8][eoj & 0xFF].keys())
        self.assertNotIn(0xD0, EPC_CODE[0x00])
        self.assertEqual(EPC_CODE[0x01][0x5A][0xC2], "Measured supply air temperature")
        self.assertEqual(EPC_CODE[0x03][0xD5][0xEF], "Used water volume")
        self.assertIn(0xE2, EPC_CODE[0x05][0xFB])
        self.assertTrue({0xC0, 0xC1, 0xC2, 0xC3} <= EPC_CODE[0x00][0x05].keys())

    async def test_generic_device_discovery_and_raw_property_round_trip(self):
        node_properties = {
            INSTANCE_LIST: bytes.fromhex("01 015a02"),
            ENL_MANUFACTURER: b"\x00\x00\x08",
            ENL_PRODUCT_CODE: b"Range hood",
            ENL_UID: b"\xfe\x00\x00\x08" + b"\x01" * 13,
        }
        device_properties = {
            ENL_STATMAP: b"\x00",
            ENL_SETMAP: b"\x02\xa0\xfa",
            ENL_GETMAP: b"\x05\x80\x8c\xa0\xc2\xfa",
            0x80: b"\x30",
            ENL_PRODUCT_CODE: b"Range hood\x00",
            0xA0: b"\x33",
            0xC2: b"\x00\xe6",
            0xFA: b"\x00\x20",
        }

        def reply(request, address):
            message = decodeEchonetMsg(request)
            if message["ESV"] == SETC:
                result = {}
                for item in message["OPC"]:
                    device_properties[item["EPC"]] = item["EDT"]
                    result[item["EPC"]] = b""
                return [(response(request, SETRES, result), address[0])]
            available = node_properties if message["DEOJGC"] == 0x0E else device_properties
            result = {item["EPC"]: available[item["EPC"]] for item in message["OPC"]}
            return [(response(request, GETRES, result), address[0])]

        api, udp = simulated_client(reply)
        self.assertTrue(await api.discover(HOST))
        device = Factory(HOST, api, 0x01, 0x5A, 0x02)
        self.assertIs(type(device), EchonetInstance)
        self.assertTrue(await device.getAllPropertyMaps())
        self.assertNotIn(0xFA, EPC_CODE[0x01][0x5A])
        self.assertEqual(await device.update(), {
            0x80: "on",
            0x8C: "Range hood",
            0xA0: "33",
            0xC2: "00e6",
            0xFA: "0020",
        })

        with self.assertRaisesRegex(ValueError, "PDC must match"):
            await device.setMessage(0xFA, b"\x00\x21", 1)
        self.assertTrue(await device.setMessage(0xFA, b"\x00\x22"))
        self.assertEqual(await device.update(0xFA, no_request=True), "0022")
        self.assertTrue(await device.setMessages([
            {"EPC": 0xFA, "EDT": b"\x00\x23"},
            {"EPC": 0xA0, "EDT": 0x34, "PDC": 1},
        ]))
        self.assertEqual(await device.getMessage(0xFA), b"\x00\x23")
        self.assertEqual(await device.update([0xA0, 0xFA], no_request=True),
                         {0xA0: "34", 0xFA: "0023"})
        await udp.finish()

    async def test_existing_scalar_decoders_accept_their_declared_arguments(self):
        charger, charger_udp = simulated_device(0xA1, {0xC5: b"\x00\x00\x32\xc8"})
        meter, meter_udp = simulated_device(0x88, {0xE1: b"\xff"})
        self.assertEqual(await charger.update(0xC5), 13000)
        self.assertIsNone(await meter.update(0xE1))
        await charger_udp.finish()
        await meter_udp.finish()

    async def test_storage_heater_reads_signed_temperatures_and_status(self):
        device, udp = simulated_device(0x55, {
            0xBB: b"\xfb", 0xBE: b"\x7e", 0xC2: b"\xff\xf6",
            0xA1: b"\x32", 0xC0: b"\x30", 0xC7: b"\x31",
        }, group=0x01)
        self.assertEqual(await device.update(), {
            0xBB: -5, 0xBE: None, 0xC2: -10,
            0xA1: "weak", 0xC0: "on", 0xC7: "Without fan",
        })
        await udp.finish()

    async def test_rice_cooker_reports_cooking_and_removal_states(self):
        device, udp = simulated_device(0xBB, {
            0xB0: b"\x42", 0xB1: b"\x43", 0xE5: b"\x41", 0xE6: b"\x42",
        }, group=0x03)
        self.assertEqual(await device.update(), {
            0xB0: "closed", 0xB1: "Rice cooking in progress",
            0xE5: "Removed", 0xE6: "Installed",
        })
        await udp.finish()

    async def test_micromotion_writes_two_byte_sampling_properties(self):
        device, udp = simulated_device(0x26, {}, (0xB2, 0xBC, 0xBD), group=0x00)
        for epc, setter in (
            (0xB2, device.setDetectionCounter),
            (0xBC, device.setSamplingCount),
            (0xBD, device.setSamplingCycle),
        ):
            self.assertTrue(await setter(1000))
            command = decodeEchonetMsg(udp.sent[-1][0])
            self.assertEqual(command["OPC"], [{"EPC": epc, "PDC": 2, "EDT": b"\x03\xe8"}])
        await udp.finish()

    async def test_activity_sensor_reads_standard_activity_level_2(self):
        device, udp = simulated_device(0x2A, {0xE2: b"\x34"}, group=0x00)
        self.assertEqual(await device.getActivityStatus(), b"\x34")
        self.assertEqual(await device.getMeasuredActivityAmount(), b"\x34")
        self.assertEqual(await device.update(0xE2), "level-4")
        self.assertTrue(all(decodeEchonetMsg(request)["OPC"][0]["EPC"] == 0xE2
                            for request, _ in udp.sent))
        await udp.finish()
