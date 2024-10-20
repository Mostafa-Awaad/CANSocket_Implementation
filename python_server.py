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
                battery_soh_percent = int(battery_soh_hex, 16) * 0.392156862745098
                battery_soh_data.append((float(parts[1]), battery_soh_percent))
    return battery_soh_data

# Function to extract the state of charge (SOC) from the CAN log file.
def extract_battery_SOC():
    global battery_soc_data
    battery_soc_data = []
    if not os.path.exists(asc_file_path):
        return []
    
    with open(asc_file_path, 'r') as file:
        can_log_content = file.readlines()
        
        for line in can_log_content:
            parts = line.strip().split()
            if len(parts) >= 9 and parts[3] == '7E8':
                battery_soc_hex = parts[11]
                battery_soc_percent = int(battery_soc_hex, 16) * 0.392156862745098
                battery_soc_data.append((float(parts[1]), battery_soc_percent))
    return battery_soc_data

# Function to extract the fuel tank level from the CAN log file.
def extract_fuel_tank_level():
    global fuel_tank_level_data
    fuel_tank_level_data = []
    if not os.path.exists(asc_file_path):
        return []
    
    with open(asc_file_path, 'r') as file:
        can_log_content = file.readlines()
        
        for line in can_log_content:
            parts = line.strip().split()
            if len(parts) >= 9 and parts[3] == '7E8':
                fuel_level_hex = parts[10]  # Assuming the fuel tank level is in the 13th byte
                fuel_tank_percent = int(fuel_level_hex, 16) * 0.392156862745098
                fuel_tank_level_data.append((float(parts[1]), fuel_tank_percent))
    return fuel_tank_level_data

# Function to extract the distance the vehicle has covered.
def extract_distance_covered():
    global distance_covered_data
    distance_covered_data = []
    if not os.path.exists(asc_file_path):
        return []
    
    with open(asc_file_path, 'r') as file:
        can_log_content = file.readlines()
        
        for line in can_log_content:
            parts = line.strip().split()
            if len(parts) >= 9 and parts[3] == '7E8':
                distance_hex = parts[9]  # Assuming the distance is in the 14th byte
                distance_km = int(distance_hex, 16)   
                distance_covered_data.append((float(parts[1]), distance_km))
    return distance_covered_data

# Function to extract the engine load from the CAN log file.
def extract_engine_load():
    global engine_load_data
    engine_load_data = []
    if not os.path.exists(asc_file_path):
        return []
    
    with open(asc_file_path, 'r') as file:
        can_log_content = file.readlines()
        
        for line in can_log_content:
            parts = line.strip().split()
            if len(parts) >= 9 and parts[3] == '7E8':
                engine_load_hex = parts[7]  # Assuming engine load is in the 16th byte
                engine_load_percent = int(engine_load_hex, 16) * 0.392156862745098
                engine_load_data.append((float(parts[1]), engine_load_percent))
    return engine_load_data

# Load the extracted vehicle speed data
vehicle_speed_data = extract_vehicle_speed()

# Load the extracted engine coolant temperature data
engine_coolant_temp_data = extract_engine_coolant_temp()

battery_soh_data = extract_battery_SOH()
battery_soc_data = extract_battery_SOC()
fuel_tank_level_data = extract_fuel_tank_level()
distance_covered_data = extract_distance_covered()
engine_load_data = extract_engine_load()


# Flask route to fetch data
@app.route('/car_dashboard_data', methods=['GET'])
def home():
    # Create and start threads for concurrent task execution
    thread1 = threading.Thread(target=extract_vehicle_speed)
    thread2 = threading.Thread(target=extract_engine_coolant_temp)
    thread3 = threading.Thread(target=extract_battery_SOH)
    thread4 = threading.Thread(target=extract_battery_SOC)
    thread5 = threading.Thread(target=extract_fuel_tank_level)
    thread6 = threading.Thread(target=extract_distance_covered)
    thread7 = threading.Thread(target=extract_engine_load)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()

    # Wait for both threads to complete
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    thread7.join()

    # Return the combined data in JSON format
    return jsonify({
        'vehicle_speed': vehicle_speed_data,
        'engine_coolant_temp': engine_coolant_temp_data,
        'battery_soh_percnet': battery_soh_data,
        'battery_soc_percent': battery_soc_data,
        'fuel_tank_level_percent': fuel_tank_level_data,
        'distance_covered_km': distance_covered_data,
        'engine_load_percent': engine_load_data
    })

if __name__ == '__main__':
    app.run(host='192.168.25.76', port=5000, debug=True)