import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "agentshield.sqlite3"

def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with _connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_text TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            result_json TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")

def save_scan(text, result):
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO scans(input_text, risk_level, risk_score, result_json) VALUES(?,?,?,?)",
            (text, result["risk"]["level"], result["risk"]["score"], json.dumps(result))
        )
        return cur.lastrowid

def get_history(limit=30):
    with _connect() as conn:
        rows = conn.execute("SELECT id, input_text, risk_level, risk_score, created_at FROM scans ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(row) for row in rows]
