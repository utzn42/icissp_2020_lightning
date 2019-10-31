import argparse

from netaddr import IPNetwork
from scapy.layers.inet import IP, TCP
from requests import get
from scapy.sendrecv import sr1, send

from util.classes import PingPong

# Parse command line arguments.
parser = argparse.ArgumentParser(
    description="Takes in an IP range and returns the IP address of Lightning nodes within that range.")
parser.add_argument("ip_range", type=str, help='IP range to be probed', default="192.168.0.0/24")
args = parser.parse_args()

src = get('https://api.ipify.org').text
sport = dport = 9735

for ip in IPNetwork(args.ip_range):
    dst = ip

    # SYN
    ip = IP(src=src, dst=dst)
    SYN = TCP(sport=sport, dport=dport, flags='S', seq=1000)
    SYNACK = sr1(ip / SYN)

    # ACK
    ACK = TCP(sport=sport, dport=dport, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
    send(ip / ACK / PingPong())
