def gather_evidence(text: str, message: dict, urls: dict) -> dict:
    observations = []
    for category, terms in message["signals"].items():
        observations.append({"type": category.replace("_", " ").title(), "detail": "Matched wording: " + ", ".join(terms)})
    for item in urls["urls"]:
        for flag in item["flags"]:
            observations.append({"type": "URL signal", "detail": f"{item['host']}: {flag}"})
    if not observations:
        observations.append({"type": "No known indicator", "detail": "The current heuristic checks found no listed warning signals. This is not proof of legitimacy."})
    return {"observations": observations, "limitations": [
        "This demo does not browse the web or query threat-intelligence services.",
        "Signals are heuristic and can produce false positives or false negatives.",
        "Do not enter passwords, OTPs, payment details, or personal information into suspicious links."
    ]}
