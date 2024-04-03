from flask import Flask

import os
import json
import requests
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Get the home directory
home_dir = os.path.expanduser("/opt")

# Define the filename
file_name = "apiDetailsConfig.json"

# Construct the full path
file_path = os.path.join(home_dir, 'BeSLighthouse', 'src' ,file_name)

# Open the JSON file in read mode ('r')
with open(file_path, 'r') as file:
    # Load JSON data
    data = json.load(file)

headers = {
    'PRIVATE-TOKEN': data["gitlab"]["token"]
}

@app.get("/osspoi_master")
@cross_origin()
def get_osspoi_master():
    response = requests.get(f"{data['gitlab']['apiUrl']}/{data['gitlab']['namespace']}/besecure-assets-store/{data['gitlab']['branch']}/projects/project-metadata.json", headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    return {"Failed to fetch data from osspoiMaster:", response.status_code}

@app.get("/version_details/<filename>")
@cross_origin()
def get_version_detail(filename):
    response = requests.get(f"{data['gitlab']['apiUrl']}/{data['gitlab']['namespace']}/besecure-assets-store/{data['gitlab']['branch']}/projects/project-version/{filename}", headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    return {"Failed to fetch data from version_detail:", response.status_code}

@app.get("/assessment_datastore/<path:pars>")
@cross_origin()
def get_assessment_datastore(pars):
    response = requests.get(f"{data['gitlab']['apiUrl']}/{data['gitlab']['namespace']}/besecure-assessment-datastore/{data['gitlab']['branch']}/{pars}", headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    return {"Failed to fetch data from assessment datastore:", response.status_code}

@app.get("/vulnerability_of_interest")
@cross_origin()
def get_voi():
    response = requests.get(f"{data['gitlab']['apiUrl']}/{data['gitlab']['namespace']}/besecure-assets-store/{data['gitlab']['branch']}/vulnerabilities/vulnerability-metadata.json", headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    return {"Failed to fetch data from vulnerability-of-interest:", response.status_code}

@app.get("/model_of_interest")
@cross_origin()
def get_moi():
    response = requests.get(f"{data['gitlab']['apiUrl']}/{data['gitlab']['namespace']}/besecure-assets-store/{data['gitlab']['branch']}/models/model-metadata.json", headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    return {"Failed to fetch data from model-of-interest:", response.status_code}
