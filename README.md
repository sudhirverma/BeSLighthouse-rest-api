# BeSLighthouse API (Production-grade)

This is a robust, production-ready Flask backend that proxies data from GitLab or GitHub.

## 🧭 Configuration
- Default config file path: `/opt/BeSLighthouse/src/apiDetailsConfig.json`
- Can be overridden by `BESL_CONFIG_PATH` environment variable.

## ⚙️ Run Locally
```bash
pip install -r requirements.txt
python run.py
```

## 🐳 Run with Docker
```bash
docker build -t besl-api .
docker run -p 5000:5000 besl-api
```
