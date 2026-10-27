# Architecture

1. **Coordinator** receives input and invokes the specialist agents.
2. **Message Analyst** flags known urgency, credential-request, financial-lure, and threat phrases.
3. **URL Investigator** parses URLs and checks basic visible structure. It does not open the destination.
4. **Evidence Researcher** explains which signals were observed and states limitations.
5. **Risk Analyst** combines heuristic signals into a 0–100 score and plain-language advice.
6. **Flask API/UI** displays the report; SQLite stores local scan history.

The score is a hand-authored heuristic, not a calibrated probability. A later version could add a trained classifier and reputable threat-intelligence API.
