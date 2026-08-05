from app.scoring.brps import calculate_brps


def test_brps_calculates_expected_score():
    result = calculate_brps(
        threat_status="EN",
        conservation_score=0.8,
        functional_relevance=0.7,
        variant_evidence=0.4,
        literature_signal=0.6,
    )

    assert result["score"] == 67.0
    assert result["tier"] == "High Priority"

def test_low_priority_candidate():
    result = calculate_brps(
        threat_status="LC",
        conservation_score=0.1,
        functional_relevance=0.1,
        variant_evidence=0.0,
        literature_signal=0.1,
    )

    assert result["tier"] == "Exploratory"