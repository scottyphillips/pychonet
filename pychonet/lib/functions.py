import socket
import struct
import sys
import time
from .eojx import EOJX_GROUP, EOJX_CLASS

# Echonetlite message format:
#
# - EDT0     |Property value data             |01 ..|01 01 30 01
#  - NUM     |Total number of instances       |01   |1
#  - EOJ     |ECHONET Lite object specificat..|01 ..|01 30 01
#    - EOJX1 |Class group code                |01   |Air conditioner-related device class group
#    - EOJX2 |Class code                      |30   |Home air conditioner class
#    - EOJX3 |Instance code                   |01   |1

ENL_PORT = 3610
ENL_MULTICAST_ADDRESS = "224.0.23.0"

# ------------------------------------------------------------------
# EHD1: ECHONET Lite Header 1
# ---------------------------------------------------------------- */
EHD1 = {
    0x00: 'Not available',
    0x10: 'Conventional ECHONET Lite Specification'
}

# ------------------------------------------------------------------
# EHD1: ECHONET Lite Header 2
# ---------------------------------------------------------------- */
EHD2 = {
    0x81: 'Format 1 (specified message format)',
    0x82: 'Format 2 (arbitrary message format)'
}

# ------------------------------------------------------------------
# ESV
# ------------------------------------------------------------------
GETC = 			0x60
SETC = 			0x61
GET  = 			0x62
INFREQ =		0x63
SETGET = 		0x6E
SETRES =		0x71
GETRES =		0x72
INF =			0x73
INFC = 			0x74
INFC_RES =		0x7A
SETGET_RES =	0x7E
SETI_SNA = 		0x50
SETC_SND =		0x51
GET_SNA = 		0x52
INF_SNA = 		0x53
SETGET_SNA =	0x5E

ESV_CODES = {
	0x60: {'name': 'GetC', 'description': 'Property value write request (no response required)'},
	0x61: {'name': 'SetC', 'description': 'Property value write request (response required)'},
	0x62: {'name': 'Get', 'description': 'Property value read request'},
	0x63: {'name': 'INF_REQ', 'description': 'Property value notification request'},
	0x6E: {'name': 'SetGet', 'description': 'Property value write & read request'},
	0x71: {'name': 'Set_Res', 'description': 'Property value Property value write response'},
	0x72: {'name': 'Get_Res' , 'description': 'Property value read response'},
	0x73: {'name': 'INF' , 'description': 'Property value notification'},
	0x74: {'name': 'INFC', 'description': 'Property value notification (response required)'},
	0x7A: {'name': 'INFC_Res' , 'description': 'Property value notification response'},
	0x7E: {'name': 'SetGet_Res' , 'description': 'Property value write & read response'},
	0x50: {'name': 'SetI_SNA', 'description': 'Property value write request (response not possible)'},
	0x51: {'name': 'SetC_SNA' , 'description': 'Property value write request (response not possible)'},
	0x52: {'name': 'Get_SNA', 'description': 'Property value read (response not possible)'},
	0x53: {'name': 'INF_SNA', 'description': 'Property value notification (response not possible)'},
    0x5E: {'name': 'SetGet_SNA', 'description': 'Property value write & read (response not possible)'}
}


"""
buildEchonetMsg is used to build an ECHONET-LITE control message in the form
of a byte string

param data: a dict representing the control message.
return: an int representing the control message.
"""
def buildEchonetMsg(data):
   try:
      # EHD is fixed to 0x1081 because I am lazy.
      message = 0x1081

      # validate TID (set a default value if none provided)
      # TODO - TID message overlap.
      if 'TID' not in data:
         data['TID'] = 0x01
      elif data['TID'] > 0xFFFF:
         raise ValueError('Transaction ID is larger then 2 bytes.')
      message = (message << 16) + data['TID']

      # append SEOJ
      message = (message << 24) + 0x05FF01

      # validate DEOJ
      if data['DEOJGC'] in EOJX_GROUP:
          message = (message << 8) + data['DEOJGC']
      else:
          raise ValueError('Value ' + str(hex(data['DEOJGC'])) + ' not a valid SEO Group code')

      if data['DEOJCC'] in EOJX_CLASS[data['DEOJGC']]:
          message = (message << 8) + data['DEOJCC']
      else:
          raise ValueError('Value ' + str(hex(data['DEOJCC'])) + ' not a valid SEO class code')
      message = (message << 8) + data['DEOJIC']

      # validate ESV by looking up the codes.
      if data['ESV'] in ESV_CODES:
          # ESV code is a string
          message = (message << 8) + data['ESV']
      else:
          raise ValueError('Value not in ESV code table')

      # validate OPC
      message = (message << 8) + len(data['OPC'])

      # You can have multiple OPC per transaction.
      for values in data['OPC']:
        # validate EPC
        message =  (message << 8) + values['EPC']
        if 'PDC' in values:
            message =  (message << 8) + values['PDC']
        # if PDC has a value then concat EDT to message
            if values['PDC'] > 0:
                message =  (message << 8 * values['PDC']) + values['EDT']
        else:
            message =  (message << 8) + 0x00
      return format(int(message), 'x')
