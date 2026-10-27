from agents.coordinator import investigate

def test_analysis_returns_risk_and_trace():
    result = investigate("Your account is suspended. Verify immediately at http://example.test/login")
    assert 0 <= result["risk"]["score"] <= 100
    assert result["risk"]["level"] in {"Low", "Medium", "High"}
    assert len(result["agent_trace"]) == 6

def test_url_is_detected():
    result = investigate("Visit https://example.com now")
    assert result["url_analysis"]["count"] == 1
