from flask import Blueprint, current_app, jsonify, make_response
from .services.git_client import GitClient

bp = Blueprint('main', __name__)
_client = None

@bp.before_app_first_request
def _init_client():
    global _client
    cfg = current_app.config['APP_CONFIG']
    _client = GitClient(cfg, current_app.logger)
    current_app.logger.info('GitClient initialized for namespace=%s', cfg.NAMESPACE)

def _json_response(payload, status=200):
    return make_response(jsonify(payload), status)

@bp.route('/osspoi_master', methods=['GET'])
def get_osspoi_master():
    current_app.logger.info('GET /osspoi_master')
    return _json_response(_client.fetch_file('besecure-assets-store', 'projects/project-metadata.json'))

@bp.route('/version_details/<filename>', methods=['GET'])
def get_version_detail(filename):
    current_app.logger.info('GET /version_details/%s', filename)
    return _json_response(_client.fetch_file('besecure-assets-store', f'projects/project-version/{filename}'))

@bp.route('/assessment_datastore/<path:pars>', methods=['GET'])
def get_assessment_datastore(pars):
    current_app.logger.info('GET /assessment_datastore/%s', pars)
    return _json_response(_client.fetch_file('besecure-assessment-datastore', pars))

@bp.route('/vulnerability_of_interest', methods=['GET'])
def get_voi():
    current_app.logger.info('GET /vulnerability_of_interest')
    return _json_response(_client.fetch_file('besecure-assets-store', 'vulnerabilities/vulnerability-metadata.json'))

@bp.route('/model_of_interest', methods=['GET'])
def get_moi():
    current_app.logger.info('GET /model_of_interest')
    return _json_response(_client.fetch_file('besecure-assets-store', 'models/model-metadata.json'))

@bp.route('/model_assessment/<path:pars>', methods=['GET'])
def get_model_assessment(pars):
    current_app.logger.info('GET /model_assessment/%s', pars)
    return _json_response(_client.fetch_file('besecure-ml-assessment-datastore', pars))
