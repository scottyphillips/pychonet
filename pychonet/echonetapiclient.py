import asyncio
from dataclasses import dataclass
from time import monotonic
from typing import Any, Callable, Dict, List, Optional, Set, Tuple


from pychonet.lib.const import (
    ENL_GETMAP,
    ENL_MANUFACTURER,
    ENL_PRODUCT_CODE,
    ENL_PORT,
    INSTANCE_LIST,
    INSTANCE_LIST_NOTIFICATION,
    ENL_SETMAP,
    ENL_UID,
    GET,
    MESSAGE_TIMEOUT,
    ENL_STATMAP,
    SETRES,
    GETRES,
    INF,
    INFC,
    INFREQ,
    SETC_SND,
    GET_SNA,
    INF_SNA,
    SETI,
    SETC,
    ENL_BROADCAST_ADDRESS,
    ENL_MULTICAST_ADDRESS,
)
from pychonet.lib.epc_functions import EPC_SUPER_FUNCTIONS
from pychonet.lib.functions import (
    DEFAULT_SEOJ,
    MAX_TID_VALUE,
    DecodeEchonetMsgError,
    buildEchonetMsg,
    decodeEchonetMsg,
    encode_property_data,
)


_RESPONSE_ESVS = {
    GET: (GETRES, GET_SNA),
    SETC: (SETRES, SETC_SND),
    INFREQ: (INF, INF_SNA),
}
_CONTROLLER_EOJ = tuple(DEFAULT_SEOJ.to_bytes(3, "big"))
_NODE_PROFILE = (0x0E, 0xF0)
_PROPERTY_MAPS = {ENL_STATMAP, ENL_GETMAP, ENL_SETMAP}
_NODE_INFORMATION = {ENL_UID, ENL_MANUFACTURER, ENL_PRODUCT_CODE}


@dataclass
class _PendingRequest:
    host: str
    eoj: Tuple[int, int, int]
    esv: int
    properties: Dict[int, bytes]
    reply: "asyncio.Future[Tuple[bool, int]]"
    responders: Optional[Set[str]] = None


