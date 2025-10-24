# BeSLighthouse Backend (Professional)

A professional Flask backend skeleton configured to read GitLab-only configuration from:

```
/opt/BeSLighthouse/src/apiDetailsConfig.json
```

Features:
- App factory pattern
- Blueprint-based routes
- Structured services layer (`app/services`)
- Robust logging (console + rotating file) using a dedicated logging configurator
- Gunicorn-friendly `wsgi.py`
- Dockerfile and systemd example included
- Tests skeleton

## Run (development)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Run (production, gunicorn)
```bash
gunicorn -c gunicorn.conf.py wsgi:app
```

## Systemd example
See `systemd/beslighthouse.service` (edit paths and user).

## Notes
- Place the `apiDetailsConfig.json` at `/opt/BeSLighthouse/src/apiDetailsConfig.json`.
- This project is GitLab-only by design (per user preference).
