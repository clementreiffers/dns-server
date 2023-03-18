# Import modules
import socket
import struct

import dnslib

from constants import GOOGLE_DNS
from fs import write_unknown_url, set_state_dns_listening
from mongo import get_all_malicious_urls


# Define a function to parse DNS queries
def parse_query(data):
    return str(dnslib.DNSRecord.parse(data).q.qname)[:-1], dnslib.DNSRecord.parse(data).q.qtype


# Define a function to build DNS responses
def build_response(qname, qtype, rcode):
    header = struct.pack(">HBBHHHH", 1, 129 + rcode, 0, 1, rcode, 0, 0)
    question = b""
    for label in qname.split("."):
        question += struct.pack("B", len(label)) + label.encode("utf-8")
    question += b"\x00" + struct.pack(">HH", qtype, 1)
    return header + question


def send_response_to_client(data, addr):
    # Forward the request to Google DNS servers (8.8.8.8 or 8.8.4.4)
    proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    proxy_sock.sendto(data, (GOOGLE_DNS, 53))
    # send google response to the client
    proxy_data, proxy_addr = proxy_sock.recvfrom(512)
    proxy_sock.sendto(proxy_data, addr)


def launch_dns():
    malicious_url_list = get_all_malicious_urls()
    # Create a UDP socket with localhost address and port 53
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", 53))

    set_state_dns_listening(True)

    print("dns listening...")
    # Start listening for incoming queries
    while True:
        # Receive data from client and get client address
        data, addr = sock.recvfrom(512)
        # Parse the query name and type from data
        qname, qtype = parse_query(data)
        print(qtype)
        # print(f"Received query for {qname} with type {qtype}")
        # Check if the query name is in lambda
        if qname in malicious_url_list:
            print(f"{qname} REFUSED")
            continue
            id, flags, qdcount, ancount, nscount, arcount = struct.unpack("!HHHHHH", data[:12])
            # Check if it is a standard query for A record
            # Pack the response header with same id and QR=1, AA=1, RA=1 flags
            header = struct.pack("!HHHHHH", id, 0x8500, qdcount, 1, 0, 0)
            # Pack the answer section with name pointer to query name and A record with TTL=60 and google_ip
            answer = struct.pack("!HHHLH4s", 0xC00C, 1, 1, 60, 4, socket.inet_aton("104.18.34.67"))
            # Send the response back to the client
            sock.sendto(header + data[12:] + answer, addr)
            continue
        else:
            print(f"{qname} OK")
            write_unknown_url(qname)
            send_response_to_client(data, addr)


if __name__ == "__main__":
    launch_dns()
