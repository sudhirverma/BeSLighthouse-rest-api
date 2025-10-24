import urllib.parse, requests
from typing import Optional, Dict
from ..utils import safe_json
from ..services.cache import SimpleCache

cache = SimpleCache()

class VCSClient:
    def __init__(self, raw_config: Dict, active_tool: str, token: Optional[str], branch: str):
        self.raw_config = raw_config
        self.active_tool = active_tool
        self.token = token
        self.branch = branch
        self.namespace = raw_config.get('namespace') if raw_config else None

    def _headers(self) -> Dict[str, str]:
        if self.active_tool == 'gitlab' and self.token:
            return {'PRIVATE-TOKEN': self.token}
        if self.active_tool == 'github' and self.token:
            return {'Authorization': f'token {self.token}'}
        return {}

    def _gitlab_project_id(self, project_name: str) -> Optional[int]:
        key = f"{self.namespace}/{project_name}"
        cached = cache.get(key)
        if cached: return cached
        base = self.raw_config.get('gitlab', {}).get('gitLabUrl')
        if not base: return None
        try:
            resp = requests.get(f"{base}/api/v4/projects", headers=self._headers(), params={"search": project_name}, timeout=10)
            resp.raise_for_status()
            for p in resp.json():
                if p.get('path_with_namespace') == key:
                    pid = p.get('id')
                    cache.set(key, pid)
                    return pid
        except requests.RequestException:
            return None
        return None

    def fetch_file(self, project_name: str, file_path: str) -> Dict:
        if self.active_tool == 'gitlab':
            project_id = self._gitlab_project_id(project_name)
            if not project_id: return {'error': f"GitLab project '{project_name}' not found."}
            encoded = urllib.parse.quote(file_path, safe='')
            base = self.raw_config.get('gitlab', {}).get('gitLabUrl')
            url = f"{base}/api/v4/projects/{project_id}/repository/files/{encoded}/raw?ref={self.branch}"
        elif self.active_tool == 'github':
            api = self.raw_config.get('github', {}).get('apiUrl')
            url = f"{api}/{self.namespace}/{project_name}/{self.branch}/{file_path}"
        else:
            return {'error': f"Unsupported active tool: {self.active_tool}"}
        try:
            r = requests.get(url, headers=self._headers(), timeout=15)
            r.raise_for_status()
            return safe_json(r)
        except requests.exceptions.JSONDecodeError:
            return {'error': 'Invalid JSON returned', 'url': url}
        except requests.RequestException as e:
            return {'error': 'Request failed', 'details': str(e), 'url': url}
