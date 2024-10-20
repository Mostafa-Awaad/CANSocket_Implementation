import tkinter as tk
from tkinter import ttk, PhotoImage, Canvas
from tkinter import *
from tkinter import PhotoImage, Canvas
from PIL import Image, ImageTk
import requests

import threading

# Function to fetch vehicle speed, engine coolant temp, battery SOH, and other data from the Flask server
def fetch_car_data():
    # Attempt to fetch car data from the server
    try:
        # Send a GET request to the provided URL to fetch car dashboard data
        response = requests.get("http://192.168.0.121:5000/car_dashboard_data")

        # Check if the request was successful (status code 200 means success)
        if response.status_code == 200:
            # If successful, return the data in JSON format
            return response.json()
        else:
            # If the status code is not 200, print an error message with the received status code
            print(f"Error: Received status code {response.status_code}")
            return {}
    
    # Catch any exceptions related to the request (e.g., connection errors, timeouts)
    except requests.exceptions.RequestException as e:
        # Print an error message with the exception details
        print(f"Error fetching data: {e}")
        return {}


# Function to update the GUI asynchronously
def update_gui():
    threading.Thread(target=update_car_data).start()
    root.after(1000, update_gui)

# Function to update speed, engine coolant temp, battery SOH, and other signals based on fetched data
def update_car_data():
    # Fetch the car data from the API
    data = fetch_car_data()

    # If valid data is returned from the API, update the dashboard
    if data:
        # Extract vehicle signals from the data dictionary
        vehicle_speed_data = data.get('vehicle_speed', [])
        engine_coolant_temp_data = data.get('engine_coolant_temp', [])
        battery_soh_data = data.get('battery_soh_percnet', [])
        battery_soc_data = data.get('battery_soc_percent', [])
        fuel_tank_level_data = data.get('fuel_tank_level_percent', [])
        distance_covered_data = data.get('distance_covered_km', [])
        engine_load_data = data.get('engine_load_percent', [])

        # Initialize an index attribute for the function if it doesn't exist yet
        if not hasattr(update_car_data, "index"):
            update_car_data.index = 0

        # Reset index if it exceeds the length of the vehicle speed data (loop back)
        if update_car_data.index >= len(vehicle_speed_data):
            update_car_data.index = 0

        # Update Vehicle Speed
        _, speed = vehicle_speed_data[update_car_data.index]
        speed_label.config(text=f"Vehicle Speed:\n{speed} km/h", fg="red" if speed > 210 else "green")  # Set speed text and color
        speed_bg_label.config(image=speed_alert_resized if speed > 210 else speed_bg_resized)  # Change background based on speed

        # Update Battery SOH (State of Health)
        _, battery_soh = battery_soh_data[update_car_data.index]
        battery_soh_label.config(text=f"SOH:\n{round(battery_soh, 2)}%", fg="red" if battery_soh < 70 else "green")  # Set SOH text and color
        soh_bg_label.config(image=soh_alert_resized if battery_soh < 70 else soh_bg_resized)  # Change background based on SOH

        # Update Engine Coolant Temperature
        _, coolant_temp = engine_coolant_temp_data[update_car_data.index]
        coolant_temp_label.config(text=f"Coolant Temp:\n{coolant_temp - 40} °C", fg="red" if coolant_temp - 40 > 120 else "blue")  # Adjust temp and color
        coolant_bg_label.config(image=coolant_alert_resized if coolant_temp - 40 > 120 else coolant_bg_resized)  # Change background based on temp

        # Update Battery SOC (State of Charge)
        _, battery_soc = battery_soc_data[update_car_data.index]
        battery_soc_label.config(text=f"SOC:\n{round(battery_soc, 2)}%" , fg="red" if battery_soh < 30 else "green")  # Set SOC text
        soc_bg_label.config(image=soc_alert_resized if battery_soc < 30 else soc_bg_resized)  # Change background based on SOC level

        # Update Fuel Tank Level
        _, fuel_tank_level = fuel_tank_level_data[update_car_data.index]
        fuel_tank_level_label.config(text=f"Fuel:\n{round(fuel_tank_level, 2)}%" , fg="red" if battery_soh < 30 else "green")  # Set fuel tank level text
        fuel_bg_label.config(image=fuel_alert_resized if fuel_tank_level < 30 else fuel_bg_resized)  # Change background based on fuel level

        # Update Distance Covered
        _, distance_covered = distance_covered_data[update_car_data.index]
        distance_covered_label.config(text=f"Distance:\n{round(distance_covered, 2)} km" , fg="red" if distance_covered > 65535 else "green")  # Set distance covered text
        distance_bg_label.config(image=distance_alert_resized if distance_covered > 65535 else distance_bg_resized)  # Background for large distances

        # Update Engine Load
        _, engine_load = engine_load_data[update_car_data.index]
        engine_load_label.config(text=f"Engine Load:\n{round(engine_load, 2)}%" , fg="red" if engine_load > 85 else "green")  # Set engine load text
        load_bg_label.config(image=load_alert_resized if engine_load > 85 else load_bg_resized)  # Background for high engine load

        # Increment the index to display the next data point in the next update
        update_car_data.index += 1
    else:
        # If no data is available, display a default message in yellow across all fields
        speed_label.config(text="No data available.", fg="yellow")
        coolant_temp_label.config(text="No data available.", fg="yellow")
        battery_soh_label.config(text="No data available.", fg="yellow")
        battery_soc_label.config(text="No data available.", fg="yellow")
        fuel_tank_level_label.config(text="No data available.", fg="yellow")
        distance_covered_label.config(text="No data available.", fg="yellow")
        engine_load_label.config(text="No data available.", fg="yellow")


