import asyncio
from pprint import pprint

from aioudp import UDPServer
from pychonet import ECHONETAPIClient as api
from pychonet.lib.const import ENL_SETMAP, ENL_GETMAP, ENL_UID, ENL_MANUFACTURER

# This example will list the properties for all discovered instances on a given host

async def main():
    udp = UDPServer()
    loop = asyncio.get_event_loop()
    udp.run("0.0.0.0", 3610, loop=loop)
    server = api(server=udp, loop=loop)

    host = '192.168.1.230'
    await server.discover(host)

    # Timeout after 3 seconds
    for x in range(0, 300):
        await asyncio.sleep(0.01)
        if 'discovered' in list(server._state[host]):
             print(f"{host} - ECHONET Node Discovery Successful!")
             break

    instance_list = []
    state = server._state[host]
    for eojgc in list(state['instances'].keys()):
        for eojcc in list(state['instances'][eojgc].keys()):
            for instance in list(state['instances'][eojgc][eojcc].keys()):
                  instance_info = f"{hex(eojgc)}-{hex(eojcc)}-{hex(instance)}"
                  await server.getAllPropertyMaps(host, eojgc, eojcc, instance)
                  print(f"{host} - ECHONET Instance {instance_info} map attributes discovered!")
                  print(f"get map is - {state['instances'][eojgc][eojcc][instance][ENL_GETMAP]}")
                  print(f"set map is - {state['instances'][eojgc][eojcc][instance][ENL_SETMAP]}")
                  getmap = [hex(e) for e in state['instances'][eojgc][eojcc][instance][ENL_GETMAP]]
                  setmap = [hex(e) for e in state['instances'][eojgc][eojcc][instance][ENL_SETMAP]]

                  await server.getIdentificationInformation(host, eojgc, eojcc, instance)
                  uid = state['instances'][eojgc][eojcc][instance][ENL_UID]
                  manufacturer = state['instances'][eojgc][eojcc][instance][ENL_MANUFACTURER]
                  print(f"{host} - ECHONET Instance {instance_info} identification number discovered!")
                  instance_list.append({"host":host,"eojgc":hex(eojgc),"eojcc":hex(eojcc),"eojci":hex(instance),"getmap":getmap,"setmap":setmap,"uid":uid,"manufacturer":manufacturer})

        pprint(instance_list)

if __name__ == "__main__":
    asyncio.run(main())
