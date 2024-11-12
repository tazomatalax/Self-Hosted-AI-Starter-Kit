import os
import json
import time

# Path to the patterns folder
patterns_folder = '/home/tazomatalax/.config/fabric/patterns'
# Unique user ID
user_id = "798bec86-f06a-4fc9-bf74-0af494b81eec"
# Current timestamp
timestamp = int(time.time())

# List to hold JSON objects
consolidated_data = []

# Walk through the patterns folder
for root, dirs, files in os.walk(patterns_folder):
    for file in files:
        if file == "system.md":
            # Read the content of the system.md file
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Get the pattern folder name
            pattern_folder_name = os.path.basename(root)
            
            # Create a JSON object
            json_object = {
                "command": f"/{pattern_folder_name.replace('_', '-')}",
                "user_id": user_id,
                "title": pattern_folder_name.replace('_', ' '),
                "content": content,
                "timestamp": timestamp
            }
            
            # Add the JSON object to the list
            consolidated_data.append(json_object)

# Write the consolidated data to a .json file
output_file = 'consolidated_patterns.json'
with open(output_file, 'w') as f:
    json.dump(consolidated_data, f, indent=2)

print(f"Consolidated data written to {output_file}")