# some sloppy error handling here.
   except ValueError as error:
        # print('Caught this error: ' + repr(error))
        quit()


"""
decodeEchonetMsg is used to build an ECHONET-LITE control message in the form
of a byte string

param bytes: A bytestring representing the hexadecimal control message in ECHONET LITE
return: a dict representing the deconstructed ECHONET packet
"""
def decodeEchonetMsg(byte):
  data = {}
  try:
      data['EHD1'] = byte[0]
      if data['EHD1'] not in EHD1:
          raise ValueError('EHD1 Header invalid')
      data['EHD2'] = byte[1]
      if data['EHD2'] not in EHD2:
          raise ValueError('EHD2 Header invalid')
      data['TID'] = int.from_bytes(byte[2:4], byteorder='big')

      # Decode SEOJ
      data['SEOJGC'] = byte[4]
      data['SEOJCC'] = byte[5]
      data['SEOJIC'] = byte[6]

      # Decode DEOJ
      data['DEOJGC'] =  byte[7]
      data['DEOJCC'] =  byte[8]
      data['DEOJIC'] =  byte[9]

      # Decode Service property
      data['ESV'] =  byte[10]

      i = 0
      epc_pointer = 12
      data['OPC'] = []
      # decode multiple processing properties (OPC)
      while i <  (byte[11]):
          OPC = {}
          pdc_pointer = epc_pointer + 1
          edt_pointer = pdc_pointer + 1
          end_pointer = edt_pointer
          OPC['EPC'] = byte[epc_pointer]
          OPC['PDC'] =  byte[pdc_pointer]
          pdc_len = byte[pdc_pointer]
          end_pointer += pdc_len
          OPC['EDT'] = byte[edt_pointer:end_pointer]
          epc_pointer = end_pointer
          i += 1
          data['OPC'].append(OPC)

  except ValueError as error:
        print('Caught this error: ' + repr(error))
        quit()
  return data

"""
sendMessage is used for ECHONET Unicast and Multicast transcations
message is assumed a correctly formatted ECHONET string
sendMessage will receive multiple messages if multicast is used "eg 224.0.23.0"

param message: an int representing the ECHONET message
param ip_address: a string representing the IPv4 address e.g "1.2.3.4"

return: an array representing the received response from the ECHONET message
"""
def sendMessage(message, ip_address):
    data =[]
    transaction_group = (ip_address, ENL_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_open = True
    while True:
        try:
            sock.bind(('',ENL_PORT))
            break
        except OSError:
            # Wait for socket to be open:
            time.sleep(0.5)

    # Set a timeout so the socket does not block
    # indefinitely when trying to receive data.
    sock.settimeout(0.5)

    # Set the time-to-live for messages to 1 so they do not
    # go past the local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    try:
        sent = sock.sendto(bytearray.fromhex(message), transaction_group)
        # Look for responses from all recipients
        while True:
            try:
                payload, server = sock.recvfrom(1024)
            except socket.timeout:
                break
            else:
                # print(payload)
                # Received a packet.
                data.append({'server':server,'payload':payload})
    finally:
        sock.close()
    return data



"""
getOpCode is used to crunch the EPC and EDT payloads from GET requests

return: an array containing dicts in the following ecample format:
[{'rx_edt': b'\x11\r\x01\x01\t\x00\x00\x01\x00\x01\x01\x01\x08\x00\x02\n\x03', 'rx_epc': 159}, {'rx_edt': b'\x06\x80\x81\x8f\xa0\xb0\xb3', 'rx_epc': 158}]

"""
def getOpCode(ip_address, deojgc, deojcc, deojci, opc, tid=0x01):
        tx_payload = {
            'TID' : tid, # Transaction ID 1
            'DEOJGC': deojgc,
            'DEOJCC': deojcc,
            'DEOJIC': deojci,
            'ESV' : GET,
            'OPC' : opc
        }
        # Build ECHONET discover messafge.
        message = buildEchonetMsg(tx_payload)
        rx_data = sendMessage(message, ip_address)
        return_data = []
        if len(rx_data) > 0:
            rx = decodeEchonetMsg(rx_data[0]['payload'])

            # Action EDT payload by calling applicable function using lookup table
            for value in rx['OPC']:
                edt = {}
                edt['rx_edt'] = value['EDT']
                edt['rx_epc'] = value['EPC']
                return_data.append(edt)

        # print(return_data)
        return return_data
