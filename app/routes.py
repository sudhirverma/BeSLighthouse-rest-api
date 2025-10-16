import requests
from flask import jsonify
from .vcs_client import fetch_file

def register_routes(app, logger, config):
    session = requests.Session()
    headers = {}
    token = config.get(config.get("activeTool"), {}).get("token")
    if token:
        if config["activeTool"] == "gitlab":
            headers = {"PRIVATE-TOKEN": token}
        else:
            headers = {"Authorization": f"Bearer {token}"}
    session.headers.update(headers)

    @app.get("/osspoi_master")
    def osspoi():
        return fetch_file(config, session, logger, "besecure-assets-store", "projects/project-metadata.json")

    @app.get("/version_details/<path:filename>")
    def version_details(filename):
        return fetch_file(config, session, logger, "besecure-assets-store", f"projects/project-version/{filename}")

    @app.get("/assessment_datastore/<path:pars>")
    def assessment(pars):
        return fetch_file(config, session, logger, "besecure-assessment-datastore", pars)

    @app.get("/vulnerability_of_interest")
    def voi():
        return fetch_file(config, session, logger, "besecure-assets-store", "vulnerabilities/vulnerability-metadata.json")

    @app.get("/model_of_interest")
    def moi():
        return fetch_file(config, session, logger, "besecure-assets-store", "models/model-metadata.json")

    @app.get("/model_assessment/<path:pars>")
    def model_assessment(pars):
        return fetch_file(config, session, logger, "besecure-ml-assessment-datastore", pars)
