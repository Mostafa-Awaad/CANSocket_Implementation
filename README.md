[![Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)](https://www.python.org)
[![CAN Socket](https://img.shields.io/badge/Protocol-CAN%20Socket-00A9E0?logo=can&logoColor=white)](https://en.wikipedia.org/wiki/Controller_area_network)
[![CAN FD](https://img.shields.io/badge/Protocol-CAN%20FD-00A9E0?logo=can&logoColor=white)](https://en.wikipedia.org/wiki/Controller_area_network#CAN_FD)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)](https://postgresql.org)
[![CAN DBC](https://img.shields.io/badge/Database-CAN_DBC-lightgrey?logo=database&logoColor=blue)](https://www.w3schools.com/sql/)

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
- [Usage](#-usage)
- [Output](#-output)

### 🚘 About
The application displays vehicle signals after being parsed from the asc file to the PostgreSQL-based database in tkinter-based GUI.

---
### ✨ Features

   
- **Backend Python Script**:
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

  - Converts the DBC data into an **ASC (ASCII log)** file containing continuously generated rows of data.
  - Automatically uploads the parsed data from the ASC file to a **Supabase database table** in real-time.



---
### 🔗 Workflow
1. **Data Processing**:
   - A Python script decodes vehicle data using a **DBC file** and generates an **ASC file** with continuous vehicle signal data.

2. **Data Storage**:
  
     ![image](https://github.com/user-attachments/assets/570afd29-4497-4fed-aa04-e9dafaec141b)

3. **Display**:
   - The Flutter application fetches the **latest row** from the Supabase table.
   - Displays the corresponding signals dynamically using **gauges** for an engaging and informative user.
       <p align="center">
        <img src="https://github.com/Mostafa-Awaad/CANSocket_Implementation/blob/main/GUI_Image3.JPG?raw=true" alt="Screenshot_1737551439" style="width: 70%; margin-right: 30px;" />
        
       </p>




---

### 🛠 Technology Stack
- **Frontend**: Flutter (Dart)
- **Backend**: Python
  - **Python Libraries**:
      ```
      - supabase,
      - cantools
      - binascii
      - base64
      - os
      - time
      - datetime
      - random
       ```
- **Database**: Supabase (PostgreSQL-based)
  - **Environment Variables For Security**:
     - `URL`: Supabase project URL.
     - `KEY`: Supabase project anon key.
- **Data Format**: DBC to ASC file conversion
  - **Files**:
     - `Custom_dbc2.dbc`: The DBC file containing CAN message definitions.
- **Communication**: Real-time database updates and streaming.

---

### 📱 Usage

1. **Setup Environment**:
   - Set `URL` and `KEY` environment variables for Supabase credentials.
2. **Run the Script**:
   - The script will:
     - Simulate CAN messages.
     - Log them into `vehicle_speed_log.asc`.
     - Parse the last logged message in the .asc file and store it in the Supabase database.
3. **Database Table**:
   - Ensure the Supabase table `car_logs_2` has the following schema:
     ```sql
     CREATE TABLE car_logs_2 (
         message_number TEXT,
         timestamp DOUBLE PRECISION,
         can_message_id BYTEA,
         data_frame BYTEA,
         signal_type TEXT
     );
     ```
---

### 📁 Output

- **ASC File**:
  - Example of logged data:
    ```
    1   1700000000.123456   1   123ABC   Tx -   8   01 02 03 04 05 06 07 08
    ```
- **Database Record**:
  - Example of inserted data:
    ```json
    {
        "message_number": "1",
        "timestamp": 1700000000.123456,
        "can_message_id": "Base64_encoded_binary_data",
        "data_frame": "Base64_encoded_binary_data",
        "signal_type": "Tx"
    }
    ```



---

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
