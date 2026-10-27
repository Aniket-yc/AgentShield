# AgentShield — Multi-Agent AI Scam Investigation

A student demonstration project that analyzes suspicious text and URLs using a coordinator and four specialist agents. It provides explainable heuristic findings and saves recent scans in a local SQLite database.

## Features
- Flask web application and responsive dashboard
- Coordinator routes input through message, URL, evidence, and risk agents
- Transparent heuristic score (not a probability or definitive verdict)
- Scan history stored locally in SQLite
- API endpoints: `GET /api/health`, `POST /api/analyze`, `GET /api/history`
- Optional SMS spam model training script

## Run on Windows PowerShell
Use Python 3.12 if available.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again. You can also run `.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt` without activation.

## Optional SMS model training
The web demo works without a trained ML model. To train the optional classifier, download the UCI SMS Spam Collection dataset and save it as `data/SMSSpamCollection` (tab-separated label and message), then run:

```powershell
python scripts/train_model.py
```

The model artifact is saved to `models/sms_model.joblib`. This training script is an optional extension and is not currently used by the heuristic dashboard.

## Tests
Run `python -m pytest -q`. Test status should be checked locally; the included tests are not a substitute for security validation.

## Limitations
This demo does not perform live web browsing, domain reputation checks, or antivirus scanning. A low score is not proof that content is safe. Do not submit real passwords, OTPs, payment information, or private data.
