## 1. CAN Socket Implementation with Scapy and python-can

This repository contains a Python script `can_socket_implem.py` that integrates Scapy with `python-can` to simulate a virtual CAN (Controller Area Network) environment. The script demonstrates how to create virtual CAN interfaces, sniff CAN FD (Flexible Data-rate) frames, and send CAN FD packets with extended identifiers using virtual CAN sockets.

### Features

- **Virtual CAN Interface Setup**: Automatically creates virtual CAN interfaces (`vcan0` and `vcan1`).
- **CAN FD Frame Sniffing**: Utilizes Scapy's `AsyncSniffer` to capture CAN FD frames with data lengths greater than 8 bytes.
- **CAN FD Frame Sending**: Sends a CAN FD extended frame from `vcan0`.
- **Multithreading**: Runs sniffing and sending processes in parallel using Python's threading module.

---

### Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Virtual CAN Interface Setup](#virtual-can-interface-setup)
4. [CAN FD Sniffing](#can-fd-sniffing)
5. [CAN FD Frame Sending](#can-fd-frame-sending)
6. [Threading Implementation](#threading-implementation)
7. [Code Walkthrough](#code-walkthrough)
8. [License](#license)
9. [Resources](#resources)

---

### Installation

#### Prerequisites

To use this script, ensure you have the following installed:

- **Python 3.x**
- **Scapy**: Packet manipulation tool.
- **python-can**: Python library for interfacing with CAN sockets.
- **Linux**: The script requires a Linux environment with support for virtual CAN interfaces.

#### Install Required Python Libraries

Install the necessary Python libraries using `pip`:

`pip install scapy python-can`

---
### Usage
1. Run the script:
The script sets up virtual CAN interfaces and sniffs for CAN FD frames while sending test CAN FD frames.

2. Functionality:
The script will sniff CAN FD frames on `vcan1` and send CAN FD frames on `vcan0` using threads.

---
### Virtual CAN Interface Setup
The script automatically configures two virtual CAN interfaces, `vcan0` and `vcan1`, using the following Linux commands:
````
sudo modprobe vcan
sudo ip link add name vcan0 type vcan
sudo ip link add name vcan1 type vcan
sudo ip link set dev vcan0 up
sudo ip link set dev vcan1 up
````

This command is executed through the Python `os.system` method to set up the virtual interfaces.

---
### CAN FD Sniffing
The script uses Scapy's AsyncSniffer to capture CAN FD frames:

- **Interface:** `vcan1`
- **Filter:** Sniff only CAN FD frames with a Data Length Code (DLC) greater than 8 bytes (indicating FD frames).
``````
sniffer = AsyncSniffer(
    iface="vcan1", 
    filter=lambda pkt: isinstance(pkt, CAN) and pkt.dlc > 8,
    prn=handle_packet,
    timeout=5
)
``````
The captured packets are handled by the `handle_packet` function, which prints a summary of the packet.

---
### CAN FD Frame Sending
The script sends a CAN FD frame with the following properties:

- **Identifier:** Extended identifier 0x155C755D (29-bit).
- **Data Length:** 64 bytes (FD frame).
- **Data:** Filled with 64 bytes of 0x01.
  
``
frame = CAN(identifier=0x155C755D, length=64, data=b'\x01'*64)  # CAN FD extended frame
socket0.send(frame)
``
The frame is sent through `vcan0` using `python-can`'s CANSocket.

---
### Threading Implementation
The script runs the sniffing and sending processes in parallel using Python’s threading module. This allows the script to send CAN FD packets while simultaneously sniffing for incoming frames.

- **Sniffer Thread:** Handles the packet-sniffing process on `vcan1`.
- **Sender Thread:** Sends the CAN FD frame through `vcan0`.
```
threadSniffer = threading.Thread(target=start_async_sniffer)
threadSenderFD = threading.Thread(target=sendPacketFD)
threadSniffer.start()
threadSenderFD.start()
threadSniffer.join()
threadSenderFD.join()
```
---
### Code Walkthrough
### Imports
- **`scapy`:** For packet sniffing and manipulation.
- **`python-can`:** For CANSocket interaction.
- **`os`:** To run system commands and manage environment variables.
- **`threading`:** For multithreaded sniffing and sending of CAN frames.

#### Virtual CAN Interface Setup
The script uses a bash command to set up two virtual CAN interfaces, `vcan0` and `vcan1`, using the `vcan` kernel module.

#### CAN FD Sniffer
The sniffer captures CAN FD frames using Scapy’s AsyncSniffer, applying a filter to only sniff frames with a DLC greater than 8.

#### CAN FD Sender
The script sends a CAN FD extended frame from `vcan0`. The CAN FD frame is generated using Scapy’s `CAN` class.

#### Multithreading
Two threads are created to run the sniffer and sender functions concurrently. The threads are then joined to ensure the main process waits for both threads to complete before exiting.

---
## Tkinter-based application:
### Implementing flask server:

### Dealing with PostgreSQL Shell (psql)
### **Create a database for a CAN message**
- `CREATE DATABASE car_log_db`
### **Create a table for storing CAN signals**
- ```
  CREATE TABLE car_logs (
       message_number SERIAL PRIMARY KEY,
       timestamp DOUBLE PRECISION,
       can_message_id BYTEA, // use bytea data type to store CAN message ID in the format of binary strings in the database
       data BYTEA        // to store CAN data frame in the format of binary strings in the database
   );
  ```
### **Adding signal_type column**
- ```
  ALTER TABLE car_logs
  ADD signal_type VARCHAR(3);
  ```
---
### Resources: 
1. https://canlogger.csselectronics.com/canedge-getting-started/ce2/log-file-tools/?_gl=1*6ogs5b*_ga*NTgyMzA4Njg5LjE3Mjg5MDM4NDQ.*_ga_YS7M75XF5N*MTcyOTAwMjA5Ny42LjEuMTcyOTAwMzE1MS4wLjAuMA..
