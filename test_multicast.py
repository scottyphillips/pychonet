import socket
import struct

def test_multicast():
    MCAST_GRP = '224.0.23.0'
    MCAST_PORT = 3610
    # ECHONET Lite Discovery Packet (Search for Node Profile)
    # Format: EHD1, EHD2, TID, SEOJ, DEOJ, ESV, OPC, EPC
    msg = b'\x10\x81\x00\x01\x0e\xf0\x01\x0e\xf0\x01\x62\x01\xd6\x00'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(5.0)
    
    # Critical for WSL2 Mirrored Mode: Bind to all interfaces
    sock.bind(('', MCAST_PORT))

    # Join the multicast group
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Sending discovery to {MCAST_GRP}...")
    sock.sendto(msg, (MCAST_GRP, MCAST_PORT))

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            print(f"Received response from {addr}: {data.hex()}")
    except socket.timeout:
        print("No devices responded. Check Windows Firewall or WSL Routing.")

if __name__ == "__main__":
    test_multicast()