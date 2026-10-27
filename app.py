from flask import Flask, render_template, request, jsonify
from agents.coordinator import investigate
from database.db import init_db, save_scan, get_history

app = Flask(__name__)
init_db()

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/api/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    text = str(payload.get("text", "")).strip()
    if not text:
        return jsonify({"error": "Enter a message or URL to investigate."}), 400
    result = investigate(text)
    scan_id = save_scan(text, result)
    result["scan_id"] = scan_id
    return jsonify(result)

@app.get("/api/history")
def history():
    return jsonify({"items": get_history()})

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "app": "AgentShield"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
