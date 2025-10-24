from flask import Blueprint, current_app, jsonify
from .services.vcs_client import VCSClient

main_bp = Blueprint('main', __name__)

def _client():
    cfg = current_app.config
    raw_cfg = cfg['API_CONFIG_RAW']
    return VCSClient(raw_cfg, cfg['ACTIVE_TOOL'], cfg.get('TOKEN') or cfg.get('TOOL_CONFIG', {}).get('token'), cfg.get('BRANCH'))

@main_bp.get('/osspoi_master')
def get_osspoi_master():
    client = _client()
    return jsonify(client.fetch_file('besecure-assets-store', 'projects/project-metadata.json'))

@main_bp.get('/version_details/<filename>')
def get_version_detail(filename: str):
    client = _client()
    return jsonify(client.fetch_file('besecure-assets-store', f'projects/project-version/{filename}'))

@main_bp.get('/assessment_datastore/<path:pars>')
def get_assessment_datastore(pars: str):
    client = _client()
    return jsonify(client.fetch_file('besecure-assessment-datastore', pars))

@main_bp.get('/vulnerability_of_interest')
def get_voi():
    client = _client()
    return jsonify(client.fetch_file('besecure-assets-store', 'vulnerabilities/vulnerability-metadata.json'))

@main_bp.get('/model_of_interest')
def get_moi():
    client = _client()
    return jsonify(client.fetch_file('besecure-assets-store', 'models/model-metadata.json'))

@main_bp.get('/model_assessment/<path:pars>')
def get_model_assessment(pars: str):
    client = _client()
    return jsonify(client.fetch_file('besecure-ml-assessment-datastore', pars))
