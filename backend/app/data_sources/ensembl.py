import requests

from app.models.evidence import OrthologEvidence, OrthologRecord


ENSEMBL_BASE_URL = "https://rest.ensembl.org"
FELIDAE_TAXON_ID = 9681

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def get_ensembl_species():
    try:
        response = requests.get(
            f"{ENSEMBL_BASE_URL}/info/species",
            headers=HEADERS,
            timeout=15,
        )

        response.raise_for_status()

        # Ensembl puede devolver una respuesta no-JSON
        # cuando está temporalmente caído o saturado.
        try:
            data = response.json()
        except ValueError:
            print(
                "Ensembl returned a non-JSON response:",
                response.status_code,
                response.text[:300],
            )
            return []

        return data.get("species", [])

    except requests.RequestException as error:
        print(f"Ensembl species request failed: {error}")
        return []

def resolve_species(species_name: str):
    species = get_ensembl_species()

    target = species_name.strip().lower()
    normalized_target = target.replace(" ", "_")

    # Exact match
    for item in species:
        if item.get("name", "").lower() == normalized_target:
            return item

    # Scientific-name prefix
    words = target.split()

    if len(words) >= 2:
        prefix = f"{words[0]}_{words[1]}"

        for item in species:
            if item.get("name", "").lower().startswith(prefix):
                return item

    # Alias
    for item in species:
        for alias in item.get("aliases") or []:
            if alias.lower() == target:
                return item

    return None

def lookup_gene(
    ensembl_species: str,
    gene: str,
):
    url = (
        f"{ENSEMBL_BASE_URL}/lookup/symbol/"
        f"{ensembl_species}/{gene}"
    )

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30,
        )

        print("Gene lookup URL:", response.url)
        print("Gene lookup status:", response.status_code)

        if response.status_code in (400, 404):
            return None

        response.raise_for_status()

        try:
            return response.json()
        except ValueError:
            print("Ensembl returned invalid JSON for gene lookup.")
            return None

    except requests.RequestException as error:
        print(f"Ensembl gene lookup failed: {error}")
        return None

def get_felidae_homologies(
    ensembl_species: str,
    ensembl_gene_id: str,
):
    """
    Retrieve orthologues restricted to Felidae.
    """

    url = (
        f"{ENSEMBL_BASE_URL}/homology/id/"
        f"{ensembl_species}/{ensembl_gene_id}"
    )

    params = {
        "type": "orthologues",
        "target_taxon": FELIDAE_TAXON_ID,
        "format": "full",
    }
    
    response = requests.get(
        url,
        params=params,
        headers={"Accept": "application/json"},
        timeout=30,
    )
    
    print("Felidae homology URL:", response.url)
    print("HTTP status:", response.status_code)
    
    if response.status_code == 404:
        return None
        
    if response.status_code == 503:
        print("Ensembl homology service temporarily unavailable.")
    return None
    
    response.raise_for_status()
    
    return response.json()


def parse_felidae_homologies(result):
    """
    Convert the raw Ensembl response into simple dictionaries.
    """

    if not result:
        return []

    homologies = []

    for record in result.get("data", []):
        for homology in record.get("homologies", []):

            target = homology.get("target", {})

            homologies.append(
                {
                    "species": target.get("species"),
                    "id": target.get("id"),
                    "protein_id": target.get("protein_id"),
                    "perc_id": target.get("perc_id"),
                    "perc_pos": target.get("perc_pos"),
                    "type": homology.get("type"),
                }
            )

    return homologies


def build_ortholog_evidence(
    reference_species: str,
    reference_gene: str,
    reference_ensembl_id: str,
    homologies: list[dict],
) -> OrthologEvidence:

    orthologs = []

    for homology in homologies:

        orthologs.append(
            OrthologRecord(
                species=homology.get("species"),
                gene_id=homology.get("id"),
                protein_id=homology.get("protein_id"),
                percent_identity=homology.get("perc_id"),
                percent_positive=homology.get("perc_pos"),
                orthology_type=homology.get("type"),
            )
        )

    return OrthologEvidence(
        reference_species=reference_species,
        reference_gene=reference_gene,
        reference_ensembl_id=reference_ensembl_id,
        felidae_ortholog_count=len(orthologs),
        orthologs=orthologs,
    )

def calculate_ortholog_metrics(evidence: OrthologEvidence):
    """
    Calculate descriptive metrics from observed Felidae orthologs.

    These metrics describe the available evidence.
    They are NOT a conservation priority score.
    """

    orthologs = evidence.orthologs

    if not orthologs:
        return {
            "ortholog_count": 0,
            "one_to_one_count": 0,
            "one_to_one_fraction": 0.0,
            "mean_percent_identity": None,
            "min_percent_identity": None,
            "max_percent_identity": None,
        }

    identities = [
        o.percent_identity
        for o in orthologs
        if o.percent_identity is not None
    ]

    one_to_one_count = sum(
        1
        for o in orthologs
        if o.orthology_type == "ortholog_one2one"
    )

    return {
        "ortholog_count": len(orthologs),

        "one_to_one_count": one_to_one_count,

        "one_to_one_fraction": round(
            one_to_one_count / len(orthologs),
            4,
        ),

        "mean_percent_identity": (
            round(sum(identities) / len(identities), 4)
            if identities
            else None
        ),

        "min_percent_identity": (
            round(min(identities), 4)
            if identities
            else None
        ),

        "max_percent_identity": (
            round(max(identities), 4)
            if identities
            else None
        ),
    }

if __name__ == "__main__":

    print("=" * 60)
    print("BioFelid AI — Felidae ortholog evidence")
    print("=" * 60)

    species = "Panthera tigris"
    gene = "BRCA2"

    print("\n1. Resolving species...")

    resolved = resolve_species(species)

    if resolved is None:
        print("Species not found.")
        raise SystemExit(1)

    ensembl_species = resolved["name"]

    print("Ensembl species:", ensembl_species)

    print("\n2. Looking up gene...")

    gene_result = lookup_gene(
        ensembl_species=ensembl_species,
        gene=gene,
    )

    if gene_result is None:
        print("Gene not found.")
        raise SystemExit(1)

    ensembl_gene_id = gene_result["id"]

    print("Gene:", gene_result.get("display_name"))
    print("Ensembl ID:", ensembl_gene_id)

    print("\n3. Querying Felidae orthologues...")

    result = get_felidae_homologies(
        ensembl_species=ensembl_species,
        ensembl_gene_id=ensembl_gene_id,
    )

    homologies = parse_felidae_homologies(result)

    print("\nFelidae orthologues found:")
    print(len(homologies))

    print("\n4. Building OrthologEvidence...")

    evidence = build_ortholog_evidence(
        reference_species=species,
        reference_gene=gene,
        reference_ensembl_id=ensembl_gene_id,
        homologies=homologies,
    )

    print("\nOrthologEvidence:")
    print(evidence)

    metrics = calculate_ortholog_metrics(evidence)
    
    print("\n6. Ortholog metrics:")
    print(metrics)

    print("\n5. Individual orthologues:")

    for ortholog in evidence.orthologs:

        print(
            f"- {ortholog.species}"
            f" | identity={ortholog.percent_identity}"
            f" | positive={ortholog.percent_positive}"
            f" | type={ortholog.orthology_type}"
        )

    print("\nDone.")