
def assess_risk(text, message, urls, evidence, ml_result=None):
    text_lower = text.lower()

    heuristic_score = min(100, message["signal_count"] * 18)

    if message["excessive_exclamation"]:
        heuristic_score += 8

    if message["all_caps_terms"]:
        heuristic_score += 5

    for item in urls["urls"]:
        heuristic_score += min(15, len(item["flags"]) * 5)

    financial_terms = [
    "collect request",
    "approve the payment",
    "transfer your funds",
    "pay registration fee"
    ]

    urgency_terms = [
        "within 15 minutes", "immediately", "expires today",
        "account will be blocked", "avoid cancellation"
    ]

    sensitive_terms = [
        "otp", "one-time code", "password", "card details",
        "bank details"
    ]

    if any(term in text_lower for term in financial_terms):
        heuristic_score += 20

    if any(term in text_lower for term in urgency_terms):
        heuristic_score += 10

    if any(term in text_lower for term in sensitive_terms):
        heuristic_score += 15

    # Targeted UPI refund scam combination
    if (
        "refund" in text_lower
        and ("upi" in text_lower or "collect request" in text_lower)
        and ("approve" in text_lower or "accept" in text_lower)
    ):
        heuristic_score += 25

    heuristic_score = min(100, heuristic_score)

    if ml_result and ml_result.get("available"):
        ml_score = ml_result["spam_probability"] * 100
        score = round(0.65 * heuristic_score + 0.35 * ml_score)
    else:
        score = round(heuristic_score)

    score = max(0, min(100, score))

    if score >= 60:
        level = "High"
        advice = (
            "Treat this as suspicious. Do not click links or share "
            "sensitive information. Verify through an official channel."
        )
    elif score >= 30:
        level = "Medium"
        advice = (
            "Be cautious. Independently verify the sender and use "
            "the organisation's official website or phone number."
        )
    else:
        level = "Low"
        advice = (
            "Few warning signals were found, but this is not a safety "
            "guarantee. Verify unexpected requests independently."
        )

    return {
        "score": score,
        "level": level,
        "advice": advice,
        "method": (
            "65% heuristic score and 35% SMS-model spam probability "
            "when available. Includes additional financial-risk rules. "
            "Not a calibrated probability."
        )
    }
