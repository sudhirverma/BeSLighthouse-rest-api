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

GITLAB_API_BASE = f"{data['gitlab']['gitLabUrl']}/api/v4"
GITLAB_NAMESPACE = data['gitlab']['namespace']
DEFAULT_BRANCH = data['gitlab']['branch']

# Cache project IDs
project_id_cache = {}

def get_project_id(project_name):
    """Get GitLab project ID for a given project name."""
    key = f"{GITLAB_NAMESPACE}/{project_name}"
    if key in project_id_cache:
        return project_id_cache[key]

    try:
        response = requests.get(
            f"{GITLAB_API_BASE}/projects",
            headers=headers,
            params={"search": project_name}
        )
        response.raise_for_status()
        projects = response.json()
        for project in projects:
            if project["path_with_namespace"] == f"{GITLAB_NAMESPACE}/{project_name}":
                project_id_cache[key] = project["id"]
                return project["id"]
        return None
    except Exception as e:
        print(f"Error getting project ID: {e}")
        return None

def fetch_file_from_gitlab(project_name, file_path, branch=DEFAULT_BRANCH):
    """Fetch file content from GitLab repo."""
    project_id = get_project_id(project_name)
    if not project_id:
        return {"error": f"Project '{project_name}' not found."}

    encoded_path = urllib.parse.quote(file_path, safe='')
    url = f"{GITLAB_API_BASE}/projects/{project_id}/repository/files/{encoded_path}/raw?ref={branch}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON returned", "url": url}
    except requests.exceptions.RequestException as e:
        return {"error": "Request failed", "details": str(e), "url": url}


@app.get("/osspoi_master")
@cross_origin()
def get_osspoi_master():
    return fetch_file_from_gitlab("besecure-assets-store", "projects/project-metadata.json")

@app.get("/version_details/<filename>")
@cross_origin()
def get_version_detail(filename):
    return fetch_file_from_gitlab("besecure-assets-store", f"projects/project-version/{filename}")

@app.get("/assessment_datastore/<path:pars>")
@cross_origin()
def get_assessment_datastore(pars):
    return fetch_file_from_gitlab("besecure-assessment-datastore", pars)

@app.get("/vulnerability_of_interest")
@cross_origin()
def get_voi():
    return fetch_file_from_gitlab("besecure-assets-store", "vulnerabilities/vulnerability-metadata.json")

@app.get("/model_of_interest")
@cross_origin()
def get_moi():
    return fetch_file_from_gitlab("besecure-assets-store", "models/model-metadata.json")

@app.get("/model_assessment/<path:pars>")
@cross_origin()
def get_model_assessment(pars):
    return fetch_file_from_gitlab("besecure-ml-assessment-datastore", pars)
