
from agents.message_analyst import analyze_message
from agents.url_investigator import investigate_urls
from agents.evidence_researcher import gather_evidence
from agents.risk_analyst import assess_risk
from agents.ml_classifier import classify_message


def investigate(text: str) -> dict:
    message = analyze_message(text)
    urls = investigate_urls(text)

    # Run the trained machine-learning classifier.
    ml_result = classify_message(text)

    evidence = gather_evidence(text, message, urls)
    risk = assess_risk(text, message, urls, evidence, ml_result)

    return {
        "input": text,
        "status": "completed",
        "risk": risk,
        "message_analysis": message,
        "url_analysis": urls,
        "ml_analysis": ml_result,
        "evidence": evidence,
        "agent_trace": [
            {
                "agent": "Coordinator",
                "status": "completed",
                "detail": "Routed input to specialist agents."
            },
            {
                "agent": "Message Analyst",
                "status": "completed",
                "detail": "Checked for social-engineering signals."
            },
            {
                "agent": "URL Investigator",
                "status": "completed",
                "detail": f"Inspected {len(urls['urls'])} URL(s)."
            },
            {
                "agent": "ML Classifier",
                "status": "completed" if ml_result["available"] else "unavailable",
                "detail": (
                    f"SMS model prediction: {ml_result['prediction']}."
                    if ml_result["available"]
                    else ml_result["note"]
                )
            },
            {
                "agent": "Evidence Researcher",
                "status": "completed",
                "detail": "Compiled observable signals and limitations."
            },
            {
                "agent": "Risk Analyst",
                "status": "completed",
                "detail": "Combined heuristic and ML signals when available."
            }
        ]
    }
