# Viva preparation

**What is AgentShield?** A multi-agent-style investigation demo that analyzes message text and visible URL structure, then explains potential risk signals.

**Why multiple agents?** Responsibilities are separated into small components: text signals, URL signals, evidence summary, and risk aggregation. The coordinator orchestrates them.

**What is the backend?** Flask exposes the dashboard route and JSON API. Python modules perform analysis; SQLite stores scan history.

**What is the frontend?** HTML structures the dashboard, CSS styles it, and JavaScript submits input using `fetch()` and renders the JSON response.

**Is the score an actual probability?** No. It is a transparent heuristic score for demonstration only.

**Does it check a website's live reputation?** No. The current version does not browse to URLs or call threat-intelligence services.

**What is the optional ML component?** A TF-IDF + Logistic Regression pipeline can be trained on the UCI SMS Spam Collection dataset. It is an optional extension and is not connected to the current dashboard scoring.
