import os
from flask import Flask
from flask_cors import CORS
from .logging_config import configure_logging
from .config import config as app_config

def create_app() -> Flask:
    """Application factory"""
    app = Flask(__name__, instance_relative_config=False)
    # attach config object for easy access
    app.config['APP_CONFIG'] = app_config

    # ensure log dir exists
    os.makedirs(app_config.LOG_DIR, exist_ok=True)

    # configure logging (console + rotating file)
    configure_logging(app)

    # enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # register blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    # simple health endpoint
    @app.route('/healthz')
    def healthz():
        return {'status': 'ok'}, 200

    app.logger.info('BeSLighthouse Flask app initialized (GitLab-only)')
    return app
