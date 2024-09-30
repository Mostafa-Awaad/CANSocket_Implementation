import scapy
from scapy.all import load_contrib, AsyncSniffer, conf
from scapy.layers.can import CAN
import can  # Import python-can for CANSocket interaction
from scapy.contrib.cansocket import CANSocket
import os
import threading
import time
from time import sleep

# Function to handle sniffed packets
def handle_packet(pkt):
    print(f"Sniffed Packet: {pkt.summary()}")

# Integrating AsyncSniffer to sniff CAN FD and extended frames
def start_async_sniffer():
    sniffer = AsyncSniffer(
        iface="vcan1", 
        filter=lambda pkt: isinstance(pkt, CAN) and pkt.dlc > 8,  # FD frames have more than 8 bytes
        prn=handle_packet,
        timeout=5  # Sniff for 5 seconds
    )
    sniffer.start()  # Start sniffing asynchronously
    sniffer.join()   # Wait for completion

# Start to Implement virtual CAN interfaces
bashCommand = "/bin/bash -c 'sudo modprobe vcan; sudo ip link add name vcan0 type vcan; sudo ip link add name vcan1 type vcan; sudo ip link set dev vcan0 up; sudo ip link set dev vcan1 up'"
os.system(bashCommand)

# Set environment variables to use python-can with CAN FD and extended frames
os.environ["CAN_INTERFACE"] = "socketcan"
os.environ["CAN_CONFIG"] = '{"receive_own_messages": true, "fd": true}'

# Configuring Scapy to use python-can CANSocket
conf.contribs['CANSocket'] = {'use-python-can': True}
load_contrib('cansocket')

# Create CANSocket instances for virtual CAN interfaces
socket0 = CANSocket(bustype='socketcan', channel='vcan0', bitrate=500000)  # Set bitrate to 500 kbps for FD support
socket1 = CANSocket(bustype='socketcan', channel='vcan1', bitrate=500000)

# Update the sending function using environment variables
def sendPacketFD():
    sleep(0.2)
    try:
        # Sending a CAN FD frame (no flags needed, environment variables handle FD support)
        frame = CAN(identifier=0x155C755D, length=64, data=b'\x01'*64)  # CAN FD extended frame
        socket0.send(frame)
        print("Packet sent successfully.")
    except Exception as e:
        print(f"Error sending packet: {e}")

# Start sniffing and sending CAN FD packets using threads
threadSenderFD = threading.Thread(target=sendPacketFD)
threadSniffer = threading.Thread(target=start_async_sniffer)

# Start both threads
threadSniffer.start()
threadSenderFD.start()

# Join threads to wait for completion
threadSniffer.join()
threadSenderFD.join()
