
import re

KEYWORDS = {
    "urgency": [
        "immediately", "urgent", "act now", "within 24 hours",
        "expires today", "last chance", "within 15 minutes"
    ],
    "credential_request": [
        "password", "otp", "one-time password", "pin", "cvv",
        "verify your account", "login", "card details",
        "one-time code", "bank details"
    ],
    "financial_lure": [
        "won", "prize", "cashback", "lottery", "free gift",
        "claim your"
    ],
    "threat": [
        "account suspended", "account will be blocked",
        "blocked", "legal action", "arrest", "penalty"
    ]
}

def analyze_message(text: str) -> dict:
    lower = text.lower()

    found = {
        name: [term for term in terms if term in lower]
        for name, terms in KEYWORDS.items()
    }
    found = {k: v for k, v in found.items() if v}

    # Treat refund messages as suspicious only when context suggests
    # a potentially deceptive payment or refund claim.
    refund_action_terms = [
        "collect request",
        "approve the payment",
        "approve the upi",
        "pay a fee",
        "pay registration fee",
        "transfer your funds",
        "claim your refund",
        "refund is pending",
        "refund pending"
    ]

    refund_context_terms = [
        "refund", "reimbursement"
    ]

    if (
        any(term in lower for term in refund_context_terms)
        and any(term in lower for term in refund_action_terms)
    ):
        found["financial_lure"] = ["suspicious refund/payment request"]

    exclamations = text.count("!")
    caps_words = re.findall(r"\b[A-Z]{4,}\b", text)

    return {
        "signals": found,
        "signal_count": sum(len(v) for v in found.values()),
        "excessive_exclamation": exclamations >= 3,
        "all_caps_terms": caps_words[:8],
        "summary": (
            "Potential social-engineering language detected."
            if found else
            "No listed keyword signals detected; this does not prove "
            "the message is safe."
        )
    }
