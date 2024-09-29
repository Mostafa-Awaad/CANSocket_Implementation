import scapy
from scapy.all import load_layer, load_contrib
from scapy.all import rdpcap, wrpcap
from scapy.layers.can import CAN
from scapy.contrib.cansocket import CANSocket  # CANSocket from contrib
#from scapy.contrib.cansocket_python_can import CANSocket
from scapy.contrib.cansocket import *
from scapy.contrib.cansocket_native import *
from scapy.all import AsyncSniffer

from scapy.all import *
#from scapy.layers.can import *
from scapy.config import *
from scapy.utils import *
from scapy.contrib import *

import os
import threading
import time
from time import sleep

from scapy.all import AsyncSniffer
from scapy.layers.can import CAN

# Function to handle sniffed packets
def handle_packet(pkt):
    print(f"Sniffed Packet: {pkt.summary()}")

# Integrating AsyncSniffer to sniff CAN FD and extended frames
def start_async_sniffer():
    sniffer = AsyncSniffer(
        iface="vcan1", 
        filter=lambda pkt: isinstance(pkt, CAN) and pkt.flags == 'fd', 
        prn=handle_packet,
        timeout=5  # Sniff for 5 seconds
    )
    sniffer.start()  # Start sniffing asynchronously

# Update the sending function for CAN FD and extended frames
def sendPacketFD():
    sleep(0.2)
    socket0.send(CAN(flags='fd', identifier=0x10010000, length=64, data=b'\x01'*64))  # CAN FD with 64 bytes

socket0 = CANSocket(channel='vcan0')
socket1 = CANSocket(channel='vcan1')
# Start sniffing and sending CAN FD packets
threadSenderFD = threading.Thread(target=sendPacketFD)
threadSniffer = threading.Thread(target=start_async_sniffer)

# Start both threads
threadSniffer.start()
threadSenderFD.start()

# Join threads to wait for completion
threadSniffer.join()
threadSenderFD.join()
