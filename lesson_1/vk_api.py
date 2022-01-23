import os
import json
import requests
from pprint import pprint

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, "tmp", "settings.json"), "r") as settings:
    vk_settings = json.load(settings)

METHOD = vk_settings["METHOD"]
TOKEN = vk_settings["TOKEN"]
V = vk_settings["V"]
USER_ID = vk_settings["USER_ID"]

url = f'https://api.vk.com/method/{METHOD}?extended=1&access_token={TOKEN}&v={V}&user_id={USER_ID}'

groups = requests.get(url)

j_data = groups.json()

with open('vk_groups.json', "w") as file:
    json.dump(j_data, file, indent=2)