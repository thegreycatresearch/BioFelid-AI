THREAT_STATUS_WEIGHTS = {
    "LC": 0,
    "NT": 5,
    "VU": 10,
    "EN": 15,
    "CR": 20,
}


def calculate_brps(
    threat_status: str,
    conservation_score: float,
    functional_relevance: float,
    variant_evidence: float,
    literature_signal: float,
) -> dict:
    """
    Calculate the BioFelid Research Priority Score (BRPS).

    All input scores except threat_status are expected to be
    normalized between 0 and 1.
    """

    threat_score = THREAT_STATUS_WEIGHTS.get(threat_status, 0)

    conservation_points = conservation_score * 25
    functional_points = functional_relevance * 20
    variant_points = variant_evidence * 15
    literature_points = literature_signal * 20

    total = (
        threat_score
        + conservation_points
        + functional_points
        + variant_points
        + literature_points
    )

    total = min(total, 100)

    if total < 35:
        tier = "Exploratory"
    elif total < 65:
        tier = "Moderate"
    else:
        tier = "High Priority"

    return {
        "score": round(total, 2),
        "tier": tier,
        "components": {
            "threat_status": threat_score,
            "conservation": round(conservation_points, 2),
            "functional_relevance": round(functional_points, 2),
            "variant_evidence": round(variant_points, 2),
            "literature_signal": round(literature_points, 2),
        },
    }


if __name__ == "__main__":
    result = calculate_brps(
        threat_status="EN",
        conservation_score=0.8,
        functional_relevance=0.7,
        variant_evidence=0.4,
        literature_signal=0.6,
    )

    print(result)