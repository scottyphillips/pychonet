"""
mitsubishi_echonet is used to provide control to Mitsubishi (and possibly other)
HVAC WiFi controllers that use the ECHONET-LITE protocol
such as the Mitsubishi MAC-IF558 adaptor.

I originally planned for this to be a full blown ECHONET library, but at this
stage it will control the AC and thats it!

"""

import socket
import struct
from pychonet.lib.eojx import EOJX_CLASS,EOJX_GROUP
from pychonet.lib.functions import buildEchonetMsg, sendMessage, decodeEchonetMsg
from pychonet.EchonetInstance import EchonetInstance

# Available classes.
from pychonet.HomeAirConditioner import HomeAirConditioner
from pychonet.HomeSolarPower import HomeSolarPower
from pychonet.StorageBattery import StorageBattery

"""
discover is used to identify ECHONET instances.
Previously this would return python objects corresponding to the echonet instances
but this got ugly and involved using lookup tables and eval.
Could probably fix this with switch case using the EOJX table.
As it stand you can use the object identifiers to instantiate your own objects

param ip_address: A string representing the IPv4 address e.g "1.2.3.4"
                  Defaults to ENL multicast address 224.0.23.0

return: an array of discovered ECHONET node instance information for example
        [{'eojgc': 1, 'eojcc': 48, 'eojci': 1, 'group':
        'Air conditioner-related device group', 'code': 'Home air conditioner'}]
"""
def discover(IP_ADDRESS = "224.0.23.0"):
    eoa = []; # array containing echonet objects
    # ESV 0x62 and EPC 0xD6 correspond to 'Self-node instance list S'
    tx_payload = {
        'TID' : 0x01, # Transaction ID 1
        'DEOJGC': 0x0E,
        'DEOJCC': 0xF0,
        'DEOJIC': 0x00,
        'ESV' : 0x62,
        'OPC' : [{'EPC': 0xD6}]
    }
    # Build ECHONET discover messafge.
    message = buildEchonetMsg(tx_payload)

    # Send message to multicast group and receive data
    data = sendMessage(message, IP_ADDRESS);
    # Decipher received message for each node discovered:

    for node in data:
        rx = decodeEchonetMsg(node['payload'])
        if (tx_payload['DEOJGC'] == rx['SEOJGC'] and
        rx['TID'] == tx_payload['TID'] and
        rx['OPC'][0]['EPC'] == 0xd6):
            # Process EDT for discovery info
            edt = rx['OPC'][0]['EDT']
            # Correspondes to 0xF0,0xD6
            data = int.from_bytes(edt, 'big')
            #1st byte: Total number of instances
            #2nd to 253rd bytes: ECHONET object codes (EOJ3 bytes) enumerated
            edtnum = bytearray(edt)[0]
            for x in range(edtnum):
                enl_instance = {}
                enl_instance['netaddr'] = node['server'][0]
                enl_instance['eojgc'] = bytearray(edt)[1 + (3 * x)]
                enl_instance['eojcc'] = bytearray(edt)[2 + (3 * x)]
                enl_instance['eojci'] = bytearray(edt)[3 + (3 * x)]

                try:
                    enl_instance['group'] = EOJX_GROUP[enl_instance['eojgc']]
                    enl_instance['code'] = EOJX_CLASS[enl_instance['eojgc']][enl_instance['eojcc'] ]
                except KeyError as e:
                    pass

                eoa.append(enl_instance)

    return eoa
