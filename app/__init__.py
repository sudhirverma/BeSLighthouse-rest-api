from flask import Flask
from flask_cors import CORS
import logging
from .routes import main_bp
from .config import load_config


def create_app(config_path: str | None = None):
    app = Flask(__name__)
    app.config.from_mapping(load_config(config_path))
    logging.basicConfig(level=app.config.get('LOG_LEVEL', 'INFO'))
    CORS(app, resources={r"/*": {"origins": "*"}}, expose_headers=["Content-Type"])
    app.register_blueprint(main_bp)
    return app
