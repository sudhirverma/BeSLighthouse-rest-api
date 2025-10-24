import os, json
from typing import Dict

DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser('/opt'), 'BeSLighthouse', 'src', 'apiDetailsConfig.json')

def _load_json_file(path: str) -> Dict:
    try:
        with open(path, 'r') as fh:
            return json.load(fh)
    except Exception:
        return {}

def load_config(config_path: str | None = None) -> Dict:
    path = config_path or os.getenv('BESL_CONFIG_PATH') or DEFAULT_CONFIG_PATH
    cfg = _load_json_file(path)
    active_tool = os.getenv('ACTIVE_TOOL') or cfg.get('activeTool', 'gitlab')
    tool_cfg = cfg.get(active_tool, {})
    return {
        'API_CONFIG_RAW': cfg,
        'ACTIVE_TOOL': active_tool.lower(),
        'TOOL_CONFIG': tool_cfg,
        'NAMESPACE': tool_cfg.get('namespace'),
        'BRANCH': tool_cfg.get('branch', 'main'),
        'TOKEN': tool_cfg.get('token'),
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO')
    }
