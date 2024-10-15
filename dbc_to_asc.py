import cantools
import random
import datetime
from datetime import datetime

# Load the DBC file
dbc = cantools.database.load_file('Custom_dbc2.dbc')

# Get the message by name
message = dbc.get_message_by_name('OBD2')

# Simulate vehicle speed data over time
vehicle_speed_values = [random.randint(0, 255) for _ in range(100)]        # Random speeds from 0 to 255 km/h
engine_coolant_temp = [random.randint(-40, 215) for _ in range(100)]       # Random coolant temp from 0 to 255 degC --> (scaling factor, offset)
                                                                           ######################################## --> (1, -40)
soh_percent = [random.randint(0, 100) for _ in range(100)]                 # Random percentage values for SOH_of battery
soc_percent = [random.randint(0, 100) for _ in range(100)]                 # Random percentage values for SOC_of battery  
Fuel_tank_level = [random.randint(0, 100) for _ in range(100)] 
New_distance_covered = [random.randint(0, 65535) for _ in range(100)] 
Engine_load = [random.randint(0, 100) for _ in range(100)]
timestamps = [datetime.now().timestamp() + i * 0.1 for i in range(100)]    # 100 messages, 0.1s interval

# Generate CAN messages and save to .asc file
with open('vehicle_speed_log.asc', 'w') as log_file:
    log_file.write("date {}\n".format(datetime.now().strftime('%a %b %d %H:%M:%S.%f %Y')))
    log_file.write("Begin Triggerblock\n")

    for i, (speed, 
            coolant_temp, 
            soh_per, 
            soc_per, 
            fuel_level, 
            new_distance, 
            eng_load) in enumerate(zip(vehicle_speed_values,
                                       engine_coolant_temp,
                                       soh_percent, soc_percent, 
                                       Fuel_tank_level,
                                       New_distance_covered,
                                       Engine_load)):
        # Ensure the signal name is correct
        try:
            encoded_message = message.encode({'S01PID0D_VehicleSpeed': speed,
                                              'S01PID05_EngineCoolantTemp': coolant_temp,
                                              'S01PID4D_BatterySOH': soh_per, 
                                              'S01PID4E_BatterySOC': soc_per,
                                              'S01PID2F_FuelTankLevel' : fuel_level,
                                              'S01PID21_DistanceMILOn' : new_distance,
                                              'S01PID04_CalcEngineLoad': eng_load})
            timestamp = timestamps[i]
            log_file.write(f"{i+1}\t {timestamp}\t1\t {message.frame_id:X}\t Tx -\t {len(encoded_message)}\t {'\t'.join(f'{b:02X}' for b in encoded_message)}\n")
        except cantools.database.errors.EncodeError as e:
            print(f"Error encoding message at index {i}: {e}")  # Handle encoding errors

    log_file.write("End TriggerBlock\n")

print("ASC file created: log_file.asc")
