import os
import json
from pathlib import Path

def load_config(logger):
    config_path = Path(os.getenv("BESL_CONFIG_PATH", "/opt/BeSLighthouse/src/apiDetailsConfig.json"))
    config = {}

    if config_path.exists():
        try:
            with config_path.open("r") as f:
                config = json.load(f)
            logger.info(f"Loaded configuration from {config_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file {config_path}: {e}")
        except Exception as e:
            logger.error(f"Failed to read config file {config_path}: {e}")
    else:
        logger.warning(f"Configuration file not found at {config_path}")

    config["activeTool"] = os.getenv("BESL_ACTIVE_TOOL", config.get("activeTool", "gitlab"))

    tool = config.get(config["activeTool"], {})
    tool["namespace"] = os.getenv("BESL_NAMESPACE", tool.get("namespace"))
    tool["branch"] = os.getenv("BESL_BRANCH", tool.get("branch", "main"))
    tool["token"] = os.getenv("BESL_TOKEN", tool.get("token"))
    config[config["activeTool"]] = tool

    return config
