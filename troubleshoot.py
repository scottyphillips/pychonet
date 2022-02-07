import asyncio

from aioudp import UDPServer

from pychonet import ECHONETAPIClient as api
from pychonet import EchonetInstance
from pychonet.lib.const import ENL_GETMAP, ENL_SETMAP, VERSION

# This example will list the properties for all discovered instances on a given host


async def main():

    print(f"pychonet verison is {VERSION}")
    udp = UDPServer()
    loop = asyncio.get_event_loop()
    udp.run("0.0.0.0", 3610, loop=loop)
    server = api(server=udp, loop=loop)

    host = "192.168.1.50"
    await server.discover(host)
    device = EchonetInstance("192.168.1.50", 2, 163, 1, server)
    # value = await device.getMessage(ENL_SETMAP)
    # print(value)
    getmap = await device.getMessage(ENL_GETMAP)
    print(f"getmap is {getmap}")

    setmap = await device.getMessage(ENL_SETMAP)
    print(f"setmap is {setmap}")

    for epc in getmap:
        value = await device.getMessage(epc)
        print(f"getmap value EPC code {epc} is {value}")

    for epc in setmap:
        value = await device.getMessage(epc)
        print(f"setmap value EPC code {epc} is {value}")


if __name__ == "__main__":
    asyncio.run(main())
