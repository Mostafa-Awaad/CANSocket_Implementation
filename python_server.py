import threading
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Path to your CAN log file
asc_file_path = 'vehicle_speed_log.asc'


# Function to extract and decode vehicle speed from CAN log data
def extract_vehicle_speed():
    global vehicle_speed_data
    #Array to store vehicle speed
    vehicle_speed_data = []
    # Check if the file exists
    if not os.path.exists(asc_file_path):
        return []

    with open(asc_file_path, 'r') as file:
        can_log_content = file.readlines()

        for line in can_log_content:
            # Split the log line into its components
            parts = line.strip().split()
            # Check if the message ID is 7E8 and has 1 bytes of data
            if len(parts) >= 9 and parts[3] == '7E8':
                # Extract the 8th byte (hexadecimal) which represents the vehicle speed
                speed_hex = parts[14] # 8th byte corresponds to parts[14] in zero-indexed split
                # Convert hex to decimal (max 255 km/h)
                speed_kmh = int(speed_hex, 16)
                # Append timestamp and decoded speed (timestamp in parts[1])
                vehicle_speed_data.append((float(parts[1]), speed_kmh))
    return vehicle_speed_data


# Function to extract and decode engine coolant temperature from CAN log data
def extract_engine_coolant_temp():
    global engine_coolant_temp_data
    #Array to store Temperature of Engine coolant
    engine_coolant_temp_data = []
    if not os.path.exists(asc_file_path):
        return []

    with open(asc_file_path, 'r') as file:
        can_log_content = file.readlines()

        for line in can_log_content:
            parts = line.strip().split()
            if len(parts) >= 9 and parts[3] == '7E8':
                coolant_temp_hex = parts[13]
                coolant_temp_celcius = int(coolant_temp_hex, 16)
                engine_coolant_temp_data.append((float(parts[1]), coolant_temp_celcius))
    return engine_coolant_temp_data


# Function to extract and decode battery_SOH from CAN log data
def extract_battery_SOH():
    global battery_soh_data
    #Array to store Temperature of Engine coolant
    battery_soh_data = []
    if not os.path.exists(asc_file_path):
        return []

    with open(asc_file_path, 'r') as file:
        can_log_content = file.readlines()

        for line in can_log_content:
            parts = line.strip().split()
            if len(parts) >= 9 and parts[3] == '7E8':
                battery_soh_hex = parts[12]
                battery_soh_percent = int(battery_soh_hex, 16)
                battery_soh_data.append((float(parts[1]), battery_soh_percent))
    return battery_soh_data


# Load the extracted vehicle speed data
vehicle_speed_data = extract_vehicle_speed()

# Load the extracted engine coolant temperature data
engine_coolant_temp_data = extract_engine_coolant_temp()

battery_soh_data = extract_battery_SOH()

# Flask route to fetch data
@app.route('/car_dashboard_data', methods=['GET'])
def home():
    # Create and start threads for concurrent task execution
    thread1 = threading.Thread(target=extract_vehicle_speed)
    thread2 = threading.Thread(target=extract_engine_coolant_temp)
    thread3 = threading.Thread(target=extract_battery_SOH)

    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for both threads to complete
    thread1.join()
    thread2.join()
    thread3.join()

    # Return the combined data in JSON format
    return jsonify({
        'vehicle_speed': vehicle_speed_data,
        'engine_coolant_temp': engine_coolant_temp_data,
        'battery_soh_percnet': battery_soh_data
    })

if __name__ == '__main__':
    app.run(host='192.168.25.53', port=5000, debug=True)