import tkinter as tk
from PIL import Image, ImageTk
import requests
import threading

# Function to fetch vehicle speed, engine coolant temp, battery SOH, and other data from the Flask server
def fetch_car_data():
    try:
        response = requests.get("http://192.168.0.121:5000/car_dashboard_data")
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
    root.after(1000, update_gui)

# Function to update speed, engine coolant temp, battery SOH, and other signals based on fetched data
def update_car_data():
    data = fetch_car_data()

    if data:
        vehicle_speed_data = data.get('vehicle_speed', [])
        engine_coolant_temp_data = data.get('engine_coolant_temp', [])
        battery_soh_data = data.get('battery_soh_percnet', [])
        battery_soc_data = data.get('battery_soc_percent', [])
        fuel_tank_level_data = data.get('fuel_tank_level_percent', [])
        distance_covered_data = data.get('distance_covered_km', [])
        engine_load_data = data.get('engine_load_percent', [])

        if not hasattr(update_car_data, "index"):
            update_car_data.index = 0

        if update_car_data.index >= len(vehicle_speed_data):
            update_car_data.index = 0

        # Vehicle Speed
        _, speed = vehicle_speed_data[update_car_data.index]
        speed_label.config(text=f"{speed} km/h", fg="red" if speed > 210 else "green")
        speed_bg_label.config(image=speed_alert_resized if speed > 210 else speed_bg_resized)

        # Battery SOH
        _, battery_soh = battery_soh_data[update_car_data.index]
        battery_soh_label.config(text=f"SOH: {round(battery_soh, 2)}%", fg="red" if battery_soh < 70 else "green")
        soh_bg_label.config(image=soh_alert_resized if battery_soh < 70 else soh_bg_resized)

        # Engine Coolant Temp
        _, coolant_temp = engine_coolant_temp_data[update_car_data.index]
        coolant_temp_label.config(text=f"{coolant_temp - 40} °C", fg="red" if coolant_temp - 40 > 120 else "blue")
        coolant_bg_label.config(image=coolant_alert_resized if coolant_temp - 40 > 120 else coolant_bg_resized)

        # Battery SOC
        _, battery_soc = battery_soc_data[update_car_data.index]
        battery_soc_label.config(text=f"SOC: {round(battery_soc, 2)}%")

        # Fuel Tank Level
        _, fuel_tank_level = fuel_tank_level_data[update_car_data.index]
        fuel_tank_level_label.config(text=f"Fuel: {round(fuel_tank_level, 2)}%")

        # Distance Covered
        _, distance_covered = distance_covered_data[update_car_data.index]
        distance_covered_label.config(text=f"Distance: {round(distance_covered, 2)} km")

        # Engine Load
        _, engine_load = engine_load_data[update_car_data.index]
        engine_load_label.config(text=f"Load: {round(engine_load, 2)}%")

        update_car_data.index += 1
    else:
        speed_label.config(text="No data available.", fg="yellow")
        coolant_temp_label.config(text="No data available.", fg="yellow")
        battery_soh_label.config(text="No data available.", fg="yellow")

# Tkinter GUI Setup
root = tk.Tk()
root.title("Futuristic Vehicle Dashboard")
root.geometry("1200x600")
root.configure(bg="#121212")

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

# Dashboard Frames
speed_frame = tk.Frame(root, bg="#1C1C1C")
speed_frame.grid(row=0, column=0, padx=40)

speed_bg_label = tk.Label(speed_frame, image=speed_bg_resized, bg="#1C1C1C")
speed_bg_label.pack()

speed_label = tk.Label(speed_frame, text="0 km/h", font=("DS-Digital", 35), bg="#1C1C1C", fg="green")
speed_label.pack()

coolant_frame = tk.Frame(root, bg="#1C1C1C")
coolant_frame.grid(row=0, column=1, padx=40)

coolant_bg_label = tk.Label(coolant_frame, image=coolant_bg_resized, bg="#1C1C1C")
coolant_bg_label.pack()

coolant_temp_label = tk.Label(coolant_frame, text="0 °C", font=("DS-Digital", 35), bg="#1C1C1C", fg="blue")
coolant_temp_label.pack()

soh_frame = tk.Frame(root, bg="#1C1C1C")
soh_frame.grid(row=0, column=2, padx=40)

soh_bg_label = tk.Label(soh_frame, image=soh_bg_resized, bg="#1C1C1C")
soh_bg_label.pack()

battery_soh_label = tk.Label(soh_frame, text="SOH: 0%", font=("DS-Digital", 35), bg="#1C1C1C", fg="green")
battery_soh_label.pack()

# New Frames for Additional Signals

# Battery SOC
soc_frame = tk.Frame(root, bg="#1C1C1C")
soc_frame.grid(row=1, column=0, padx=40)

battery_soc_label = tk.Label(soc_frame, text="SOC: 0%", font=("DS-Digital", 35), bg="#1C1C1C", fg="green")
battery_soc_label.pack()

# Fuel Tank Level
fuel_frame = tk.Frame(root, bg="#1C1C1C")
fuel_frame.grid(row=1, column=1, padx=40)

fuel_tank_level_label = tk.Label(fuel_frame, text="Fuel: 0%", font=("DS-Digital", 35), bg="#1C1C1C", fg="green")
fuel_tank_level_label.pack()

# Distance Covered
distance_frame = tk.Frame(root, bg="#1C1C1C")
distance_frame.grid(row=1, column=2, padx=40)

distance_covered_label = tk.Label(distance_frame, text="Distance: 0 km", font=("DS-Digital", 35), bg="#1C1C1C", fg="green")
distance_covered_label.pack()

# Engine Load
load_frame = tk.Frame(root, bg="#1C1C1C")
load_frame.grid(row=2, column=0, padx=40)

engine_load_label = tk.Label(load_frame, text="Load: 0%", font=("DS-Digital", 35), bg="#1C1C1C", fg="green")
engine_load_label.pack()

# Start the update loop
update_gui()

# Run the Tkinter event loop
root.mainloop()
