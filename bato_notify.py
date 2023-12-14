from notifypy import Notify
from PIL import Image, ImageColor
import psutil
import arrow
import os
import csv
import pandas as pd
import time




"""
File Handler
Notificaiton Handler
Main Script Runner
Data Visualization
Data Processing
Data Handler (retival, writting)
"""





battery = psutil.sensors_battery()
csv_file = 'data.csv'
power = battery.power_plugged
lvl = battery.percent

def current_battery():
    global battery, lvl, power
    battery = psutil.sensors_battery()
    power = battery.power_plugged
    lvl = battery.percent

# generate icon for notification
def get_icon():
    color = ImageColor.getrgb(f"hsl({int(120 * (lvl / 100))}, 100%, 50%)")
    image = Image.new('RGB', (64, 64), color) 
    icon_path = 'notification_icon.png'
    image.save(icon_path)
    return icon_path

# Get the time now in year-month-day hour:minutes:seconds format
def timestamp():
    return arrow.now().format("YYYY-MM-DD HH:mm:ss")

# Check if file exists 
def file_exists_and_not_empty(csv_file):
    return os.path.isfile(csv_file) and os.path.getsize(csv_file) > 0


# Recored data about battery level and status
def write_csv():
    # if file does not exist, create file 
    if not file_exists_and_not_empty(csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Timestamp', 'Level', 'Status'])  # Write header row
    
    # write the current battery data to file
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([timestamp(), f"{lvl:016.12f}", status()])

# Get the last data recorded
def get_latest_data(csv_file, n=1):
    df = pd.read_csv(csv_file, header=None)
    return df.tail(n)

def status():
    return 'Charging' if power else 'Discharging'

# Send a notification to the desktop
def message():
    notice = Notify()
    notice.icon = get_icon()
    notice.title = f"Battery {status()}"
    notice.message = f"Level: {int(lvl)}%"
    notice.send()
    os.system('paplay /usr/share/sounds/freedesktop/stereo/message.oga')

# Get latest data
def latest_data():
    if not file_exists_and_not_empty(csv_file):
        return ["UNKNOWN", -1, "UNKNOWN"]

    data = get_latest_data(csv_file)
    timestamp = arrow.get(data.iloc[0][0], "YYYY-MM-DD HH:mm:ss")
    level = data.iloc[0][1]
    state = data.iloc[0][2]

    return [timestamp, float(level), state]


# # Detemine when to send a notification
# def should_notify():
#     last_data = latest_data()[1:]
#     curr_data = [lvl, status()]
    
#     if last_data[-1] != status(): return True
    
#     if last_data != curr_data:
#         if (lvl < 5 and status() == "Discharging") or (curr_data == [100.0, 'Charging']):
#             return True
    
    
#     return False

# # Send the notificaiton message
# def send_message():
#     if should_notify():
#         message()
        

# def blcot():
#     latest_data
        
        
# if __name__=="__main__":
#     while True:
#         send_message()
#         current_battery()
        
#         if round(lvl, 12) != round(latest_data()[1], 12):
#             write_csv()
        
#         time.sleep(3)

import time

# Other existing functions...

def should_notify(last_data, curr_data):
    last_level, last_status = last_data
    curr_level, curr_status = curr_data

    # Check for status change
    if last_status != curr_status:
        return True

    # Existing conditions (e.g., battery level thresholds)
    # Add here any other conditions for notifying based on the battery level

    return False

def send_message():
    global last_notification_time, last_level, last_status
    current_battery()
    curr_data = [lvl, status()]

    if should_notify([last_level, last_status], curr_data):
        current_time = time.time()
        if current_time - last_notification_time > notification_interval:
            message()
            last_notification_time = current_time
            last_level, last_status = curr_data  # Update last known data

if __name__ == "__main__":
    last_notification_time = 0
    notification_interval = 60  # 60 seconds interval
    last_level, last_status = -1, ""  # Initialize with default values

    while True:
        current_battery()

        if round(lvl, 12) != round(latest_data()[1], 12):
            write_csv()

        send_message()
        time.sleep(1)  # Delay of 10 seconds
