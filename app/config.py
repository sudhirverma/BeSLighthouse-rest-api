import os
import json
import logging
from typing import Dict, Any

class Config:
    """Configuration object loaded from /opt/BeSLighthouse/src/apiDetailsConfig.json.
    GitLab-only (raises if activeTool is not 'gitlab').
    """

    def __init__(self) -> None:
        home_dir = os.path.expanduser('/opt')
        file_name = 'apiDetailsConfig.json'
        self.file_path = os.path.join(home_dir, 'BeSLighthouse', 'src', file_name)

        self._data = self._load_json_config()

        self.active_tool: str = self._data.get('activeTool', 'gitlab').lower()
        if self.active_tool != 'gitlab':
            raise ValueError(f"Unsupported active tool '{self.active_tool}'. Only 'gitlab' is supported.")

        self.gitlab: Dict[str, Any] = self._data.get('gitlab', {})
        self.NAMESPACE: str = self.gitlab.get('namespace')
        self.BRANCH: str = self.gitlab.get('branch', 'main')
        self.TOKEN: str = self.gitlab.get('token')
        self.GITLAB_URL: str = self.gitlab.get('gitLabUrl')

        # Misc
        self.LOG_DIR: str = self._data.get('logDir', './logs')
        self.ENV: str = os.getenv('ENV', 'production')
        self.REQUEST_TIMEOUT: float = float(os.getenv('REQUEST_TIMEOUT', '10.0'))

        # HTTP headers for GitLab
        self.HEADERS = self._build_headers()

        logging.getLogger(__name__).info('Config loaded from %s', self.file_path)

    def _load_json_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f'Configuration file not found: {self.file_path}')
        try:
            with open(self.file_path, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            return data
        except json.JSONDecodeError as exc:
            logging.getLogger(__name__).exception('Invalid JSON in config file: %s', exc)
            raise
        except Exception:
            logging.getLogger(__name__).exception('Failed to load config file')
            raise

    def _build_headers(self) -> Dict[str, str]:
        if not self.TOKEN:
            logging.getLogger(__name__).warning('GitLab token not found in config - some API calls may fail')
            return {}
        return {'PRIVATE-TOKEN': self.TOKEN}


# singleton instance for easy import
config = Config()
