from flask import Flask
import requests
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.get("/osspoi_master")
@cross_origin()
def get_osspoi_master():
    response = requests.get("https://raw.githubusercontent.com/Be-Secure/besecure-osspoi-datastore/main/OSSP-Master.json")
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    return {"Failed to fetch data from osspoiMaster:", response.status_code}

@app.get("/version_details/<filename>")
@cross_origin()
def get_version_detail(filename):
    response = requests.get(f"https://raw.githubusercontent.com/Be-Secure/besecure-osspoi-datastore/main/version_details/{filename}")
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    return {"Failed to fetch data from version_detail:", response.status_code}

@app.get("/assessment_datastore/<path:pars>")
@cross_origin()
def get_assessment_datastore(pars):
    response = requests.get(f"https://raw.githubusercontent.com/Be-Secure/besecure-assessment-datastore/main/{pars}")
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    return {"Failed to fetch data from assessment datastore:", response.status_code}

@app.get("/vulnerability_of_interest")
@cross_origin()
def get_voi():
    response = requests.get(f"https://raw.githubusercontent.com/Be-Secure/besecure-ossvoi-datastore/main/vulnerability-of-interest.json")
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    return {"Failed to fetch data from vulnerability-of-interest:", response.status_code}
