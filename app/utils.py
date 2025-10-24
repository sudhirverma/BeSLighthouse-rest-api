import json
from requests import Response

def safe_json(resp: Response):
    try:
        return resp.json()
    except ValueError:
        return resp.text
