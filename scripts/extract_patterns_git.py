import os
import json
import time
import requests

# GitHub repository URL
repo_url = 'https://api.github.com/repos/danielmiessler/fabric/contents/patterns'
# Raw content base URL
raw_base_url = 'https://raw.githubusercontent.com/danielmiessler/fabric/main/patterns'
# Unique user ID
user_id = "798bec86-f06a-4fc9-bf74-0af494b81eec"
# Current timestamp
timestamp = int(time.time())

# List to hold JSON objects
consolidated_data = []

# Get the list of pattern folders from the GitHub API
response = requests.get(repo_url)
if response.status_code == 200:
    pattern_folders = response.json()
    for pattern_folder in pattern_folders:
        if pattern_folder['type'] == 'dir':
            folder_name = pattern_folder['name']
            # Construct the URL to the system.md file
            file_url = f"{raw_base_url}/{folder_name}/system.md"
            
            # Download the file
            file_response = requests.get(file_url)
            
            if file_response.status_code == 200:
                content = file_response.text
                
                # Create a JSON object
                json_object = {
                    "command": f"/{folder_name.replace('_', '-')}",
                    "user_id": user_id,
                    "title": folder_name.replace('_', ' '),
                    "content": content,
                    "timestamp": timestamp
                }
                
                # Add the JSON object to the list
                consolidated_data.append(json_object)
            else:
                print(f"Failed to download {file_url}")
else:
    print(f"Failed to retrieve pattern folders from {repo_url}")

# Write the consolidated data to a .json file
output_file = 'consolidated_patterns_git.json'
with open(output_file, 'w') as f:
    json.dump(consolidated_data, f, indent=2)

print(f"Consolidated data written to {output_file}")