from util.classes import PingPong
from scapy.all import *
from scapy.layers.inet import IP, TCP

# TODO: Set up full TCP handshake
source_port = 9735
dest_port = 9735
ip_packet = IP(src="192.168.0.59", dst="88.99.209.230")
tcp_syn = TCP(sport=source_port, dport=dest_port, flags="S", seq=1000)
ping = PingPong()
synack = sr1(ip_packet / tcp_syn)
ack = TCP(sport=source_port, dport=dest_port, flags='A', seq=synack.ack + 1, ack=synack.seq + 1)
send(ip_packet / ack)
sr1(ip_packet/TCP/ping)
