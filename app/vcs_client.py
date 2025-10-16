import urllib.parse
import requests
from .cache import TTLCache
from .utils import make_flask_response

PROJECT_CACHE = TTLCache()
FILE_CACHE = TTLCache()

def get_project_id(config, session, logger, project_name):
    """
    Retrieve the GitLab project ID for a given project name.
    Uses caching to minimize repeated API calls.
    """

    active_tool = config.get("activeTool", "gitlab").lower()
    if active_tool != "gitlab":
        logger.warning(f"Active tool '{active_tool}' is not GitLab. Skipping project ID lookup.")
        return None

    tool_conf = config.get("gitlab", {})
    namespace = tool_conf.get("namespace")

    if not namespace:
        logger.error("Namespace not configured for GitLab in apiDetailsConfig.json.")
        return None

    key = f"{namespace}/{project_name}"
    cached = PROJECT_CACHE.get(key)
    if cached:
        logger.debug(f"Cache hit for project ID: {key} -> {cached}")
        return cached

    base_url = tool_conf.get("gitLabUrl")
    if not base_url:
        logger.error("gitLabUrl not found in config file for GitLab.")
        return None

    url = f"{base_url.rstrip('/')}/api/v4/projects/{urllib.parse.quote(key, safe='')}"
    logger.debug(f"Fetching GitLab project ID from {url}")

    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
        pid = r.json().get("id")

        if pid:
            PROJECT_CACHE.set(key, pid, 3600)
            logger.info(f"Cached GitLab project ID: {key} -> {pid}")
            return pid
        else:
            logger.error(f"No 'id' field in GitLab response for project {key}")
            return None

    except requests.exceptions.HTTPError as e:
        logger.error(f"GitLab API returned HTTP error for project {key}: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed while fetching GitLab project ID: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error fetching project ID for {key}: {e}")

    return None


def fetch_file(config, session, logger, project_name, file_path, branch="main"):
    """
    GitLab-only fetcher:
      - Uses activeTool from config but only supports 'gitlab' (logs & returns error otherwise)
      - Caches requests.Response objects for FILE_CONTENT_TTL (default 300s)
      - Preserves upstream content-type and status codes
      - Returns Flask Response (via make_flask_response) or (json, status) tuples on error
    """
    tool = config.get("activeTool", "gitlab").lower()
    cache_key = f"{tool}:{project_name}:{file_path}:{branch}"

    # Try cache first
    cached = FILE_CACHE.get(cache_key)
    if cached:
        logger.debug("Cache hit for %s", cache_key)
        # cached is expected to be a requests.Response (same as when we set it below)
        return make_flask_response(cached)

    # Only GitLab supported for now
    if tool != "gitlab":
        logger.warning("Active tool '%s' is not supported by fetch_file (only 'gitlab' supported)", tool)
        return {"error": f"Unsupported active tool: {tool}"}, 400

    # Resolve project id (helper function should already be GitLab-only)
    pid = get_project_id(config, session, logger, project_name)
    if not pid:
        logger.info("Project not found: %s/%s", config.get("gitlab", {}).get("namespace"), project_name)
        return {"error": f"GitLab project '{project_name}' not found."}, 404

    base_url = config.get("gitlab", {}).get("gitLabUrl")
    if not base_url:
        logger.error("gitLabUrl missing in config for GitLab")
        return {"error": "gitLabUrl not configured"}, 500

    encoded_path = urllib.parse.quote(file_path, safe="")
    url = f"{base_url.rstrip('/')}/api/v4/projects/{pid}/repository/files/{encoded_path}/raw"
    params = {"ref": branch}

    logger.debug("Fetching file from GitLab: url=%s params=%s", url, params)

    try:
        r = session.get(url, params=params, timeout=10)
        r.raise_for_status()
        # Cache the requests.Response object (same type used by make_flask_response)
        FILE_CACHE.set(cache_key, r, 300)
        logger.info("Fetched and cached file %s (project=%s, branch=%s)", file_path, project_name, branch)
        return make_flask_response(r)

    except requests.exceptions.HTTPError as e:
        # upstream returned 4xx/5xx
        status_code = getattr(e.response, "status_code", None)
        logger.error("GitLab HTTP error fetching file %s: %s (status=%s)", file_path, e, status_code)
        # Try to forward upstream body if available
        try:
            return make_flask_response(e.response)
        except Exception:
            return {"error": "GitLab returned an HTTP error", "details": str(e)}, 502

    except requests.exceptions.RequestException as e:
        logger.error("Network/request error fetching file %s: %s", file_path, e)
        return {"error": "Request to GitLab failed", "details": str(e)}, 502

    except Exception as e:
        logger.exception("Unexpected error fetching file %s: %s", file_path, e)
        return {"error": "Internal server error", "details": str(e)}, 500
