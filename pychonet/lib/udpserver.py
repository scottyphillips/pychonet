import asyncio
import socket
import struct
from collections import deque


class UDPServer:
    def __init__(
        self, upload_speed=0, download_speed=0, recv_max_size=256 * 1024, local_ip=None
    ):
        self._upload_speed = upload_speed
        self._download_speed = download_speed
        self._recv_max_size = recv_max_size

        # Get Local IP address
        self._ip = (
            local_ip
            or [
                (s.connect(("224.0.23.0", 3610)), s.getsockname()[0], s.close())
                for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
            ][0][1]
        )

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setblocking(False)

        # enable multicast
        self._multicast_ips = set()
        self.register_multicast(self._ip)

        self._send_event = asyncio.Event()
        self._send_queue = deque()

        self._subscribers = {}

    # figure out which multicast IP would be used to reach host
    def register_multicast_from_host(self, host):
        # connect to known destination, e.g. via UDP port 80
        temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_sock.connect((host, 80))
        with temp_sock:
            local_ip, *_ = temp_sock.getsockname()
            self.register_multicast(local_ip)

    def register_multicast(self, local_ip):
        if local_ip not in self._multicast_ips:
            self._multicast_ips.add(local_ip)
            self._sock.setsockopt(
                socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(local_ip)
            )
            mreq = struct.pack(
                "=4s4s", socket.inet_aton("224.0.23.0"), socket.inet_aton(local_ip)
            )
            self._sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # region Interface
    def run(self, host, port, loop):
        self.loop = loop

        self._sock.bind((host, port))

        self._connection_made()

        self._run_future(self._send_periodically(), self._recv_periodically())

    def subscribe(self, fut):
        self._subscribers[id(fut)] = fut

    def unsubscribe(self, fut):
        self._subscribers.pop(id(fut), None)

    def send(self, data, addr):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("Param 'data' should be bytes or bytearray type")

        self._send_queue.append((data, addr))
        self._send_event.set()

    # endregion

    def _run_future(self, *args):
        for fut in args:
            asyncio.ensure_future(fut, loop=self.loop)

    def _sock_recv(self, fut=None, registered=False):
        fd = self._sock.fileno()

        if fut is None:
            fut = self.loop.create_future()

        if registered:
            self.loop.remove_reader(fd)

        try:
            data, addr = self._sock.recvfrom(self._recv_max_size)
        except (BlockingIOError, InterruptedError, OSError):
            self.loop.add_reader(fd, self._sock_recv, fut, True)
        except Exception as e:
            fut.set_exception(e)
            self._socket_error(e)
        else:
            fut.set_result((data, addr))

        return fut

    def _sock_send(self, data, addr, fut=None, registered=False):
        fd = self._sock.fileno()

        if fut is None:
            fut = self.loop.create_future()

        if registered:
            self.loop.remove_writer(fd)

        if not data:
            return

        try:
            bytes_sent = self._sock.sendto(data, addr)
        except (BlockingIOError, InterruptedError, OSError):
            self.loop.add_writer(fd, self._sock_send, data, addr, fut, True)
        except Exception as e:
            fut.set_exception(e)
            self._socket_error(e)
        else:
            fut.set_result(bytes_sent)

        return fut

    async def _throttle(self, data_len, speed=0):
        delay = (data_len / speed) if speed > 0 else 0
        await asyncio.sleep(delay)

    async def _send_periodically(self):
        while True:
            await self._send_event.wait()
            try:
                while self._send_queue:
                    data, addr = self._send_queue.popleft()
                    bytes_sent = self._sock_send(data, addr)
                    await self._throttle(bytes_sent, self._upload_speed)
            finally:
                self._send_event.clear()

    async def _recv_periodically(self):
        while True:
            data, addr = await self._sock_recv()
            self._notify_subscribers(*self._datagram_received(data, addr))
            await self._throttle(len(data), self._download_speed)

    def _connection_made(self):
        pass

    def _socket_error(self, e):
        pass

    def _datagram_received(self, data, addr):
        return data, addr

    def _notify_subscribers(self, data, addr):
        self._run_future(*(fut(data, addr) for fut in self._subscribers.values()))
