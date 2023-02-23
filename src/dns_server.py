# Import modules
import socket
import struct

import dnslib
import pymongo

from src.change_dns_address import change_dns
from src.contants import MONGO_URL
from src.fs import write_unknown_url


# Define a function to parse DNS queries
def parse_query(data):
    return str(dnslib.DNSRecord.parse(data).q.qname)[:-1], dnslib.DNSRecord.parse(data).q.qtype


def get_all_malicious_urls():
    client = pymongo.MongoClient(MONGO_URL)
    return list(map(lambda obj: obj["url"], client.test.urls.find()))


# Define a function to build DNS responses
def build_response(qname, qtype, rcode):
    # Create a response header with ID, QR, OPCODE, AA, TC, RD, RA, Z, RCODE fields
    # ID is copied from query, QR is 1 (response), OPCODE is 0 (standard query)
    # AA is 0 (not authoritative), TC is 0 (not truncated), RD is 1 (recursion desired)
    # RA is 1 (recursion available), Z is 0 (reserved), RCODE is given as parameter
    header = struct.pack(">HBBHHHH", 1, 129 + rcode, 0, 1, rcode, 0, 0)

    # Create a response question section with QNAME, QTYPE and QCLASS fields
    # QNAME is encoded as labels separated by length octets
    # QTYPE and QCLASS are copied from query (QTYPE is given as parameter)
    question = b""
    for label in qname.split("."):
        question += struct.pack("B", len(label)) + label.encode("utf-8")
    question += b"\x00" + struct.pack(">HH", qtype, 1)

    return header + question


def launch_dns():
    change_dns("8.8.8.8")
    malicious_url_list = get_all_malicious_urls()
    # Create a UDP socket with localhost address and port 53
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", 53))

    # Start listening for incoming queries
    while True:
        # Receive data from client and get client address
        data, addr = sock.recvfrom(512)
        # Parse the query name and type from data
        qname, qtype = parse_query(data)
        # print(f"Received query for {qname} with type {qtype}")
        print(qname)
        # Check if the query name is in lambda
        if qname in malicious_url_list:
            print("REFUSED")
            # Send an error response with RCODE 3 (Name Error)
            rcode = 3
            response = build_response(qname, qtype, rcode)
            sock.sendto(response, addr)
            print(f"Sent error response with RCODE {rcode}")
            continue
        else:
            print("OK")
            write_unknown_url(qname)
            # Forward the request to Google DNS servers (8.8.8.8 or 8.8.4.4)
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            proxy_sock.sendto(data, ("8.8.8.8", 53))
            proxy_data, proxy_addr = proxy_sock.recvfrom(512)
            proxy_sock.sendto(proxy_data, addr)

            print(f"Sent proxy response from {proxy_addr}")


if __name__ == "__main__":
    launch_dns()
