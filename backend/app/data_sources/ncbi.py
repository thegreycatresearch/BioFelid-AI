from app.models.evidence import GeneEvidence
import requests


NCBI_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def search_gene(species: str, gene: str) -> dict:
    """
    Search NCBI Gene for a gene in a specific species.
    """

    params = {
        "db": "gene",
        "term": f"{gene}[Gene Name] AND {species}[Organism]",
        "retmode": "json",
    }

    response = requests.get(
        f"{NCBI_BASE_URL}esearch.fcgi",
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    return {
        "species": species,
        "gene": gene,
        "ncbi_gene_ids": data["esearchresult"]["idlist"],
        "count": int(data["esearchresult"]["count"]),
    }

def fetch_gene_record(gene_id: str) -> dict:
    params = {
        "db": "gene",
        "id": gene_id,
        "retmode": "json",
    }

    response = requests.get(
        f"{NCBI_BASE_URL}esummary.fcgi",
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()

def get_gene_evidence(species: str, gene: str) -> GeneEvidence | None:
    search_result = search_gene(
        species=species,
        gene=gene,
    )

    if not search_result["ncbi_gene_ids"]:
        return None

    gene_id = search_result["ncbi_gene_ids"][0]

    raw_record = fetch_gene_record(gene_id)

    record = raw_record["result"][gene_id]

    genomic_info = record.get("genomicinfo", [{}])[0]

    location_history = record.get("locationhist", [{}])[0]

    organism = record.get("organism", {})

    return GeneEvidence(
        species=organism.get("scientificname", species),
        gene=record.get("name", gene),
        ncbi_gene_id=gene_id,
        description=record.get("description"),
        chromosome=record.get("chromosome"),
        genetic_source=record.get("geneticsource"),
        taxid=organism.get("taxid"),
        chromosome_accession=genomic_info.get("chraccver"),
        chromosome_start=genomic_info.get("chrstart"),
        chromosome_stop=genomic_info.get("chrstop"),
        exon_count=genomic_info.get("exoncount"),
        assembly_accession=location_history.get("assemblyaccver"),
        annotation_release=location_history.get("annotationrelease"),
    )

def search_genes(
    species: str,
    query: str = "",
    limit: int = 20,
):
    """
    Search NCBI Gene records for a species.

    Optionally filters by a gene name/symbol query.
    """

    ESEARCH_URL = (
        "https://eutils.ncbi.nlm.nih.gov/"
        "entrez/eutils/esearch.fcgi"
    )

    ESUMMARY_URL = (
        "https://eutils.ncbi.nlm.nih.gov/"
        "entrez/eutils/esummary.fcgi"
    )

    # --------------------------------------------------
    # Build NCBI search query
    # --------------------------------------------------

    term = f'"{species}"[Organism] AND alive[prop]'

    if query.strip():
        term += f' AND {query.strip()}[All Fields]'

    # --------------------------------------------------
    # 1. Search Gene IDs
    # --------------------------------------------------

    search_params = {
        "db": "gene",
        "term": term,
        "retmax": limit,
        "retmode": "json",
    }

    response = requests.get(
        ESEARCH_URL,
        params=search_params,
        timeout=30,
    )

    response.raise_for_status()

    search_data = response.json()

    ids = (
        search_data
        .get("esearchresult", {})
        .get("idlist", [])
    )

    if not ids:
        return []

    # --------------------------------------------------
    # 2. Retrieve summaries
    # --------------------------------------------------

    summary_params = {
        "db": "gene",
        "id": ",".join(ids),
        "retmode": "json",
    }

    response = requests.get(
        ESUMMARY_URL,
        params=summary_params,
        timeout=30,
    )

    response.raise_for_status()

    summary_data = response.json()

    result = summary_data.get("result", {})

    genes = []

    for gene_id in ids:

        gene = result.get(gene_id)

        if not gene:
            continue

        genes.append(
            {
                "gene_id": gene_id,
                "symbol": gene.get("name"),
                "description": gene.get("description"),
            }
        )

    return genes

if __name__ == "__main__":
    evidence = get_gene_evidence(
        species="Panthera tigris",
        gene="BRCA2",
    )

    print(evidence)

if __name__ == "__main__":

    results = search_genes(
        species="Felis catus",
        query="BRCA",
        limit=10,
    )

    print("\nGenes encontrados:\n")

    for gene in results:
        print(gene)