# Tkinter GUI Setup
root = tk.Tk()
root.title("Futuristic Vehicle Dashboard")
root.geometry("1200x600")
#root.configure(bg="#121212")

# Load background image
background_image = Image.open("futuristic_bg.jpg")
background_image_resized = background_image.resize((1600, 800), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image_resized)

# Set background image using a Label
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load images for dials
speed_bg = Image.open("normal_speed.jpg")
speed_bg_resized = speed_bg.resize((150, 150), Image.Resampling.LANCZOS)
speed_bg_resized = ImageTk.PhotoImage(speed_bg_resized)

speed_alert = Image.open("high_speed.jpg")
speed_alert_resized = speed_alert.resize((150, 150), Image.Resampling.LANCZOS)
speed_alert_resized = ImageTk.PhotoImage(speed_alert_resized)

coolant_bg = Image.open("low_coolant_temp.jpg")
coolant_bg_resized = coolant_bg.resize((150, 150), Image.Resampling.LANCZOS)
coolant_bg_resized = ImageTk.PhotoImage(coolant_bg_resized)

coolant_alert = Image.open("high_coolant_temp.png")
coolant_alert_resized = coolant_alert.resize((150, 150), Image.Resampling.LANCZOS)
coolant_alert_resized = ImageTk.PhotoImage(coolant_alert_resized)

soh_bg = Image.open("good_battery_health.png")
soh_bg_resized = soh_bg.resize((150, 150), Image.Resampling.LANCZOS)
soh_bg_resized = ImageTk.PhotoImage(soh_bg_resized)

soh_alert = Image.open("low_soh.png")
soh_alert_resized = soh_alert.resize((150, 150), Image.Resampling.LANCZOS)
soh_alert_resized = ImageTk.PhotoImage(soh_alert_resized)

soc_bg = Image.open("normal_soc.jpg")
soc_bg_resized = soc_bg.resize((150, 150), Image.Resampling.LANCZOS)
soc_bg_resized = ImageTk.PhotoImage(soc_bg_resized)

soc_alert = Image.open("low_soc.jpg")
soc_alert_resized = soc_alert.resize((150, 150), Image.Resampling.LANCZOS)
soc_alert_resized = ImageTk.PhotoImage(soc_alert_resized)

fuel_bg = Image.open("normal_fuel.jpg")
fuel_bg_resized = fuel_bg.resize((150, 150), Image.Resampling.LANCZOS)
fuel_bg_resized = ImageTk.PhotoImage(fuel_bg_resized)

fuel_alert = Image.open("low_fuel.jpg")
fuel_alert_resized = fuel_alert.resize((150, 150), Image.Resampling.LANCZOS)
fuel_alert_resized = ImageTk.PhotoImage(fuel_alert_resized)

load_bg = Image.open("normal_load.jpg")
load_bg_resized = load_bg.resize((150, 150), Image.Resampling.LANCZOS)
load_bg_resized = ImageTk.PhotoImage(load_bg_resized)

load_alert = Image.open("high_load.jpg")
load_alert_resized = load_alert.resize((150, 150), Image.Resampling.LANCZOS)
load_alert_resized = ImageTk.PhotoImage(load_alert_resized)

distance_bg = Image.open("car_insurance.png")
distance_bg_resized = distance_bg.resize((150, 150), Image.Resampling.LANCZOS)
distance_bg_resized = ImageTk.PhotoImage(distance_bg_resized)

