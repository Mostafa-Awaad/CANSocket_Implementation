[![Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)](https://www.python.org)
![Flask](https://img.shields.io/badge/-Flask-000000?style=flat&logo=flask&logoColor=white)&nbsp;
[![CAN Socket](https://img.shields.io/badge/Protocol-CAN%20Socket-00A9E0?logo=can&logoColor=white)](https://en.wikipedia.org/wiki/Controller_area_network)
[![CAN FD](https://img.shields.io/badge/Protocol-CAN%20FD-00A9E0?logo=can&logoColor=white)](https://en.wikipedia.org/wiki/Controller_area_network#CAN_FD)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://postgresql.org)
[![CAN DBC](https://img.shields.io/badge/Database-CAN_DBC-lightgrey?logo=database&logoColor=blue)](https://www.w3schools.com/sql/)

# Two projects 
1. [CAN Socket Implementation with Scapy and python-can](#1.-can-socket-implementation-with-scapy-and-python-can)
2. [Tkinter-based vehicle monitoring application](#2.-Tkinter-based-vehicle-monitoring-application:)
   
## 1. CAN Socket Implementation with Scapy and python-can:

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

#### 2. Virtual CAN Interface Setup
The script uses a bash command to set up two virtual CAN interfaces, `vcan0` and `vcan1`, using the `vcan` kernel module.

#### CAN FD Sniffer
The sniffer captures CAN FD frames using Scapy’s AsyncSniffer, applying a filter to only sniff frames with a DLC greater than 8.

#### CAN FD Sender
The script sends a CAN FD extended frame from `vcan0`. The CAN FD frame is generated using Scapy’s `CAN` class.

#### Multithreading
Two threads are created to run the sniffer and sender functions concurrently. The threads are then joined to ensure the main process waits for both threads to complete before exiting.

---
## 2. Tkinter-based vehicle monitoring application:

## Table of Contents
- [About](#-about)
- [Features](#-features)
- [Workflow](#-workflow)
- [Technology Stack](#-technology-stack)

### 🚘 About
The Tkinter-based vehicle monitoring application is a vehicle monitoring solution designed using Python for the user interface and for backend data processing. It provides an interactive dashboard that streams various car signals using dynamic gauges for each signal.

---
### ✨ Features

- **Tkinter application**:
  - Fetches vehicle speed, engine coolant temp, battery SOH, and other data from the Flask server.
  - Updates the GUI asynchronously.
  - Updates speed, engine coolant temp, battery SOH, and other signals and their descriptive images based on fetched data.
- **Python Script for creating ASC log file**:
  - Processes a **DBC (Database CAN)** file to decode CAN messages.
    ##### CAN DBC file (CAN Database) syntax:
      ```DBC
      BO_ 2024 OBD2: 8 Vector__XXX
     SG_ S01PID0D_VehicleSpeed m1 : 63|8@0+ (1,0) [0|255] "km/h" Vector__XXX
     ```
     | **Field**                      | **Description**                                                                                                    |
      |--------------------------------|--------------------------------------------------------------------------------------------------------------------|
      | **BO_**                        | Indicates message start (message syntax).                                                                          |
      | **2024**                       | CAN ID.                                                                                                            |
      | **OBD2**                       | Message name.                                                                                                      |
      | **8**                          | Length of message in data bytes.                                                                                   |
      | **Vector__XXX**                | Sender name.                                                                                                       |
      | **SG_**                        | Signal syntax.                                                                                                     |
      | **S01PID0D_VehicleSpeed**      | Signal name.                                                                                                       |
      | **m1**                         | Multiplexer name, where multiplexer (m1) allows multiple signals to be sent using the same message ID but differentiated based on their multiplexer value. |
      | **63**                         | Start bit of the corresponding signal.                                                                             |
      | **8**                          | Length of signal in bits.                                                                                          |
      | **@0**                         | Little-endian byte ordering, where the least significant bit is stored first.                                      |
      | **(1,0)**                      | (Scale, Offset).                                                                                                   |
      | **[0,255]**                    | Signal minimum and maximum values.                                                                                 |
      | **km/h**                       | Measuring unit.                                                                                                    |
      | **Vector__XXX**                | Receiver name.                                                                                                     |

  - Converts the DBC data into an **ASC (ASCII log)** file based on generated random data (100 values for each signal) .

- **Python Flask-based Server**:
  - Contains set of functions, which is resposible for:
    - Extracting the desired signal like vehicle speed.
    - Processing the signal value depending on its scale & offset in the DBC file.
  - Handles each different signal type in its own thread and sending over the flask server.


---
### 🔗 Workflow
1. **Data Processing**:
   - A Python script decodes vehicle data using a **DBC file** and generates an **ASC file** with 100 random signal values for each signal type.

2. **Data extracing and sending**:
      - Vehicle data is extracted using different functions, each function is responsible for extracting specific signal
      - Each extracted signal is handled in its own thread.
      - The extracted data is jsonified and sent over a flask server.

3. **Display**:
   - The Tkinter application fetches the latest vehicle data sent from the flask server.
   - The data is updated corresponding to the current index.
   - The GUI is updated every 1 second.
   - Displays the corresponding signals in different windows for each signal with descriptive images for each state.
       <p align="center">
        <img src="https://github.com/Mostafa-Awaad/CANSocket_Implementation/blob/main/GUI_Image3.JPG?raw=true" alt="Screenshot_1737551439" style="width: 70%; margin-right: 30px;" />
        
       </p>




---

### 🛠 Technology Stack
- Python.
- Flask.
- CAN DBC.
- CAN FD.
---
### Resources: 
1. https://canlogger.csselectronics.com/canedge-getting-started/ce2/log-file-tools/?_gl=1*6ogs5b*_ga*NTgyMzA4Njg5LjE3Mjg5MDM4NDQ.*_ga_YS7M75XF5N*MTcyOTAwMjA5Ny42LjEuMTcyOTAwMzE1MS4wLjAuMA..
