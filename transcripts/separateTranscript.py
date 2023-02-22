# This script is used to separate all transcripts object stored in the transcripts.json file
# It needs the transcript file and will generate a json file for every transcript and will store
# them in the same hierarchy as the original database

import os
import json
import time
import argparse

# Parse the arguments passed to the script
parser = argparse.ArgumentParser()
parser.add_argument("json_file", help="Path to the JSON file")
args = parser.parse_args()

# Load the JSON file
with open(args.json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Confirm that the JSON file has been loaded
print("JSON loaded")

# Iterate over each item in the JSON data
for item in data:
    file_path = item["file"]

    # Get the current timestamp as a string
    timestamp = str(int(time.time()))

    # Split the file path into the directory and filename
    directory, filename = os.path.split(file_path)

    # Remove the "F:/" part from the directory path
    directory = directory[3:]

    # Create the directory hierarchy, if it does not exist
    os.makedirs(directory, exist_ok=True)

    # Write the JSON data for each item to a file
    with open(f"{directory}/{timestamp}_transcript.json", "w", encoding="utf-8") as f:
        json.dump(item, f)
