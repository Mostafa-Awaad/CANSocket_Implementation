import psycopg2
import binascii  # for hex to binary conversion

# parsing the asc file into parts to make it easy to access the desired data
def parse_asc_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    log_data = []

    for line in lines:
        parts = line.split()

        if len(parts) < 10:
            continue  # Skip invalid lines
        
        message_number = parts[0]
        timestamp = float(parts[1])
        can_message_id = parts[3].strip()  # Strip any spaces
        
        # Ensure the can_message_id has even length by padding with a leading 0 if necessary
        if len(can_message_id) % 2 != 0:
            can_message_id = '0' + can_message_id

        signal_type = parts[4]
        data_frame = parts[7:]  # Data bytes
        
        # Convert can_message_id and data_frame to binary for BYTEA
        try:
            can_message_id_bin = binascii.unhexlify(can_message_id)  # Convert hex to binary
        except binascii.Error:
            print(f"Error converting CAN message ID: {can_message_id}")
            continue

        # Join data_frame bytes and remove any unwanted spaces, then convert to binary
        data_frame_cleaned = ''.join(byte.strip() for byte in data_frame)
        try:
            data_frame_bin = binascii.unhexlify(data_frame_cleaned)
        except binascii.Error:
            print(f"Error converting data frame: {data_frame_cleaned}")
            continue

        log_data.append({
            'message_number': message_number,
            'timestamp': timestamp,
            'can_message_id': can_message_id_bin,
            'data_frame': data_frame_bin,
            'signal_type': signal_type
        })
    
    return log_data

# Insert the parsed log_data into the created database
def insert_to_postgresql(log_data):
    conn = psycopg2.connect(
        dbname="car_log_db",
        user="postgres",  
        password="Mmk@3040112",  
        host="localhost"
    )
    cursor = conn.cursor()

    # Create a Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS car_logs(
                   message_number SERIAL PRIMARY KEY,
                   timestamp DOUBLE PRECISION,
                   can_message_id BYTEA,
                   data_frame BYTEA, 
                   signal_type VARCHAR(3)
                   );
                   ''')

    # Insert each log entry
    for log_entry in log_data:
        cursor.execute('''INSERT INTO car_logs (message_number, timestamp, can_message_id, data_frame, signal_type)
                          VALUES (%s, %s, %s, %s, %s)''', 
                          (log_entry['message_number'], log_entry['timestamp'], log_entry['can_message_id'], log_entry['data_frame'], log_entry['signal_type']))

    conn.commit()
    cursor.close()
    conn.close()

# Example usage
log_data = parse_asc_file('vehicle_speed_log.asc')
insert_to_postgresql(log_data)
