from util.classes import PingPong
from scapy.all import *
from scapy.layers.inet import IP, TCP

# TODO: Set up full TCP handshake
packets = IP(src="192.168.0.59", dst="203.132.95.10") / TCP(dport=9735, flags="S") / PingPong()
print(sr1(packets))
