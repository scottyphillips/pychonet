# Pychonet

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)
![Project Maintenance][maintenance-shield]

A Python library for interfacing with the ECHONET Lite protocol as commonly used in Japan.
Useful for interfacing with HVACs, lighting systems, electric car chargers, solar systems,
distribution panel meters, water heaters, and many other devices that support ECHONET Lite.

Designed to work with Python 3.9+. Built on asyncio for compatibility with Home Assistant
and other async frameworks.

## Installation

```bash
pip install pychonet
```

## Basic Usage

### Start the ECHONET Lite listener

```python
import asyncio
from pychonet.lib.udpserver import UDPServer
from pychonet import ECHONETAPIClient as api

udp = UDPServer()
loop = asyncio.get_event_loop()
udp.run("0.0.0.0", 3610, loop=loop)
server = api(server=udp)
```

### Configure the client

```python
import logging
_LOGGER = logging.getLogger(__name__)

server.configure(
    message_timeout=50,       # 50 ticks × 0.1s = 5s per request (default: 200 = 20s)
    logger=_LOGGER.debug,     # route pychonet logs to your logger
    debug=True,               # enable verbose internal logging
    discover_callback=my_cb,  # async callback when unknown host is detected
)
```

### Discover devices

```python
# Discover instances on a host
await server.discover('192.168.1.6')

# Register multicast for the interface used to reach a host
server.register_multicast('192.168.1.6')
```

### Pre-populate instance state (without network discovery)

Useful when restoring known device state from stored configuration:

```python
server.register_instance(
    host='192.168.1.6',
    eojgc=1, eojcc=48, eojci=1,
    ntfmap=[0x80, 0x81, 0x88],   # STATMAP — EPCs the device pushes notifications for
    setmap=[0x80, 0x81, 0xB3],   # SETMAP
    getmap=[0x80, 0x81, 0x88, 0xB3, 0xBB],  # GETMAP
    uid='abc123',
)
```

### Unregister a host (e.g. on shutdown)

```python
server.unregister_host('192.168.1.6')
```

### Create a device instance

```python
from pychonet import Factory

# Using the Factory (recommended — selects the correct class automatically)
device = Factory('192.168.1.6', server, 1, 48, 1)

# Or directly
from pychonet import HomeAirConditioner
aircon = HomeAirConditioner('192.168.1.6', server)
```

### Read EPC values

```python
# Read all supported EPCs
data = await device.update()

# Read specific EPCs
data = await device.update([0x80, 0xBB, 0xB3])

# Read from local cache (no network request)
data = await device.update([0x80], no_request=True)
```

### Write EPC values

```python
# Set a single EPC
await device.setMessage(0x80, b'\x30')  # operating status = on

# Set multiple EPCs
await device.setMessages([
    {'EPC': 0x80, 'EDT': b'\x30'},
    {'EPC': 0xB3, 'EDT': b'\x41'},
])
```

### Register custom EPC decode functions (quirks)

For devices with non-standard EPC behaviour, register instance-level overrides:

```python
def my_custom_decoder(edt):
    return {'value': int.from_bytes(edt, 'big')}

device.register_epc_function(0xB3, my_custom_decoder)
```

This creates an instance-level override — the custom function only applies to this
device instance, not all instances of the same device class.

### Push notifications

Register a callback to receive unsolicited INF packets from the device:

```python
async def on_update(isPush: bool):
    data = await device.update([0x80, 0x88], no_request=True)
    print(f"Device state changed: {data}")

server.register_async_update_callbacks('192.168.1.6', 1, 48, 1, on_update)
```

Unregister when done:

```python
server.unregister_async_update_callbacks('192.168.1.6', 1, 48, 1)
```

### Populate property maps

```python
await server.getAllPropertyMaps('192.168.1.6', 1, 48, 1)
```

## Return values from `update()`

| Return value | Meaning |
|---|---|
| `dict` | Success — EPC values keyed by EPC code |
| `None` | pychonet `_waiting` queue was busy — request not sent, serve cached data |
| Raises `TimeoutError` | Request sent but device did not respond |

`None` (queue busy) should be treated as a cache-serve rather than an error. A `TimeoutError`
indicates the device genuinely did not respond within `message_timeout` ticks.

## Device Classes

pychonet includes classes for many ECHONET Lite device types. Each class provides
an `EPC_FUNCTIONS` dict mapping EPC codes to decode functions, and inherits the
generic `update()` and `setMessage()` API from `EchonetInstance`.

Use `Factory()` to automatically select the correct class based on `eojgc`/`eojcc`:

```python
from pychonet import Factory
device = Factory(host, server, eojgc, eojcc, eojci)
```

For device types not yet supported, `EchonetInstance` provides raw connectivity
and the generic `update()`/`setMessage()` API works for any EPC.

## Using with Home Assistant

For Home Assistant users there is a dedicated integration installable via HACS:

**https://github.com/scottyphillips/echonetlite_homeassistant**

## Hall of Fame

Big thanks to Naoki Sawada (nao-pon) for many excellent updates including push
notification support via multicast.
どうもありがとうございます！

Thanks to Jason Nader for quality of life updates to the codebase and documentation.

Thanks to khcnz (Karl Chaffey) and gvs for helping refactor the old code
and contributing to testing.

Thanks to Dick Swart, Masaki Tagawa, Paul, khcnz, Kolodnerd, Leonunix, and Alfie Gerner
for contributing code updates to this library.

Thanks to Jeffro Carr who inspired me to write a native Python ECHONET library
for Home Assistant.

Thanks to Futomi Hatano for open sourcing a well-documented ECHONET Lite library
in Node JS: https://github.com/futomi/node-echonet-lite

Extra Special thanks to 'sayurin' for offering up so many constructive ideas on how to make this project better,

## References

- [ECHONET Lite Specification, Version 1.13](https://echonet.jp/spec_v113_lite_en/)
- [APPENDIX, Detailed Requirements for ECHONET Device objects, Release Q](https://echonet.jp/wp/wp-content/uploads/pdf/General/Standard/Release/Release_Q/Appendix_Release_Q_E.pdf)
- [Machine Readable Appendix (MRA)](https://echonet.jp/spec_mra_rq/)

## License

MIT License — refer to LICENSE for details.

Portions of 'ECHONET Lite Device Emulator' (Copyright 2020 Kanagawa Institute of Technology)
have been used. Licensed under MIT.

The UDP code is based on 'aio-udp-server' (Copyright 2021 Dmitriy Bashkirtsev).
Licensed under GPL: https://github.com/bashkirtsevich-llc/aioudp

---
[pychonet]: https://github.com/scottyphillips/pychonet
[releases-shield]: https://img.shields.io/github/release/scottyphillips/pychonet.svg?style=for-the-badge
[releases]: https://github.com/scottyphillips/pychonet/releases
[license-shield]: https://img.shields.io/github/license/scottyphillips/pychonet?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/Maintainer-Scott%20Phillips-blue?style=for-the-badge