# CAN Socket Implementation with Scapy and python-can

This repository contains a Python script `can_socket_implem.py` that integrates Scapy with `python-can` to simulate a virtual CAN (Controller Area Network) environment. The script demonstrates how to create virtual CAN interfaces, sniff CAN FD (Flexible Data-rate) frames, and send CAN FD packets with extended identifiers using virtual CAN sockets.

## Features

- **Virtual CAN Interface Setup**: Automatically creates virtual CAN interfaces (`vcan0` and `vcan1`).
- **CAN FD Frame Sniffing**: Utilizes Scapy's `AsyncSniffer` to capture CAN FD frames with data lengths greater than 8 bytes.
- **CAN FD Frame Sending**: Sends a CAN FD extended frame from `vcan0`.
- **Multithreading**: Runs sniffing and sending processes in parallel using Python's threading module.

---

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Virtual CAN Interface Setup](#virtual-can-interface-setup)
4. [CAN FD Sniffing](#can-fd-sniffing)
5. [CAN FD Frame Sending](#can-fd-frame-sending)
6. [Threading Implementation](#threading-implementation)
7. [Code Walkthrough](#code-walkthrough)
8. [License](#license)

---

## Installation

### Prerequisites

To use this script, ensure you have the following installed:

- **Python 3.x**
- **Scapy**: Packet manipulation tool.
- **python-can**: Python library for interfacing with CAN sockets.
- **Linux**: The script requires a Linux environment with support for virtual CAN interfaces.

### Install Required Python Libraries

Install the necessary Python libraries using `pip`:

```bash
pip install scapy python-can

### Resources: 
1. https://canlogger.csselectronics.com/canedge-getting-started/ce2/log-file-tools/?_gl=1*6ogs5b*_ga*NTgyMzA4Njg5LjE3Mjg5MDM4NDQ.*_ga_YS7M75XF5N*MTcyOTAwMjA5Ny42LjEuMTcyOTAwMzE1MS4wLjAuMA..
