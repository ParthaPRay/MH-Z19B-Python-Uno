import serial
import matplotlib.pyplot as plt
from collections import deque
import numpy as np  # Needed for percentile calculation
from datetime import datetime  # Import the datetime module

# Setup Serial Connection
ser = serial.Serial('/dev/ttyACM0', 115200)

# Variables
CO2_values = deque()  # Stores last 100 readings for visualization
time_values = deque()  # Stores timestamp

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(12, 7))
ax.set_title("Real-time CO2 Sensor Readings (ppm)", fontsize=16)
ax.set_xlabel("Time (Seconds)", fontsize=14)
ax.set_ylabel("CO2 (ppm)", fontsize=14)
colors = {"safe": "green", "moderate": "yellow", "high": "red"}
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.set_facecolor('#f5f5f5')  # Light gray background for better clarity

# Color Legend
ax.plot([], [], color=colors["safe"], label="Safe (< 800 ppm)", linewidth=2)
ax.plot([], [], color=colors["moderate"], label="Moderate (800-1200 ppm)", linewidth=2)
ax.plot([], [], color=colors["high"], label="High (> 1200 ppm)", linewidth=2)
ax.legend(loc="upper right", fontsize=12)

# Function to update plot
def update_plot():
    ax.clear()

    # Get the current date and time
    current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    ax.set_title(f"Real-time CO2 Sensor Readings (ppm) on {current_time}", fontsize=16)
    ax.set_xlabel("Time (Seconds)", fontsize=14)
    ax.set_ylabel("CO2 (ppm)", fontsize=14)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_facecolor('#f5f5f5')
    
    # Plot CO2 values
    ax.plot(time_values, CO2_values, marker='o', linestyle='-', linewidth=2, label="CO2")
    
    # Plot min, max, mean lines
    min_val = min(CO2_values)
    max_val = max(CO2_values)
    mean_val = sum(CO2_values) / len(CO2_values)
    ax.axhline(y=min_val, color='blue', linestyle='-', label="Min")
    ax.axhline(y=max_val, color='red', linestyle='-', label="Max")
    ax.axhline(y=mean_val, color='gray', linestyle='-', label="Mean")
    
    # Plot 25% and 75% quartiles
    q25 = np.percentile(CO2_values, 25)
    q75 = np.percentile(CO2_values, 75)
    ax.axhline(y=q25, color='purple', linestyle=':', label="25% Quartile")
    ax.axhline(y=q75, color='orange', linestyle=':', label="75% Quartile")

    for i, val in enumerate(CO2_values):
        if val < 800:
            color = colors["safe"]
        elif 800 <= val <= 1200:
            color = colors["moderate"]
        else:
            color = colors["high"]
        ax.scatter(time_values[i], val, color=color, s=50)  # s is size of the marker
    
    ax.legend(loc="upper right", fontsize=12)
    plt.pause(0.05)

# Infinite loop to continuously read from Arduino
try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("CO2:"):
            value = int(line.split("CO2:")[1].strip())
            CO2_values.append(value)
            time_values.append(len(CO2_values))
            update_plot()
except KeyboardInterrupt:
    print("Stopped.")
finally:
    ser.close()
    plt.show(block=True)
