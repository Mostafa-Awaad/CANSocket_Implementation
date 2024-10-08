import cantools
import random
import datetime
from datetime import datetime

# Load the DBC file
dbc = cantools.database.load_file('Custom_dbc2.dbc')

# Get the message by name
message = dbc.get_message_by_name('OBD2')

# Simulate vehicle speed data over time
vehicle_speed_values = [random.randint(0, 255) for _ in range(100)]  # Random speeds from 0 to 255 km/h
timestamps = [datetime.now().timestamp() + i * 0.1 for i in range(100)]  # 100 messages, 0.1s interval

# Generate CAN messages and save to .asc file
with open('vehicle_speed_log.asc', 'w') as log_file:
    log_file.write("date {}\n".format(datetime.now().strftime('%a %b %d %H:%M:%S.%f %Y')))
    log_file.write("Begin Triggerblock\n")

    for i, speed in enumerate(vehicle_speed_values):
        # Ensure the signal name is correct
        try:
            encoded_message = message.encode({'S01PID0D_VehicleSpeed': speed})
            timestamp = timestamps[i]
            log_file.write(f"{i+1}\t {timestamp}\t 1\t {message.frame_id:X}\t Tx -\t {len(encoded_message)}\t {'\t'.join(f'{b:02X}' for b in encoded_message)}\n")
        except cantools.database.errors.EncodeError as e:
            print(f"Error encoding message at index {i}: {e}")  # Handle encoding errors

    log_file.write("End TriggerBlock\n")

print("ASC file created: vehicle_speed_log.asc")