distance_alert = Image.open("car_repair.png")
distance_alert_resized = distance_alert.resize((150, 150), Image.Resampling.LANCZOS)
distance_alert_resized = ImageTk.PhotoImage(distance_alert_resized)

# Configure grid layout for the root window
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure([0, 1, 2, 3, 4], weight=1)

# Dashboard Frames

# Configure grid layout for the root window
# This configures how rows and columns behave
root.grid_rowconfigure([0, 1], weight=1, uniform="row")  # Ensuring equal height for both rows
root.grid_columnconfigure([0, 1, 2, 3], weight=1, uniform="col")  # Ensuring equal width for columns

# Dashboard Frames

# Speed Frame - Row 0, Column 0
speed_frame = tk.Frame(root, bg="#1C1C1C")
speed_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')  # Adjusted for uniform grid placement

speed_bg_label = tk.Label(speed_frame, image=speed_bg_resized, bg="#1C1C1C")
speed_bg_label.pack()

speed_label = tk.Label(speed_frame, text="Speed: 0 km/h", font=("DS-Digital", 24), bg="#1C1C1C", fg="green")
speed_label.pack()

# Coolant Frame - Row 0, Column 1
coolant_frame = tk.Frame(root, bg="#1C1C1C")
coolant_frame.grid(row=0, column=1, padx=20, pady=20, sticky='nsew')

coolant_bg_label = tk.Label(coolant_frame, image=coolant_bg_resized, bg="#1C1C1C")
coolant_bg_label.pack()

coolant_temp_label = tk.Label(coolant_frame, text="Coolant_Temp: 0 °C", font=("DS-Digital", 24), bg="#1C1C1C", fg="blue")
coolant_temp_label.pack()

# SOH Frame - Row 0, Column 2
soh_frame = tk.Frame(root, bg="#1C1C1C")
soh_frame.grid(row=0, column=2, padx=20, pady=20, sticky='nsew')

soh_bg_label = tk.Label(soh_frame, image=soh_bg_resized, bg="#1C1C1C")
soh_bg_label.pack()

battery_soh_label = tk.Label(soh_frame, text="SOH: 0%", font=("DS-Digital", 24), bg="#1C1C1C", fg="green")
battery_soh_label.pack()

# SOC Frame - Row 0, Column 3
soc_frame = tk.Frame(root, bg="#1C1C1C")
soc_frame.grid(row=0, column=3, padx=20, pady=20, sticky='nsew')

soc_bg_label = tk.Label(soc_frame, image=soc_bg_resized, bg="#1C1C1C")
soc_bg_label.pack()

battery_soc_label = tk.Label(soc_frame, text="SOC: 0%", font=("DS-Digital", 24), bg="#1C1C1C", fg="green")
battery_soc_label.pack()

# Row 1 Frames

# Engine Load Frame - Row 1, Column 0
load_frame = tk.Frame(root, bg="#1C1C1C")
load_frame.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')

load_bg_label = tk.Label(load_frame, image=load_bg_resized, bg="#1C1C1C")
load_bg_label.pack()

engine_load_label = tk.Label(load_frame, text="Load: 0%", font=("DS-Digital", 24), bg="#1C1C1C", fg="green")
engine_load_label.pack()

# Fuel Tank Level Frame - Row 1, Column 1
fuel_frame = tk.Frame(root, bg="#1C1C1C")
fuel_frame.grid(row=1, column=1, padx=20, pady=20, sticky='nsew')

fuel_bg_label = tk.Label(fuel_frame, image=fuel_bg_resized, bg="#1C1C1C")
fuel_bg_label.pack()

fuel_tank_level_label = tk.Label(fuel_frame, text="Fuel: 0%", font=("DS-Digital", 24), bg="#1C1C1C", fg="green")
fuel_tank_level_label.pack()

# Distance Covered Frame - Row 1, Column 2
distance_frame = tk.Frame(root, bg="#1C1C1C")
distance_frame.grid(row=1, column=2, padx=20, pady=20, sticky='nsew')

distance_bg_label = tk.Label(distance_frame, image=distance_bg_resized, bg="#1C1C1C")
distance_bg_label.pack()

distance_covered_label = tk.Label(distance_frame, text="Distance: 0 km", font=("DS-Digital", 24), bg="#1C1C1C", fg="green")
distance_covered_label.pack()

# Start the update loop
update_gui()

# Run the Tkinter event loop
root.mainloop()