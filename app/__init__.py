from flask import Flask
from flask_cors import CORS
from .config import load_config
from .logger import setup_logging
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    logger = setup_logging()
    config = load_config(logger)

    app.config.update(config)
    logger.info(f"Active tool: {config.get('activeTool', 'gitlab')}")

    register_routes(app, logger, config)

    @app.route("/healthz")
    def health_check():
        return {"status": "ok", "active_tool": config.get("activeTool", "gitlab")}, 200

    return app
