import json
import requests
import re

pattern = r"\|\|(.+?)\^"

def download_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to download JSON:", response.status_code)
        return None

def create_txt_files(data):
    for obj in data:
        obj_id = obj.get("id")
        rules = obj.get("rules")
        if obj_id and rules:
            filename = 'lists/' + obj_id + ".txt"
            with open(filename, "w") as file:
                for rule in rules:
                  match = re.search(pattern, rule)
                  if match:
                      line = match.group(1)
                  else:
                      line = rule
                  file.write(f"0.0.0.0 {line}\n")
            print(f"Created {filename} file.")

# Pulls AdguardHome service lists and converts it to individual files
url = "https://adguardteam.github.io/HostlistsRegistry/assets/services.json"  

json_data = download_json(url)
if json_data:
    create_txt_files(json_data['blocked_services'])