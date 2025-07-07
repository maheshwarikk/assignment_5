import os
import time
import threading
from datetime import datetime
import schedule

# CONFIGURATION 
WATCH_FOLDER = "trigger_folder"  # Folder to monitor for event trigger
TRIGGER_INTERVAL_SECONDS = 10     # Interval for schedule-based trigger

# Create the folder if it doesn't exist
if not os.path.exists(WATCH_FOLDER):
    os.makedirs(WATCH_FOLDER)

def run_pipeline(trigger_type):
    print(f"[{trigger_type}] Pipeline executed at {datetime.now().strftime('%H:%M:%S')}")

#  Schedule Trigger
def schedule_trigger():
    run_pipeline("Schedule Trigger")

#  Event Trigger (file creation) 
existing_files = set(os.listdir(WATCH_FOLDER))
def event_trigger():
    global existing_files
    current_files = set(os.listdir(WATCH_FOLDER))
    new_files = current_files - existing_files
    if new_files:
        run_pipeline("Event Trigger")
    existing_files = current_files

# Schedule task every 10 seconds
schedule.every(TRIGGER_INTERVAL_SECONDS).seconds.do(schedule_trigger)

def monitor():
    print("[Monitor] Pipeline monitoring started...")
    while True:
        schedule.run_pending()
        event_trigger()
        time.sleep(1)

# Run the monitor loop
monitor()
