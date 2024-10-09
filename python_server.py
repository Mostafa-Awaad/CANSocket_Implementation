from flask import Flask, jsonify
import os

app = Flask(__name__)

# Path to your CAN log file
asc_file_path = 'vehicle_speed_log.asc'

# Function to extract and decode vehicle speed from CAN log data
def extract_vehicle_speed():
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
                # Extract the 5th byte (hexadecimal) which represents the vehicle speed
                speed_hex = parts[10]  # 5th byte corresponds to parts[7] in zero-indexed split
            
                # Convert hex to decimal (max 255 km/h)
                speed_kmh = int(speed_hex, 16)
                
                # Append timestamp and decoded speed (timestamp in parts[1])
                vehicle_speed_data.append((float(parts[1]), speed_kmh))

    return vehicle_speed_data

# Load the extracted vehicle speed data
vehicle_speed_data = extract_vehicle_speed()

@app.route('/vehicle_speed', methods=['GET'])
def get_vehicle_speed():
    return jsonify(vehicle_speed_data)

if __name__ == '__main__':
    # Change the host to '0.0.0.0' to allow access from any device on the network
    app.run(host='192.168.0.193', port=5000, debug=True)