class ECHONETAPIClient:
    """ECHONET API client for handling ECHONETLite communication."""

    def __init__(self, server: Any):
        """Initialize the ECHONET API client.
        
        Args:
            server: UDPServer instance for sending and receiving messages
        """
        self._server: Any = server
        self._logger: Callable[..., Any] = print
        self._debug_flag: bool = False
        # Note: Home Assistant integration replaces self._logger with its own logger
        self._server.subscribe(self.echonetMessageReceived)
        self._state: Dict[str, Dict[str, Any]] = {}
        self._next_tx_tid: int = 0x0000
        self._pending_requests: Dict[int, _PendingRequest] = {}
        self._message_timeout: int = MESSAGE_TIMEOUT
        self._update_callbacks: Dict[str, List[Callable[[bool], Any]]] = {}
        self._receive_callbacks: Dict[str, List[Callable[[bool], Any]]] = {}
        self._discover_callback: Optional[Callable[[str], Any]] = None
        self._waiting: Dict[str, int] = {}
        self._last_activity: Dict[str, float] = {}  # host -> monotonic timestamp of last received packet

    async def echonetMessageReceived(self, raw_data: bytes, addr: Tuple[str, int]) -> None:
        """Update device state from a response or an unsolicited notification."""
        host = addr[0]
        try:
            message = decodeEchonetMsg(raw_data)
        except (DecodeEchonetMsgError, IndexError) as error:
            if self._debug_flag:
                self._logger(f"Ignoring an invalid ECHONET Lite frame from {host}: {error}")
            return

        properties = message["OPC"]
        if any(prop["PDC"] != len(prop["EDT"]) for prop in properties):
            return
        self._last_activity[host] = monotonic()

        tid = message["TID"]
        source = (message["SEOJGC"], message["SEOJCC"], message["SEOJCI"])
        destination = (message["DEOJGC"], message["DEOJCC"], message["DEOJCI"])
        esv = message["ESV"]
        if self._debug_flag:
            self._logger(f"ECHONET Lite message from {host}: {message}")

        request = self._pending_requests.get(tid)
        if request is not None and (
            destination != _CONTROLLER_EOJ
            or source[:2] != request.eoj[:2]
            or request.eoj[2] not in (0, source[2])
            or esv not in _RESPONSE_ESVS.get(request.esv, ())
            or (request.responders is None and (host != request.host or request.reply.done()))
        ):
            request = None

        if request is not None and request.responders is not None:
            await self._record_multicast_response(request, host, esv, properties)
            return

        if request is None and esv not in (INF, INFC):
            return
        if host not in self._state:
            if request is None and callable(self._discover_callback):
                await self._discover_callback(host)
            return
        if source[0] == 0x0F:
            return

        updated = False
        returned = set()
        accepted = 0
        is_set = esv in (SETRES, SETC_SND)
        is_profile = source[:2] == _NODE_PROFILE
        instance = None if is_profile else self._instance_state(host, source)
        if not is_profile and instance is None:
            if request is None:
                return
            instance = self._ensure_instance(host, source)

        for prop in properties:
            epc = prop["EPC"]
            if request is not None:
                if epc not in request.properties:
                    continue
                # A large node may return several D5 lists in one notification.
                multiple_lists = is_profile and esv == INF and epc == INSTANCE_LIST_NOTIFICATION
                if epc in returned and not multiple_lists:
                    continue
                returned.add(epc)
            if is_set:
                if prop["PDC"] != 0:
                    continue
                edt = request.properties[epc]
            else:
                if not prop["PDC"]:
                    continue
                edt = prop["EDT"]

            if is_profile:
                if not await self.process_discovery_data(host, prop):
                    continue
            elif epc in _PROPERTY_MAPS or epc in _NODE_INFORMATION:
                instance[epc] = EPC_SUPER_FUNCTIONS[epc](edt)
            else:
                updated |= instance.get(epc) != edt
                instance[epc] = edt
            accepted += 1

        if request is not None:
            if not returned:
                return
            if is_set:
                success = esv == SETRES and accepted == len(request.properties)
            else:
                success = accepted > 0
            request.reply.set_result((success, len(returned)))

        node = self._state[host]
        if not node.get("available"):
            node["available"] = True
            await self._notify_host_available(host)
            return

        key = f"{host}-{source[0]}-{source[1]}-{source[2]}"
        is_push = request is None
        if updated:
            for callback in tuple(self._update_callbacks.get(key, ())):
                await callback(is_push)
        for callback in tuple(self._receive_callbacks.get(key, ())):
            await callback(is_push)

    async def _record_multicast_response(self, request, host, esv, properties):
        if esv != GETRES or host in request.responders:
            return
        for prop in properties:
            if prop["EPC"] == INSTANCE_LIST and self._decode_instance_list(prop["EDT"], False):
                request.responders.add(host)
                node = self._state.setdefault(host, {"instances": {}, "available": True})
                unknown = not node["instances"] and not node.get("discovered")
                recovered = not node["available"]
                node["available"] = True
                await self.process_discovery_data(host, prop)
                if not request.reply.done():
                    request.reply.set_result((True, 1))
                if recovered:
                    await self._notify_host_available(host)
                if unknown and callable(self._discover_callback):
                    await self._discover_callback(host)
                else:
                    await self._request_additional_instances(host)
                return

    async def _notify_host_available(self, host):
        prefix = f"{host}-"
        for registry in (self._update_callbacks, self._receive_callbacks):
            for key, callbacks in tuple(registry.items()):
                if key.startswith(prefix):
                    for callback in tuple(callbacks):
                        await callback(False)

    def _instance_state(self, host, eoj):
        group, code, instance = eoj
        node = self._state.get(host, {})
        return node.get("instances", {}).get(group, {}).get(code, {}).get(instance)

    def _ensure_instance(self, host, eoj):
        group, code, instance = eoj
        instances = self._state[host]["instances"]
        return instances.setdefault(group, {}).setdefault(code, {}).setdefault(instance, {})

    def _allocate_tid(self):
        for _ in range(MAX_TID_VALUE):
            self._next_tx_tid = self._next_tx_tid % MAX_TID_VALUE + 1
            if self._next_tx_tid not in self._pending_requests:
                return self._next_tx_tid
        raise RuntimeError("No ECHONET Lite transaction IDs available")

    async def discover(
        self,
        host: str = ENL_MULTICAST_ADDRESS,
        *,
        broadcast: bool = False,
    ) -> Optional[bool]:
        """Discover devices on the network.

        Args:
            host: Host to discover (default: multicast address). The IPv4
                broadcast address requests both multicast and broadcast.
            broadcast: Also send multicast discovery to the IPv4 broadcast address.

        Returns:
            True on response, False on timeout, or None if the request queue is busy.
        """
        if host == ENL_BROADCAST_ADDRESS:
            host = ENL_MULTICAST_ADDRESS
            broadcast = True
        if host == ENL_MULTICAST_ADDRESS:
            opc = [{"EPC": INSTANCE_LIST}]
        else:
            opc = [
                {"EPC": ENL_MANUFACTURER},
                {"EPC": ENL_PRODUCT_CODE},
                {"EPC": ENL_UID},
                {"EPC": INSTANCE_LIST},
            ]
        if broadcast:
            return await self.echonetMessage(
                host, 0x0E, 0xF0, 0x01, GET, opc, broadcast=True
            )
        result = await self.echonetMessage(host, 0x0E, 0xF0, 0x01, GET, opc)
        if result and host != ENL_MULTICAST_ADDRESS:
            await self._request_additional_instances(host)
        return result

    async def _request_additional_instances(self, host):
        if self._state.get(host, {}).get("instance_count", 0) > 84:
            # D6 holds at most 84 EOJs. D5 can announce the rest in separate lists.
            await self.echonetMessage(
                host, 0x0E, 0xF0, 0x01, INFREQ,
                [{"EPC": INSTANCE_LIST_NOTIFICATION}],
            )

    async def echonetMessage(
        self,
        host: str,
        deojgc: int,
        deojcc: int,
        deojci: int,
        esv: int,
        opc: List[Dict[str, Any]],
        *,
        broadcast: bool = False,
    ) -> Optional[bool]:
        """Send an ECHONET message and await response.
        
        Args:
            host: Destination host IP
            deojgc: Destination ECHONET Group Code
            deojcc: Destination ECHONET Class Code
            deojci: Destination ECHONET Instance Code
            esv: Service Element Value
            opc: List of OPC dictionaries with EPC, PDC, EDT
            broadcast: Also send the multicast node discovery request via IPv4 broadcast.
            
        Returns:
            True if message was successful, False otherwise, None if queue is full
        """
        if host == ENL_BROADCAST_ADDRESS:
            raise ValueError("Use discover(broadcast=True) for IPv4 broadcast")

        eoj = (deojgc, deojcc, deojci)
        is_profile = eoj[:2] == _NODE_PROFILE
        multicast_discovery = (
            host == ENL_MULTICAST_ADDRESS
            and is_profile
            and esv == GET
            and [prop["EPC"] for prop in opc] == [INSTANCE_LIST]
        )
        if broadcast and not multicast_discovery:
            raise ValueError("Broadcast requires multicast node discovery")

        if self._waiting.get(host):
            for _ in range(self._message_timeout):
                await asyncio.sleep(0.1)
                if not self._waiting[host]:
                    break
            if self._waiting[host]:
                return None
        self._waiting[host] = 1
        tid = None
        retain_discovery = False
        try:
            instance = self._instance_state(host, eoj)
            if instance is not None and not is_profile:
                if esv == GET and ENL_GETMAP in instance:
                    readable = set(instance[ENL_GETMAP]) | _PROPERTY_MAPS
                    opc = [prop for prop in opc if prop["EPC"] in readable]
                elif esv in (SETC, SETI) and ENL_SETMAP in instance:
                    writable = set(instance[ENL_SETMAP])
                    if any(prop["EPC"] not in writable for prop in opc):
                        return False

            if not opc:
                return False
            properties = {prop["EPC"]: encode_property_data(prop) for prop in opc}
            if esv in (SETC, SETI) and not all(properties.values()):
                return False
            tid = self._allocate_tid()
            payload = buildEchonetMsg({
                "TID": tid,
                "DEOJGC": deojgc,
                "DEOJCC": deojcc,
                "DEOJCI": deojci,
                "ESV": esv,
                "OPC": opc,
            })

            loop = asyncio.get_running_loop()
            timeout = self._message_timeout * 0.1
            deadline = loop.time() + timeout
            if not multicast_discovery:
                self._state.setdefault(host, {"instances": {}, "available": True})
            if esv != SETI:
                request = _PendingRequest(
                    host, eoj, esv, properties, loop.create_future(),
                    set() if multicast_discovery else None,
                )
                self._pending_requests[tid] = request

            self._server.send(payload, (host, ENL_PORT))
            if broadcast:
                self._server.send(payload, (ENL_BROADCAST_ADDRESS, ENL_PORT))
            if esv == SETI:
                return True

            try:
                success, returned = await asyncio.wait_for(request.reply, timeout)
            except asyncio.TimeoutError:
                node = self._state.get(host)
                if not is_profile and node is not None and node["available"]:
                    node["available"] = False
                    prefix = f"{host}-"
                    for key, callbacks in tuple(self._update_callbacks.items()):
                        if key.startswith(prefix):
                            for callback in tuple(callbacks):
                                await callback(False)
                return False

            if multicast_discovery:
                # Keep deduplicating and collecting peers for the original discovery window.
                loop.call_at(deadline, self._pending_requests.pop, tid, None)
                retain_discovery = True
            elif esv == GET and not is_profile and returned < len(properties):
                raise EchonetMaxOpcError(returned)
            return success
        finally:
            if tid is not None and not retain_discovery:
                self._pending_requests.pop(tid, None)
            self._waiting[host] = 0

    async def getAllPropertyMaps(
        self,
        host: str,
        eojgc: int,
        eojcc: int,
        eojci: int,
    ) -> Dict[int, Any]:
        """Get property maps for a device.
        
        Args:
            host: Device host IP
            eojgc: ECHONET Group Code
            eojcc: ECHONET Class Code
            eojci: ECHONET Instance Code
            
        Returns:
            Dictionary containing STATMAP, GETMAP, and SETMAP
        """
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

    async def getIdentificationInformation(
        self,
        host: str,
        eojgc: int,
        eojcc: int,
        eojci: int,
    ) -> Dict[str, Any]:
        """Get device identification information.
        
        Args:
            host: Device host IP
            eojgc: ECHONET Group Code
            eojcc: ECHONET Class Code
            eojci: ECHONET Instance Code
            
        Returns:
            Dictionary containing UID and manufacturer information
        """
        return await self.echonetMessage(
            host,
            eojgc,
            eojcc,
            eojci,
            GET,
            [{"EPC": ENL_UID}, {"EPC": ENL_MANUFACTURER}],
        )

    @staticmethod
    def _decode_instance_list(edt, notification):
        if not edt or len(edt) > 253 or (len(edt) - 1) % 3:
            return None
        count = edt[0]
        listed = (len(edt) - 1) // 3
        if count < listed or ((notification or count <= 84) and count != listed):
            return None
        instances = [tuple(edt[index : index + 3]) for index in range(1, len(edt), 3)]
        return count, instances

    async def process_discovery_data(self, host: str, opc_data: Dict[str, Any]) -> bool:
        """Merge information from a node profile response."""
        node = self._state[host]
        epc = opc_data["EPC"]
        edt = opc_data["EDT"]
        if epc == ENL_UID:
            node["uid"] = EPC_SUPER_FUNCTIONS[ENL_UID](edt, host)
        elif epc == ENL_MANUFACTURER:
            node["manufacturer"] = EPC_SUPER_FUNCTIONS[ENL_MANUFACTURER](edt)
        elif epc == ENL_PRODUCT_CODE:
            node["product_code"] = EPC_SUPER_FUNCTIONS[ENL_PRODUCT_CODE](edt)
        elif epc in (INSTANCE_LIST, INSTANCE_LIST_NOTIFICATION):
            listing = self._decode_instance_list(edt, epc == INSTANCE_LIST_NOTIFICATION)
            if listing is None:
                return False
            count, instances = listing
            if epc == INSTANCE_LIST:
                node["instance_count"] = count
            for eoj in instances:
                if eoj[0] != 0x0F:
                    self._ensure_instance(host, eoj)
        else:
            return True

        if node["instances"]:
            if node.get("uid") is None:
                node["uid"] = EPC_SUPER_FUNCTIONS[ENL_UID](b"", host)
            if node.get("manufacturer") is None:
                node["manufacturer"] = EPC_SUPER_FUNCTIONS[ENL_MANUFACTURER](b"\xff\xff\xff")
            node["discovered"] = True
        return True

    def register_async_update_callbacks(
        self,
        host: str,
        eojgc: int,
        eojcc: int,
        eojci: int,
        fn: Callable[[], Any],
    ) -> None:
        """Register an async update callback.
        
        Args:
            host: Device host IP
            eojgc: ECHONET Group Code
            eojcc: ECHONET Class Code
            eojci: ECHONET Instance Code
            fn: Callback function to be called on updates
        """
        key = f"{host}-{eojgc}-{eojcc}-{eojci}"
        if key not in self._update_callbacks:
            self._update_callbacks[key] = []
        self._update_callbacks[key].append(fn)

    def register_async_receive_callbacks(
        self,
        host: str,
        eojgc: int,
        eojcc: int,
        eojci: int,
        fn: Callable[[], Any],
    ) -> None:
        """Register an async receive callback.
        
        Args:
            host: Device host IP
            eojgc: ECHONET Group Code
            eojcc: ECHONET Class Code
            eojci: ECHONET Instance Code
            fn: Callback function to be called on receives
        """
        key = f"{host}-{eojgc}-{eojcc}-{eojci}"
        if key not in self._receive_callbacks:
            self._receive_callbacks[key] = []
        self._receive_callbacks[key].append(fn)

    def unregister_async_update_callbacks(
        self,
        host: str,
        eojgc: int,
        eojcc: int,
        eojci: int,
    ) -> None:
        """Unregister all async update callbacks for a device.
        
        Args:
            host: Device host IP
            eojgc: ECHONET Group Code
            eojcc: ECHONET Class Code
            eojci: ECHONET Instance Code
        """
        key = f"{host}-{eojgc}-{eojcc}-{eojci}"
        if key in self._update_callbacks:
            self._update_callbacks[key].clear()

    def unregister_async_receive_callbacks(
        self,
        host: str,
        eojgc: int,
        eojcc: int,
        eojci: int,
    ) -> None:
        """Unregister all async receive callbacks for a device.
        
        Args:
            host: Device host IP
            eojgc: ECHONET Group Code
            eojcc: ECHONET Class Code
            eojci: ECHONET Instance Code
        """
        key = f"{host}-{eojgc}-{eojcc}-{eojci}"
        if key in self._receive_callbacks:
            self._receive_callbacks[key].clear()


    # ------------------------------------------------------------------
    # Public configuration and state management API
    # Provides clean alternatives to direct private attribute access,
    # addressing the coupling concern raised about external code touching
    # _state, _message_timeout, _logger, _debug_flag, _discover_callback,
    # _update_callbacks, and _server directly.
    # ------------------------------------------------------------------

    def configure(
        self,
        message_timeout: Optional[int] = None,
        logger: Optional[Callable[..., Any]] = None,
        debug: Optional[bool] = None,
        discover_callback: Optional[Callable[[str], Any]] = None,
    ) -> None:
        """Configure the API client settings.

        Replaces direct access to _message_timeout, _logger, _debug_flag,
        and _discover_callback private attributes.

        Args:
            message_timeout: Number of 0.1s ticks before a request times out.
                             Defaults to MESSAGE_TIMEOUT if not set.
            logger:          Callable for log output (e.g. logging.debug).
            debug:           Enable verbose internal debug logging.
            discover_callback: Async callable invoked when an unknown host
                               is detected. Receives host IP as argument.
        """
        if message_timeout is not None:
            self._message_timeout = message_timeout
        if logger is not None:
            self._logger = logger
        if debug is not None:
            self._debug_flag = debug
        if discover_callback is not None:
            self._discover_callback = discover_callback

    def register_multicast(self, host: str) -> None:
        """Register multicast for the interface used to reach host.

        Replaces direct access to server._server.register_multicast_from_host().

        Args:
            host: Device host IP address used to determine local interface.
        """
        self._server.register_multicast_from_host(host)

    def register_instance(
        self,
        host: str,
        eojgc: int,
        eojcc: int,
        eojci: int,
        ntfmap: List[int],
        setmap: List[int],
        getmap: List[int],
        uid: Optional[str] = None,
    ) -> None:
        """Pre-populate instance state from stored configuration.

        Replaces direct manipulation of the _state dict. Called during
        integration setup to restore known device state without performing
        a network discovery.

        Args:
            host:   Device host IP address.
            eojgc:  ECHONET Group Code.
            eojcc:  ECHONET Class Code.
            eojci:  ECHONET Instance Code.
            ntfmap: Notification property map (STATMAP).
            setmap: Set property map.
            getmap: Get property map.
            uid:    Optional device unique identifier.
        """
        self._state.setdefault(host, {"instances": {}, "available": True})
        instance = self._ensure_instance(host, (eojgc, eojcc, eojci))
        instance.setdefault(ENL_STATMAP, ntfmap)
        instance.setdefault(ENL_SETMAP, setmap)
        instance.setdefault(ENL_GETMAP, getmap)
        if uid is not None:
            instance.setdefault(ENL_UID, uid)

    def unregister_host(self, host: str) -> None:
        """Remove all state and callbacks for a host.

        Replaces direct manipulation of _state and _update_callbacks during
        integration unload.

        Args:
            host: Device host IP address to remove.
        """
        self._state.pop(host, None)
        for key in list(self._update_callbacks.keys()):
            if key.startswith(host):
                del self._update_callbacks[key]
        for key in list(self._receive_callbacks.keys()):
            if key.startswith(host):
                del self._receive_callbacks[key]

    @property
    def message_timeout(self) -> int:
        """Current message timeout in 0.1s ticks."""
        return self._message_timeout

    @property
    def state(self) -> Dict[str, Dict[str, Any]]:
        """Read-only view of internal device state.

        Returns the live state dict — callers should not mutate it directly.
        Use register_instance() and unregister_host() for state management.
        """
        return self._state

    def last_activity(self, host: str) -> Optional[float]:
        """Return monotonic timestamp of last received packet from host.

        Updated whenever any ECHONET Lite packet arrives from the host —
        GET responses, INF notifications, discovery packets, anything.
        Returns None if no packet has ever been received from this host.

        Callers can use this to implement a silence threshold for availability:

            elapsed = time.monotonic() - (server.last_activity(host) or 0)
            if elapsed > SILENCE_THRESHOLD:
                # device has been silent too long
        """
        return self._last_activity.get(host)


class EchonetMaxOpcError(Exception):
    pass
