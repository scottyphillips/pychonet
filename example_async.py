import asyncio
from pprint import pprint
from aioudp import UDPServer
from pychonet import ECHONETAPIClient as api
from pychonet.lib.const import ENL_SETMAP, ENL_GETMAP, ENL_UID, ENL_MANUFACTURER, VERSION
from pychonet.lib.epc import EPC_SUPER, EPC_CODE
from pychonet.lib.eojx import EOJX_GROUP, EOJX_CLASS

# This example will list the properties for all discovered instances on a given host

TARGET = '192.168.1.6'


def epc2str(gc, cc, pc):
    try:
        return EPC_SUPER[pc]
    except KeyError:
        pass

    try:
        return EPC_CODE[gc][cc][pc]
    except KeyError:
        return "Unknown"


async def main():
    udp = UDPServer()
    loop = asyncio.get_event_loop()
    udp.run("0.0.0.0", 3610, loop=loop)
    server = api(server=udp, loop=loop)
    server._debug_flag = False
    server._message_timeout = 300

    await server.discover(TARGET)
    # Timeout after 3 seconds
    for x in range(0, 300):
        await asyncio.sleep(0.01)
        if 'discovered' in list(server._state[TARGET]):
            break

    instance_list = []
    state = server._state[TARGET]

    for eojgc in state['instances'].keys():
        for eojcc in state['instances'][eojgc].keys():
            for instance in state['instances'][eojgc][eojcc].keys():
                # issue here??
                await server.getAllPropertyMaps(TARGET, eojgc, eojcc, 0x00)
                getmap = [(hex(e), epc2str(eojgc, eojcc, e))
                          for e in state['instances'][eojgc][eojcc][instance][ENL_GETMAP]]
                setmap = [(hex(e), epc2str(eojgc, eojcc, e))
                          for e in state['instances'][eojgc][eojcc][instance][ENL_SETMAP]]

                await server.getIdentificationInformation(TARGET, eojgc, eojcc, instance)
                uid = state['instances'][eojgc][eojcc][instance][ENL_UID]
                manufacturer = state['instances'][eojgc][eojcc][instance][ENL_MANUFACTURER]
                instance_list.append({
                    "host": TARGET,
                    "group": (hex(eojgc), EOJX_GROUP[eojgc]),
                    "class": (hex(eojcc), EOJX_CLASS[eojgc][eojcc]),
                    "instance": hex(instance),
                    "getmap": getmap,
                    "setmap": setmap,
                    "uid": uid,
                    "manufacturer": manufacturer
                })

    pprint(instance_list)

if __name__ == "__main__":
    asyncio.run(main())
