import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import threading

# Function to fetch vehicle speed data from the Flask server
def fetch_vehicle_speed():
    try:
        response = requests.get("http://0.0.0.0:5000/vehicle_speed")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Function to update the GUI asynchronously
def update_gui():
    threading.Thread(target=update_speed_data).start()
    root.after(1000, update_gui)  # Update every second

# Function to update the speed and image based on fetched data
def update_speed_data():
    data = fetch_vehicle_speed()
    
    if data:
        if not hasattr(update_speed_data, "index"):
            update_speed_data.index = 0

        if update_speed_data.index >= len(data):
            update_speed_data.index = 0

        timestamp, speed = data[update_speed_data.index]
        speed_label.config(text=f"{speed} km/h")

        # Check speed and update image
        if speed > 210:
            speed_image_label.config(image=exceed_image_resized)
            #messagebox.showinfo("Speed Alert", f"Speed is {speed} km/h! Speed Limit is 210")
        else:
            speed_image_label.config(image=normal_image_resized) 

        update_speed_data.index += 1
    else:
        speed_label.config(text="No data available.")
        speed_image_label.config(image=normal_image)  # Reset to normal image if no data

# Tkinter GUI Setup
root = tk.Tk()
root.title("Futuristic Vehicle Speed Monitor")
root.geometry("600x600")
root.configure(bg="#1C1C1C")
image_width, image_height = 500, 300 # Set desired dimensions
# Load images
normal_image = Image.open("normal_speed.jpg")  # Image for normal speed
#normal_image = ImageTk.PhotoImage(normal_image)
normal_image_resized = normal_image.resize((image_width, image_height), Image.Resampling.LANCZOS)
normal_image_resized = ImageTk.PhotoImage(normal_image_resized)

exceed_image = Image.open("exceed_image.jpg")  # Image for speed exceeded
#exceed_image = ImageTk.PhotoImage(exceed_image)
exceed_image_resized = exceed_image.resize((image_width, image_height), Image.Resampling.LANCZOS)
exceed_image_resized = ImageTk.PhotoImage(exceed_image_resized)

# Speed Label with digital style
speed_label = tk.Label(root, text="Fetching...", font=("DS-Digital", 48), bg="#1C1C1C", fg="#00FF00")
speed_label.pack(pady=20)

# Image Label to display speed status images
speed_image_label = tk.Label(root, image=normal_image_resized)
speed_image_label.pack(pady=20)

# Start the update loop
update_gui()

# Run the Tkinter event loop
root.mainloop()
