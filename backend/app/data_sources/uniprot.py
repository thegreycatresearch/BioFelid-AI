import requests

from app.models.evidence import UniProtEvidence


UNIPROT_SEARCH_URL = "https://rest.uniprot.org/uniprotkb/search"


def get_uniprot_evidence(
    species: str,
    gene: str,
    taxid: int,
) -> UniProtEvidence:

    query = f"gene:{gene} AND organism_id:{taxid}"

    params = {
        "query": query,
        "format": "json",
        "size": 10,
        "fields": (
            "accession,"
            "id,"
            "protein_name,"
            "organism_name,"
            "length,"
            "cc_function,"
            "keyword"
        ),
    }

    response = requests.get(
        UNIPROT_SEARCH_URL,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])

    # --------------------------------------------------
    # No UniProt record
    # --------------------------------------------------

    if not results:
        return UniProtEvidence(
            species=species,
            gene=gene,
            found=False,
        )

    # --------------------------------------------------
    # Prefer reviewed Swiss-Prot entries
    # --------------------------------------------------

    reviewed_results = [
        result
        for result in results
        if result.get("entryType")
        == "UniProtKB reviewed (Swiss-Prot)"
    ]

    if reviewed_results:
        result = reviewed_results[0]
        reviewed = True
    else:
        result = results[0]
        reviewed = False

    # --------------------------------------------------
    # Organism
    # --------------------------------------------------

    organism = result.get("organism", {})

    # --------------------------------------------------
    # Protein name
    # --------------------------------------------------

    protein_description = result.get(
        "proteinDescription",
        {}
    )

    recommended_name = protein_description.get(
        "recommendedName",
        {}
    )

    full_name = recommended_name.get(
        "fullName",
        {}
    )

    protein_name = full_name.get("value")

    # --------------------------------------------------
    # Function
    # --------------------------------------------------

    comments = result.get("comments", [])

    function_text = None

    for comment in comments:

        if comment.get("commentType") == "FUNCTION":

            texts = comment.get("texts", [])

            if texts:
                function_text = texts[0].get("value")

            break

    # --------------------------------------------------
    # Keywords
    # --------------------------------------------------

    keywords = []

    for keyword in result.get("keywords", []):

        value = keyword.get("value")

        if value:
            keywords.append(value)

    # --------------------------------------------------
    # Evidence object
    # --------------------------------------------------

    return UniProtEvidence(
        species=species,
        gene=gene,
        found=True,

        accession=result.get(
            "primaryAccession"
        ),

        entry_name=result.get(
            "uniProtkbId"
        ),

        protein_name=protein_name,

        organism=organism.get(
            "scientificName"
        ),

        length=result.get(
            "sequence",
            {}
        ).get("length"),

        function=function_text,

        keywords=keywords,

        reviewed=reviewed,
    )


if __name__ == "__main__":

    result = get_uniprot_evidence(
        species="Felis catus",
        gene="BRCA2",
        taxid=9685,
    )

    print(result)