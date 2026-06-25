import asyncio
from typing import Callable, Dict, List, Tuple, Any, Optional


from pychonet.lib.const import (
    ENL_GETMAP,
    ENL_MANUFACTURER,
    ENL_PRODUCT_CODE,
    ENL_PORT,
    INSTANCE_LIST,
    ENL_SETMAP,
    ENL_UID,
    GET,
    MESSAGE_TIMEOUT,
    ENL_STATMAP,
    SETRES,
    GETRES,
    INF,
    INFC,
    SETC_SND,
    GET_SNA,
    INF_SNA,
    SETI,
    SETC,
    ENL_MULTICAST_ADDRESS,
)
from pychonet.lib.epc_functions import EPC_SUPER_FUNCTIONS
from pychonet.lib.functions import TIDError, buildEchonetMsg, decodeEchonetMsg

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
        self._message_list: Dict[int, Dict[str, Any]] = {}
        self._failure_list: Dict[int, int] = {}
        self._opc_counts: Dict[int, int] = {}
        self._message_timeout: int = MESSAGE_TIMEOUT
        self._update_callbacks: Dict[str, List[Callable[[bool], Any]]] = {}
        self._receive_callbacks: Dict[str, List[Callable[[bool], Any]]] = {}
        self._discover_callback: Optional[Callable[[str], Any]] = None
        self._waiting: Dict[str, int] = {}
        self._last_activity: Dict[str, float] = {}  # host -> monotonic timestamp of last received packet

    async def echonetMessageReceived(
        self,
        raw_data: bytes,
        addr: Tuple[str, int],
    ) -> None:
        """Handle incoming ECHONET messages.
        
        Args:
            raw_data: Raw bytes of the received message
            addr: Tuple of (host IP, port) from the sender
        """
        updated = False
        host = addr[0]
        import time as _time
        self._last_activity[host] = _time.monotonic()
        is_discovery = False

        if self._debug_flag:
            self._logger(
                f"ECHONETLite Message Received from {host} - Raw data is {raw_data}"
            )

        processed_data = decodeEchonetMsg(raw_data)

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

        if self._state.get(host) is None:  # echonet packet arrived we dont know about
            self._logger(f"Unknown ECHONETLite node has been identified - {host}")
            if callable(self._discover_callback):
                if self._debug_flag:
                    self._logger(f"Called _discover_callback('{host}')")
                await self._discover_callback(host)
            return

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
                    self._logger(f"ignoring packet but please notify devs on Github.")
            else:  # process each EPC in order
                if epc == ENL_SETMAP or epc == ENL_GETMAP or epc == ENL_STATMAP:
                    map = EPC_SUPER_FUNCTIONS[epc](opc["EDT"])
                    self._state[host]["instances"][seojgc][seojcc][seojci][epc] = map
                elif epc in (ENL_UID, ENL_MANUFACTURER, ENL_PRODUCT_CODE):
                    try:
                        self._state[host]["instances"][seojgc][seojcc][seojci][
                            epc
                        ] = EPC_SUPER_FUNCTIONS[epc](opc["EDT"])
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

        # if we get duplicate packets that have already been processed then dont worry about the message list.
        # but still process them regardless.
        if tid_data is not None:
            del self._message_list[tid]

    async def discover(
        self,
        host: str = ENL_MULTICAST_ADDRESS,
    ) -> List[Any]:
        """Discover devices on the network.
        
        Args:
            host: Host to discover (default: multicast address)
            
        Returns:
            List of discovered device information
        """
        if host is ENL_MULTICAST_ADDRESS:
            opc = [{"EPC": INSTANCE_LIST}]
        else:
            opc = [
                {"EPC": ENL_MANUFACTURER},
                {"EPC": ENL_PRODUCT_CODE},
                {"EPC": ENL_UID},
                {"EPC": INSTANCE_LIST},
            ]
        return await self.echonetMessage(host, 0x0E, 0xF0, 0x01, GET, opc)

    async def echonetMessage(
        self,
        host: str,
        deojgc: int,
        deojcc: int,
        deojci: int,
        esv: int,
        opc: List[Dict[str, Any]],
    ) -> bool:
        """Send an ECHONET message and await response.
        
        Args:
            host: Destination host IP
            deojgc: Destination ECHONET Group Code
            deojcc: Destination ECHONET Class Code
            deojci: Destination ECHONET Instance Code
            esv: Service Element Value
            opc: List of OPC dictionaries with EPC, PDC, EDT
            
        Returns:
            True if message was successful, False otherwise, None if queue is full
        """
        no_res = True if esv is SETI else False
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
                # Wait up to message_timeout * 0.1 seconds for the queue to clear.
                await asyncio.sleep(0.1)
                if not self._waiting[host]:
                    break
            if self._waiting[host]:
                # Queue is still busy — return None to distinguish this from a
                # genuine device timeout (False). Callers can treat None as
                # "queue busy, serve cached data" rather than "device offline".
                return None
        self._waiting[host] += 1

        self._next_tx_tid += 1
        tx_tid = self._next_tx_tid
        message_array["TID"] = tx_tid
        try:
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

            if not no_res:
                not_timeout = False
                for x in range(0, self._message_timeout):
                    # Wait up to 20(0.1*200) seconds depending on the Echonet specifications.
                    await asyncio.sleep(0.1)
                    # if tx_tid is not in message list then the message listener has received the message
                    if self._message_list.get(tx_tid) is None:
                        # Check OPC count in results
                        if not is_discover and tx_tid in self._opc_counts:
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

    async def process_discovery_data(
        self,
        host: str,
        opc_data: Dict[str, Any],
    ) -> None:
        """Process discovered device data.
        
        Args:
            host: Device host IP
            opc_data: OPC data from discovery response
        """
        if "discovered" not in self._state[host]:
            if opc_data["EPC"] == ENL_UID:
                self._state[host]["uid"] = EPC_SUPER_FUNCTIONS[ENL_UID](
                    opc_data["EDT"], host
                )
            elif opc_data["EPC"] == ENL_MANUFACTURER:
                self._state[host]["manufacturer"] = EPC_SUPER_FUNCTIONS[
                    ENL_MANUFACTURER
                ](opc_data["EDT"])
            elif opc_data["EPC"] == ENL_PRODUCT_CODE:
                self._state[host]["product_code"] = EPC_SUPER_FUNCTIONS[
                    ENL_PRODUCT_CODE
                ](opc_data["EDT"])
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
                        if eojgc not in list(self._state[host]["instances"].keys()):
                            self._state[host]["instances"].update({eojgc: {}})
                        if eojcc not in list(
                            self._state[host]["instances"][eojgc].keys()
                        ):
                            self._state[host]["instances"][eojgc].update({eojcc: {}})
                        if eojci not in list(
                            self._state[host]["instances"][eojgc][eojcc].keys()
                        ):
                            self._state[host]["instances"][eojgc][eojcc][eojci] = {}
                            self._state[host]["instances"][eojgc][eojcc][eojci].update(
                                {ENL_STATMAP: []}
                            )
                            self._state[host]["instances"][eojgc][eojcc][eojci].update(
                                {ENL_SETMAP: []}
                            )
                            self._state[host]["instances"][eojgc][eojcc][eojci].update(
                                {ENL_GETMAP: []}
                            )

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
        from pychonet.lib.const import ENL_STATMAP, ENL_SETMAP, ENL_GETMAP, ENL_UID

        if host not in self._state:
            self._state[host] = {"instances": {}, "available": True}

        instances = self._state[host]["instances"]
        if eojgc not in instances:
            instances[eojgc] = {}
        if eojcc not in instances[eojgc]:
            instances[eojgc][eojcc] = {}
        if eojci not in instances[eojgc][eojcc]:
            instances[eojgc][eojcc][eojci] = {
                ENL_STATMAP: ntfmap,
                ENL_SETMAP: setmap,
                ENL_GETMAP: getmap,
            }
            if uid is not None:
                instances[eojgc][eojcc][eojci][ENL_UID] = uid

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