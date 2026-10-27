import re
from urllib.parse import urlparse

URL_RE = re.compile(r"(?i)\b(?:https?://|www\.)[^\s<>'\"]+")

def investigate_urls(text: str) -> dict:
    raw_urls = URL_RE.findall(text)
    results = []
    for raw in raw_urls[:10]:
        cleaned = raw.rstrip(".,!?);]")
        normalized = cleaned if cleaned.lower().startswith(("http://", "https://")) else "http://" + cleaned
        parsed = urlparse(normalized)
        host = (parsed.hostname or "").lower()
        flags = []
        if parsed.scheme == "http":
            flags.append("Uses HTTP rather than HTTPS")
        if host.startswith("xn--") or ".xn--" in host:
            flags.append("Contains an internationalized/punycode domain")
        if re.search(r"\d{1,3}(?:\.\d{1,3}){3}", host):
            flags.append("Uses an IP address as the host")
        if len(host.split(".")) >= 5:
            flags.append("Has an unusually deep subdomain structure")
        if any(x in host for x in ["verify", "secure", "account", "login", "claim", "gift"]):
            flags.append("Host contains a sensitive-action word")
        results.append({"url": cleaned, "host": host, "flags": flags,
                        "note": "No live domain reputation or destination-page check was performed."})
    return {"urls": results, "count": len(results)}
