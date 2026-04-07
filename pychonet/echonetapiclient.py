import asyncio
import time
from typing import Callable

from pychonet.lib.const import (
    ENL_GETMAP,
    ENL_MANUFACTURER,
    ENL_MULTICAST_ADDRESS,
    ENL_PORT,
    ENL_PRODUCT_CODE,
    ENL_SETMAP,
    ENL_STATMAP,
    ENL_UID,
    GET,
    GET_SNA,
    GETRES,
    INF,
    INF_SNA,
    INFC,
    INSTANCE_LIST,
    MESSAGE_TIMEOUT,
    SETC,
    SETC_SND,
    SETI,
    SETRES,
)
from pychonet.lib.epc_functions import EPC_SUPER_FUNCTIONS
from pychonet.lib.functions import TIDError, buildEchonetMsg, decodeEchonetMsg
from pychonet.lib.udpserver import UDPServer


class ECHONETAPIClient:
    """
    Async ECHONET Lite API client.

    This class manages:
      - Sending and receiving ECHONET Lite UDP packets
      - Device discovery (multicast and unicast)
      - Instance and property state tracking
      - Callback dispatch for updates and received packets

    Discovery behaviour
    -------------------
    Two discovery mechanisms are implemented:

    1. Active discovery
       A multicast Node Profile request (EPC=INSTANCE_LIST) is sent to
       224.0.23.0:3610. Multiple devices may respond within a short time window.
       Responses are collected during `_discovery_window`.

    2. Passive discovery
       When a valid ECHONET Lite packet is received from an unknown host,
       the host is temporarily added to `_state` and a background discovery
       probe is scheduled via `_discover_callback`.

       To avoid repeated discovery storms, unknown host probing is suppressed
       using `_unknown_discovery_in_progress` and `_unknown_discovery_last_failed`.

    Notes
    -----
    - The first packet from an unknown device is still processed so discovery
      data (e.g. INSTANCE_LIST, UID, manufacturer) can be extracted immediately.
    - Discovery callbacks are scheduled using `asyncio.create_task()` so that
      packet reception is not blocked.
    """

    def __init__(self, server: UDPServer):
        self._server = server
        self._logger: Callable = print
        self._server.subscribe(self.echonetMessageReceived)
        self._state = {}
        self._next_tx_tid = 0x0000
        self._message_list = {}
        self._failure_list = {}
        self._opc_counts = {}
        self._message_timeout = MESSAGE_TIMEOUT
        self._debug_flag = False
        self._update_callbacks = {}
        self._receive_callbacks = {}
        self._discover_callback: Callable | None = None
        self._waiting = {}
        # Discovery-specific response collection
        #
        # Multicast discovery can generate multiple responses from different devices.
        # Instead of finishing the transaction when the first response arrives,
        # responses are collected during `_discovery_window` seconds.
        #
        # `_discovery_tids` tracks TIDs currently used for discovery transactions.
        self._discovery_tids = set()
        self._discovery_window = 2.0
        # Unknown host discovery control
        #
        # When a packet arrives from a host that is not yet known in `_state`,
        # a background discovery probe will be scheduled.  These structures
        # prevent repeated discovery attempts when devices send frequent
        # notifications (INF/INFC).
        #
        # _unknown_discovery_in_progress
        #     Hosts currently undergoing discovery.
        #
        # _unknown_discovery_last_failed
        #     Timestamp of the last failed discovery attempt.
        #
        # _unknown_discovery_suppress_seconds
        #     Minimum delay before retrying discovery for the same host.
        #
        # _unknown_discovery_last_scheduled
        #     Timestamp of the last time discovery was scheduled for a host.
        #
        # _unknown_discovery_cooldown_seconds
        #     Minimum delay before scheduling discovery again for the same host,
        #     regardless of success or failure.
        self._unknown_discovery_in_progress = set()
        self._unknown_discovery_last_failed = {}
        self._unknown_discovery_suppress_seconds = 30.0
        self._unknown_discovery_last_scheduled = {}
        self._unknown_discovery_cooldown_seconds = 10.0

    async def echonetMessageReceived(self, raw_data, addr):
        updated = False
        host = addr[0]
        is_discovery = False

        if host in self._server._multicast_ips:
            return

        if self._debug_flag:
            self._logger(
                f"ECHONETLite Message Received from {host} - Raw data is {raw_data}"
            )

        try:
            processed_data = decodeEchonetMsg(raw_data)
        except Exception as err:
            if self._debug_flag:
                self._logger(
                    f"Failed to decode ECHONETLite packet from {host}: {err}, raw={raw_data}"
                )
            return

        if self._debug_flag:
            self._logger(
                f"ECHONETLite Message Received from {host} - Processed data is {processed_data}"
            )

        tid = processed_data["TID"]
        tid_data = self._message_list.get(tid)

        if self._debug_flag:
            self._logger(
                f"ECHONETLite Message Received from {host} - tid_data is {tid_data}"
            )

        isPush = tid_data is None
        seojgc = processed_data["SEOJGC"]
        seojcc = processed_data["SEOJCC"]
        seojci = processed_data["SEOJCI"]
        esv = processed_data["ESV"]

        # Passive discovery:
        #
        # If a packet arrives from a host that is not known yet, create a
        # temporary state entry and schedule a background discovery probe.
        #
        # The current packet is still processed so that discovery information
        # (e.g. INSTANCE_LIST) contained in the packet can be extracted
        # immediately.
        if self._state.get(host) is None:
            self._logger(f"Unknown ECHONETLite node has been identified - {host}")

            # Create temporary host state so the current packet can still be processed
            self._state[host] = {"instances": {}, "available": True}

            # If this packet is already a Node Profile response, discovery data
            # will be processed from this packet, so skip active discovery.
            if seojgc == 0x0E and seojcc == 0xF0:
                pass
            elif self._should_schedule_unknown_discovery(host):
                self._unknown_discovery_last_scheduled[host] = time.monotonic()
                self._unknown_discovery_in_progress.add(host)
                asyncio.create_task(self._run_unknown_host_discovery(host))

        key = f"{host}-{seojgc}-{seojcc}-{seojci}"
        esv_set = esv in [SETRES, SETC_SND]
        esv_get = esv in [GETRES, GET_SNA, INF, INF_SNA, INFC]
        if not isPush:
            self._failure_list[tid] = 0
            self._opc_counts[tid] = len(processed_data["OPC"])
        # handle discovery message response
        for opc in processed_data["OPC"]:
            epc = opc["EPC"]
            if seojgc == 0x0E and seojcc == 0xF0:  # Node Profile Class Response
                if epc in [
                    INSTANCE_LIST,
                    ENL_MANUFACTURER,
                    ENL_PRODUCT_CODE,
                    ENL_UID,
                ]:  # process discovery data
                    is_discovery = True
                    await self.process_discovery_data(host, opc)
                else:
                    # @todo handling others
                    """
                    Ex. 0x05: Instance list notification
                    A property to announce the configuration of instances to be disclosed to the network at startup.
                    This property also announces instances held at the self-node each time the configuration of
                    instances disclosed to the network is changed during system operation, such as instance
                    addition or deletion.
                    """
                    """
                    It is desirable to dynamically add and delete entities when there is an increase
                    or decrease in the number of instances within a device already configured with HA,
                    but that will be an issue for the future.
                    """
                    continue
            elif seojgc == 0x0F:  # User definition class group
                if self._debug_flag:
                    self._logger(
                        f"Packet received from {host} for user definition class group 0x0F"
                    )
                    self._logger(f"Full packet details are {processed_data}")
                    self._logger("ignoring packet but please notify devs on Github.")
            else:  # process each EPC in order
                self._ensure_instance_state(host, seojgc, seojcc, seojci)
                if epc == ENL_SETMAP or epc == ENL_GETMAP or epc == ENL_STATMAP:
                    map = EPC_SUPER_FUNCTIONS[epc](opc["EDT"])
                    self._state[host]["instances"][seojgc][seojcc][seojci][epc] = map
                elif epc in (ENL_UID, ENL_MANUFACTURER, ENL_PRODUCT_CODE):
                    try:
                        self._state[host]["instances"][seojgc][seojcc][seojci][epc] = (
                            EPC_SUPER_FUNCTIONS[epc](opc["EDT"])
                        )
                    except KeyError as e:
                        if self._debug_flag:
                            self._logger(
                                f"ECHONET _state _key error {e} of {host} this packet contains the following data: {processed_data}"
                            )
                        continue
                        # raise Exception(
                        #     f"ECHONET Packet contains the following data: {processed_data}"
                        # )
                else:
                    if esv_set:
                        if opc["PDC"] > 0 or isPush:
                            if not isPush:
                                self._failure_list[tid] += 1
                            continue
                        if tid_data.get(epc) is None:
                            self._failure_list[tid] += 1
                            if self._debug_flag:
                                self._logger(
                                    f"EDT is not set in send data for EPC '{epc}' - process each EPC"
                                )
                            continue
                        else:
                            # set request data
                            opc["EDT"] = tid_data[epc]
                    elif esv_get:
                        if opc["PDC"] == 0:
                            if not isPush:
                                self._failure_list[tid] += 1
                            continue
                    else:
                        # @todo more esv support
                        continue

                    if (
                        epc
                        not in self._state[host]["instances"][seojgc][seojcc][seojci]
                        or self._state[host]["instances"][seojgc][seojcc][seojci][epc]
                        != opc["EDT"]
                    ):
                        updated = True
                    self._state[host]["instances"][seojgc][seojcc][seojci][epc] = opc[
                        "EDT"
                    ]

        # Markup "discovered"
        if is_discovery and len(self._state[host]["instances"]):
            if self._state[host].get("uid") is None:
                self._state[host]["uid"] = EPC_SUPER_FUNCTIONS[ENL_UID](b"", host)
            if self._state[host].get("manufacturer") is None:
                self._state[host]["manufacturer"] = EPC_SUPER_FUNCTIONS[
                    ENL_MANUFACTURER
                ](0xFFFFFF.to_bytes(3, "big"))
            self._state[host]["discovered"] = True

        # Markup "available"
        _to_available = False
        if host in self._state:
            if not self._state[host].get("available"):
                _to_available = True
                self._state[host]["available"] = True

        if _to_available:
            # Call update callback functions
            # key is f"{host}-{deojgc}-{deojcc}-{deojci}"
            for _key in self._update_callbacks:
                if _key.startswith(host):
                    for update_func in self._update_callbacks[_key]:
                        await update_func(False)

            # Call receive callback functions
            for _key in self._receive_callbacks:
                if _key.startswith(host):
                    for receive_func in self._receive_callbacks[_key]:
                        await receive_func(False)

        else:
            # Call update callback functions
            if updated and key in self._update_callbacks:
                for update_func in self._update_callbacks[key]:
                    await update_func(isPush)

            # Call receive callback functions
            if key in self._receive_callbacks:
                for receive_func in self._receive_callbacks[key]:
                    await receive_func(isPush)

        # For multicast discovery, keep the TID alive until the discovery
        # collection window ends so multiple responders can be gathered.
        if tid in self._discovery_tids:
            return

        # if we get duplicate packets that have already been processed then
        # dont worry about the message list, but still process them regardless.
        if tid_data is not None:
            del self._message_list[tid]

    async def discover(self, host=ENL_MULTICAST_ADDRESS):
        """
        Perform device discovery.

        If `host` is the multicast address, a network-wide discovery is performed
        by requesting INSTANCE_LIST from all devices.

        If `host` is a specific IP address, a unicast discovery probe is sent to
        obtain manufacturer, product code, UID, and instance list.

        Returns
        -------
        bool
            True if at least one device (or the specified host) responded.
        """
        if host == ENL_MULTICAST_ADDRESS:
            opc = [{"EPC": INSTANCE_LIST}]
        else:
            opc = [
                {"EPC": ENL_MANUFACTURER},
                {"EPC": ENL_PRODUCT_CODE},
                {"EPC": ENL_UID},
                {"EPC": INSTANCE_LIST},
            ]
        return await self.echonetMessage(host, 0x0E, 0xF0, 0x01, GET, opc)

    async def echonetMessage(self, host, deojgc, deojcc, deojci, esv, opc):
        no_res = esv == SETI
        payload = None
        # Is node profile
        is_discover = deojgc == 0x0E and deojcc == 0xF0
        map_epcs = {ENL_STATMAP, ENL_GETMAP, ENL_SETMAP}
        # Check OPC Code
        try:
            if not is_discover:
                if esv == GET:
                    check_map = set(
                        self._state[host]["instances"][deojgc][deojcc][deojci].get(
                            ENL_GETMAP, []
                        )
                    )
                    check_map |= map_epcs
                elif esv == SETC:
                    check_map = set(
                        self._state[host]["instances"][deojgc][deojcc][deojci].get(
                            ENL_SETMAP, []
                        )
                    )
                else:
                    check_map = {}
                if len(check_map):
                    checked_opc = []
                    for values in opc:
                        if values.get("EPC") in check_map:
                            checked_opc.append(values)
                    opc = checked_opc
        except KeyError:
            pass

        message_array = {
            "DEOJGC": deojgc,
            "DEOJCC": deojcc,
            "DEOJCI": deojci,
            "ESV": esv,
            "OPC": opc,
        }
        if self._state.get(host) is None:
            self._state[host] = {"instances": {}, "available": True}

        # Consecutive requests to the device must wait for a response
        if self._waiting.get(host) is None:
            self._waiting[host] = 0
        if self._waiting[host] > 0:
            for x in range(0, self._message_timeout):
                # Wait up to 20(0.1*200) seconds depending on the Echonet specifications.
                await asyncio.sleep(0.1)
                if not self._waiting[host]:
                    break
            if self._waiting[host]:
                return False
        self._waiting[host] += 1

        self._next_tx_tid += 1
        tx_tid = self._next_tx_tid
        message_array["TID"] = tx_tid
        try:
            discovery_deadline: float | None = None
            discovered_before: set[str] | None = None
            try:
                payload = buildEchonetMsg(message_array)
            except TIDError:  # Quashing the rollover bug hopefully once and for all...
                self._next_tx_tid = 1
                tx_tid = self._next_tx_tid
                message_array["TID"] = tx_tid
                payload = buildEchonetMsg(message_array)

            opc_count = len(opc)
            if no_res:
                is_success = True
            else:
                is_success = False
                tid_data = {}
                for opc_data in opc:
                    if opc_data.get("EDT") is not None:
                        if isinstance(opc_data["EDT"], int):
                            tid_data[opc_data["EPC"]] = opc_data["EDT"].to_bytes(
                                opc_data["PDC"], "big"
                            )
                self._message_list[tx_tid] = tid_data

            self._server.send(payload, (host, ENL_PORT))
            if is_discover:
                self._discovery_tids.add(tx_tid)
                discovery_deadline = time.monotonic() + self._discovery_window
                if host == ENL_MULTICAST_ADDRESS:
                    discovered_before = set(self._state.keys())

            if not no_res:
                not_timeout = False
                if is_discover:
                    if discovery_deadline is None:
                        raise RuntimeError("discovery_deadline was not initialized")

                    # Collect discovery responses for a fixed time window
                    while time.monotonic() < discovery_deadline:
                        await asyncio.sleep(0.1)

                    if self._message_list.get(tx_tid) is not None:
                        del self._message_list[tx_tid]
                    self._discovery_tids.discard(tx_tid)

                    if host == ENL_MULTICAST_ADDRESS:
                        discovered_hosts = {
                            h
                            for h, state in self._state.items()
                            if h != ENL_MULTICAST_ADDRESS
                            and (
                                state.get("discovered")
                                or len(state.get("instances", {}))
                            )
                        }
                        if discovered_before is not None:
                            discovered = len(discovered_hosts - discovered_before) > 0
                        else:
                            discovered = len(discovered_hosts) > 0
                    else:
                        discovered = bool(
                            self._state.get(host, {}).get("discovered")
                            or len(self._state.get(host, {}).get("instances", {}))
                        )

                    is_success = discovered
                    not_timeout = discovered
                else:
                    for x in range(0, self._message_timeout):
                        # Wait up to 20(0.1*200) seconds depending on the Echonet specifications.
                        await asyncio.sleep(0.1)
                        # if tx_tid is not in message list then the message listener has received the message
                        if self._message_list.get(tx_tid) is None:
                            # Check OPC count in results
                            if tx_tid in self._opc_counts:
                                res_opc_count = self._opc_counts[tx_tid]
                                del self._opc_counts[tx_tid]
                                if self._debug_flag:
                                    self._logger(
                                        f"OPC count in results is {res_opc_count}/{opc_count} from IP {host}."
                                    )
                                if res_opc_count < opc_count:
                                    raise EchonetMaxOpcError(res_opc_count)

                            # transaction sucessful remove from list
                            if self._failure_list.get(tx_tid, opc_count) < opc_count:
                                is_success = True
                                if tx_tid in self._failure_list:
                                    del self._failure_list[tx_tid]
                                not_timeout = True
                            break

                if not is_success:
                    if self._message_list.get(tx_tid) is not None:
                        del self._message_list[tx_tid]
                self._discovery_tids.discard(tx_tid)
                if not is_discover and self._state[host]["available"] != not_timeout:
                    self._state[host]["available"] = not_timeout
                    # Call update callback functions
                    # key is f"{host}-{deojgc}-{deojcc}-{deojci}"
                    for key in self._update_callbacks:
                        if key.startswith(host):
                            for update_func in self._update_callbacks[key]:
                                await update_func(False)
        finally:
            self._waiting[host] -= 1
        return is_success

    async def getAllPropertyMaps(self, host, eojgc, eojcc, eojci):
        return await self.echonetMessage(
            host,
            eojgc,
            eojcc,
            eojci,
            GET,
            [
                {"EPC": ENL_STATMAP},
                {"EPC": ENL_GETMAP},
                {"EPC": ENL_SETMAP},
            ],
        )

    async def getIdentificationInformation(self, host, eojgc, eojcc, eojci):
        return await self.echonetMessage(
            host,
            eojgc,
            eojcc,
            eojci,
            GET,
            [{"EPC": ENL_UID}, {"EPC": ENL_MANUFACTURER}],
        )

    async def process_discovery_data(self, host, opc_data):
        if opc_data["EPC"] == ENL_UID:
            self._state[host]["uid"] = EPC_SUPER_FUNCTIONS[ENL_UID](
                opc_data["EDT"], host
            )
        elif opc_data["EPC"] == ENL_MANUFACTURER:
            self._state[host]["manufacturer"] = EPC_SUPER_FUNCTIONS[ENL_MANUFACTURER](
                opc_data["EDT"]
            )
        elif opc_data["EPC"] == ENL_PRODUCT_CODE:
            self._state[host]["product_code"] = EPC_SUPER_FUNCTIONS[ENL_PRODUCT_CODE](
                opc_data["EDT"]
            )
        else:
            edt = bytearray(opc_data["EDT"])
            # 1st byte: Total number of instances
            # 2nd to 253rd bytes: ECHONET object codes (EOJ3 bytes) enumerated
            edtnum = bytearray(edt)[0]
            for x in range(edtnum):
                eojgc = bytearray(edt)[1 + (3 * x)]
                eojcc = bytearray(edt)[2 + (3 * x)]
                eojci = bytearray(edt)[3 + (3 * x)]
                if eojgc != 0x0F:  # ignore this group code.
                    # populate state table
                    self._ensure_instance_state(host, eojgc, eojcc, eojci)

    def register_async_update_callbacks(self, host, eojgc, eojcc, eojci, fn):
        key = f"{host}-{eojgc}-{eojcc}-{eojci}"
        if key not in self._update_callbacks:
            self._update_callbacks[key] = []
        self._update_callbacks[key].append(fn)

    def register_async_receive_callbacks(self, host, eojgc, eojcc, eojci, fn):
        key = f"{host}-{eojgc}-{eojcc}-{eojci}"
        if key not in self._receive_callbacks:
            self._receive_callbacks[key] = []
        self._receive_callbacks[key].append(fn)

    def _ensure_instance_state(self, host, eojgc, eojcc, eojci):
        instances = self._state[host]["instances"]
        if eojgc not in instances:
            instances[eojgc] = {}
        if eojcc not in instances[eojgc]:
            instances[eojgc][eojcc] = {}
        if eojci not in instances[eojgc][eojcc]:
            instances[eojgc][eojcc][eojci] = {
                ENL_STATMAP: [],
                ENL_SETMAP: [],
                ENL_GETMAP: [],
            }

    async def _run_unknown_host_discovery(self, host):
        """
        Execute background discovery for an unknown host.

        This method is scheduled via `asyncio.create_task()` so that
        packet reception is not blocked by discovery logic.

        Any exception raised by the discovery callback will mark the
        discovery as failed and activate the retry suppression timer.
        """
        try:
            await asyncio.sleep(0.5)

            if callable(self._discover_callback):
                if self._debug_flag:
                    self._logger(f"Called _discover_callback('{host}')")
                await self._discover_callback(host)
        except Exception as err:
            self._unknown_discovery_last_failed[host] = time.monotonic()
            self._logger(f"Unknown host discovery failed for {host}: {err}")

            state = self._state.get(host)
            if state and not state.get("instances") and not state.get("discovered"):
                self._state.pop(host, None)
        finally:
            self._unknown_discovery_in_progress.discard(host)

    def _should_schedule_unknown_discovery(self, host):
        """
        Determine whether discovery should be scheduled for an unknown host.

        Discovery will be skipped if:
          - A discovery is already running for the host
          - Discovery was scheduled recently and cooldown has not expired
          - A previous discovery failed recently and suppression time
            has not yet expired
        """
        if host in self._unknown_discovery_in_progress:
            return False

        last_scheduled = self._unknown_discovery_last_scheduled.get(host)
        if last_scheduled is not None:
            if (
                time.monotonic() - last_scheduled
            ) < self._unknown_discovery_cooldown_seconds:
                return False

        last_failed = self._unknown_discovery_last_failed.get(host)
        if last_failed is not None:
            if (
                time.monotonic() - last_failed
            ) < self._unknown_discovery_suppress_seconds:
                return False

        return True


class EchonetMaxOpcError(Exception):
    pass
