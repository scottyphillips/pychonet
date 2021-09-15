import asyncio
from pprint import pprint

from aioudp import UDPServer
from pychonet import ECHONETAPIClient as api
from pychonet import Factory, EchonetInstance
from pychonet.lib.const import ENL_SETMAP, ENL_GETMAP, ENL_UID, ENL_MANUFACTURER

# This example will list the properties for all discovered instances on a given host

async def main():
    udp = UDPServer()
    loop = asyncio.get_event_loop()
    udp.run("0.0.0.0", 3610, loop=loop)
    server = api(server=udp, loop=loop)

    host = '192.168.1.50'
    await server.discover(host)
    device = EchonetInstance("192.168.1.50", 2,90,1, server)
    # value = await device.getMessage(ENL_SETMAP)
    # print(value)
    value = await device.getMessage(ENL_GETMAP)
    print(f"getmap is {value}")

    value = await device.getMessage(ENL_SETMAP)
    print(f"setmap is {value}")

if __name__ == "__main__":
    asyncio.run(main())
