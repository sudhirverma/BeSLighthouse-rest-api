import urllib.parse
import requests
from functools import lru_cache
from typing import Optional
from requests import RequestException

class GitClient:
    """Lightweight GitLab client for fetching raw file contents from repository."""

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        # lru_cache on methods that accept hashable args
        self._get_project_id_cached = self.get_project_id

    @lru_cache(maxsize=1024)
    def get_project_id(self, project_name: str) -> Optional[int]:
        """Search and return GitLab project id for a repo name under configured namespace."""
        key = f"{self.config.NAMESPACE}/{project_name}"
        try:
            url = f"{self.config.GITLAB_URL.rstrip('/')}/api/v4/projects"
            resp = requests.get(url, headers=self.config.HEADERS, params={'search': project_name}, timeout=self.config.REQUEST_TIMEOUT)
            resp.raise_for_status()
            projects = resp.json()
            for p in projects:
                if p.get('path_with_namespace') == key:
                    return p.get('id')
            self.logger.debug('Project %s not found in search results', key)
            return None
        except RequestException as exc:
            self.logger.exception('HTTP error while searching project %s: %s', project_name, exc)
            return None
        except Exception as exc:
            self.logger.exception('Unexpected error while searching project %s: %s', project_name, exc)
            return None

    def fetch_file(self, project_name: str, file_path: str, branch: Optional[str] = None):
        branch = branch or self.config.BRANCH
        project_id = self.get_project_id(project_name)
        if not project_id:
            return {'error': f"GitLab project '{project_name}' not found"}

        encoded_path = urllib.parse.quote(file_path, safe='')
        url = f"{self.config.GITLAB_URL.rstrip('/')}/api/v4/projects/{project_id}/repository/files/{encoded_path}/raw"
        params = {'ref': branch}
        try:
            self.logger.debug('Fetching %s (branch=%s)', file_path, branch)
            resp = requests.get(url, headers=self.config.HEADERS, params=params, timeout=self.config.REQUEST_TIMEOUT)
            resp.raise_for_status()
            # Try parse JSON, otherwise return text
            try:
                return resp.json()
            except ValueError:
                return {'content': resp.text}
        except RequestException as exc:
            self.logger.exception('HTTP error while fetching file %s/%s: %s', project_name, file_path, exc)
            return {'error': 'request_failed', 'details': str(exc)}
        except Exception as exc:
            self.logger.exception('Unexpected error while fetching file %s/%s: %s', project_name, file_path, exc)
            return {'error': 'unexpected_error', 'details': str(exc)}
