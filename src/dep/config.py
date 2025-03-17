import json
import os

CONFIG_FILE = "config.json"

def save_config(soundboard):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(soundboard, config_file)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            return json.load(config_file)
    return {}