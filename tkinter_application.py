import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import threading

# Function to fetch vehicle speed and engine coolant temp data from the Flask server
def fetch_car_data():
    try:
        response = requests.get("http://192.168.25.53:5000/car_dashboard_data")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}

# Function to update the GUI asynchronously
def update_gui():
    threading.Thread(target=update_car_data).start()
    root.after(1000, update_gui)  # Update every second

# Function to update the speed and engine coolant temp based on fetched data
def update_car_data():
    data = fetch_car_data()
    
    if data:
        # Vehicle speed data
        vehicle_speed_data = data.get('vehicle_speed', [])
        engine_coolant_temp_data = data.get('engine_coolant_temp', [])
        battery_soh_data = data.get('battery_soh_percnet', [])

        if not hasattr(update_car_data, "index"):
            update_car_data.index = 0

        if update_car_data.index >= len(vehicle_speed_data):
            update_car_data.index = 0

        # Get the current vehicle speed and engine coolant temperature
        timestamp, speed = vehicle_speed_data[update_car_data.index]
        _, coolant_temp = engine_coolant_temp_data[update_car_data.index]
        _, battery_soh = battery_soh_data[update_car_data.index]

        # Update vehicle speed label and image
        if speed > 210:
            speed_label.config(text=f"High Speed: {speed} km/h")
            speed_image_label.config(image=exceed_image_resized)
        else:
            speed_label.config(text=f"Normal Speed: {speed} km/h")
            speed_image_label.config(image=normal_image_resized)

        # Update engine coolant temp label
        coolant_temp_label.config(text=f"Coolant Temp: {coolant_temp - 40} °C")

        battery_soh_label.config(text=f"SOH: {round (battery_soh * 0.392156862745098, 2)} %")
        
        update_car_data.index += 1
    else:
        speed_label.config(text="No data available.")
        coolant_temp_label.config(text="No data available.")
        battery_soh_label.config(text="No data available.")
        speed_image_label.config(image=normal_image_resized)  # Reset to normal image if no data

# Tkinter GUI Setup
root = tk.Tk()
root.title("Futuristic Vehicle Dashboard")
root.geometry("600x600")
root.configure(bg="#1C1C1C")
image_width, image_height = 500, 300  # Set desired dimensions

# Load images
normal_image = Image.open("normal_speed.jpg")  # Image for normal speed
normal_image_resized = normal_image.resize((image_width, image_height), Image.Resampling.LANCZOS)
normal_image_resized = ImageTk.PhotoImage(normal_image_resized)

exceed_image = Image.open("exceed_image.jpg")  # Image for speed exceeded
exceed_image_resized = exceed_image.resize((image_width, image_height), Image.Resampling.LANCZOS)
exceed_image_resized = ImageTk.PhotoImage(exceed_image_resized)

# Vehicle speed label with digital style
speed_label = tk.Label(root, text="Fetching...", font=("DS-Digital", 40), bg="#1C1C1C", fg="#00FF00")
speed_label.pack(pady=20)

# Coolant temperature label
coolant_temp_label = tk.Label(root, text="Fetching...", font=("DS-Digital", 40), bg="#1C1C1C", fg="#FF4500")
coolant_temp_label.pack(pady=20)

# battery_soh_percentage label
battery_soh_label = tk.Label(root, text="Fetching...", font=("DS-Digital", 40), bg="#1C1C1C", fg="#FF4500")
battery_soh_label.pack(side="left", padx=5, pady=20)

# Image label to display speed status images
speed_image_label = tk.Label(root, image=normal_image_resized)
speed_image_label.pack(pady=20)

# Start the update loop
update_gui()

# Run the Tkinter event loop
root.mainloop()