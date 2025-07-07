Title: Configure Schedule & Event Triggers for Pipeline Automation  
Name: Kallu Maheshwari  
Task: Automate pipeline using schedule and event triggers  

Description:
This project simulates automated pipeline execution using both schedule-based and event-based triggers without using Azure services.

1. Schedule Trigger:
   - Uses the `schedule` module to execute the pipeline every 10 seconds.
   - Simulates regular pipeline execution intervals for batch data movement.

2. Event Trigger:
   - Uses the `watchdog` module to watch a folder named `trigger_folder/`.
   - Automatically triggers the pipeline whenever a new file is added to that folder.
   - Simulates dynamic, real-time data arrival triggering the pipeline.

How to Run:
1. Make sure required packages are installed:
   pip install schedule watchdog

2. Create a folder in the same directory called:
   trigger_folder

3. Run the script:
   python pipeline_trigger_simulation.py

4. You will see output in the terminal:
   - "Schedule Trigger" messages every 10 seconds.
   - "Event Trigger" messages when a file is added to the `trigger_folder/`.

Note:
To simulate the event trigger, add any text file (e.g., test.txt) into the `trigger_folder/` during runtime.

This script emulates Azure Data Factory-style automation using local Python simulation tools.

