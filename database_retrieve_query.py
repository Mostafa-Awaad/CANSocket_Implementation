import psycopg2
import binascii
def retrieve_from_postgresql():
    conn = psycopg2.connect(
        dbname="car_log_db",
        user="postgres",  
        password="Mmk@3040112",  
        host="localhost"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT message_number, timestamp, can_message_id, data_frame, signal_type FROM car_logs")
    rows = cursor.fetchall()

    for row in rows:
        message_number = row[0]
        timestamp = row[1]
        can_message_id = binascii.hexlify(row[2]).decode('utf-8').upper()  # Convert binary back to hex
        data_frame = binascii.hexlify(row[3]).decode('utf-8').upper()  # Convert binary back to hex
        signal_type = row[4]
        
        print(f"Message Number: {message_number}, Timestamp: {timestamp}, CAN Message ID: {can_message_id}, Data Frame: {data_frame}, Signal Type: {signal_type}")

    cursor.close()
    conn.close()

# Example usage
retrieve_from_postgresql()
