from flask import Flask, request
import requests

app = Flask(__name__)


@app.get("/osspoi_master")
def get_osspoi_master():
    response = requests.get("https://raw.githubusercontent.com/Be-Secure/besecure-osspoi-datastore/main/OSSP-Master.json")
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    return {"Failed to fetch data from osspoiMaster:", response.status_code}

@app.get("/version_details/<filename>")
def get_version_detail(filename):
    response = requests.get(f"https://raw.githubusercontent.com/Be-Secure/besecure-osspoi-datastore/main/version_details/{filename}")
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    return {"Failed to fetch data from version_detail:", response.status_code}
