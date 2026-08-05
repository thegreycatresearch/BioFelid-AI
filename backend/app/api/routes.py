from fastapi import APIRouter, HTTPException

from app.data_sources.taxonomy import get_felidae_species

from app.data_sources.ncbi import (
    get_gene_evidence,
    search_genes,
)

from app.data_sources.uniprot import (
    get_uniprot_evidence,
)

from app.data_sources.ensembl import (
    resolve_species,
    lookup_gene,
    get_felidae_homologies,
    parse_felidae_homologies,
    build_ortholog_evidence,
    calculate_ortholog_metrics,
)


router = APIRouter()


# ==================================================
# ANALYZE CANDIDATE
# ==================================================

@router.get("/analyze")
def analyze(species: str, gene: str):

    # --------------------------------------------------
    # 1. NCBI
    # --------------------------------------------------

    ncbi_evidence = get_gene_evidence(
        species=species,
        gene=gene,
    )

    if ncbi_evidence is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "No NCBI Gene record found for this "
                "species/gene combination."
            ),
        )

    # --------------------------------------------------
    # 2. UniProt
    # --------------------------------------------------

    uniprot_evidence = get_uniprot_evidence(
        species=species,
        gene=gene,
        taxid=ncbi_evidence.taxid,
    )

    # --------------------------------------------------
    # 3. Ensembl species resolution
    # --------------------------------------------------

    ensembl_species = resolve_species(species)

    # If Ensembl doesn't have this species
    if ensembl_species is None:

        return {
            "species": ncbi_evidence.species,
            "gene": ncbi_evidence.gene,

            "ncbi": {
                "gene_id": ncbi_evidence.ncbi_gene_id,
                "description": ncbi_evidence.description,
                "chromosome": ncbi_evidence.chromosome,
                "genetic_source": ncbi_evidence.genetic_source,
                "taxid": ncbi_evidence.taxid,
                "chromosome_accession": (
                    ncbi_evidence.chromosome_accession
                ),
                "chromosome_start": (
                    ncbi_evidence.chromosome_start
                ),
                "chromosome_stop": (
                    ncbi_evidence.chromosome_stop
                ),
                "exon_count": ncbi_evidence.exon_count,
                "assembly_accession": (
                    ncbi_evidence.assembly_accession
                ),
                "annotation_release": (
                    ncbi_evidence.annotation_release
                ),
            },

            "ensembl": None,

            "uniprot": {
                "found": uniprot_evidence.found,
                "accession": uniprot_evidence.accession,
                "entry_name": uniprot_evidence.entry_name,
                "protein_name": uniprot_evidence.protein_name,
                "organism": uniprot_evidence.organism,
                "length": uniprot_evidence.length,
                "function": uniprot_evidence.function,
                "keywords": uniprot_evidence.keywords,
                "source": uniprot_evidence.source,
            },
        }

    ensembl_species_name = ensembl_species["name"]

    # --------------------------------------------------
    # 4. Ensembl gene lookup
    # --------------------------------------------------

    ensembl_gene = lookup_gene(
        ensembl_species=ensembl_species_name,
        gene=gene,
    )

    # If Ensembl has the species but not the gene
    if ensembl_gene is None:

        return {
            "species": ncbi_evidence.species,
            "gene": ncbi_evidence.gene,

            "ncbi": {
                "gene_id": ncbi_evidence.ncbi_gene_id,
                "description": ncbi_evidence.description,
                "chromosome": ncbi_evidence.chromosome,
                "genetic_source": ncbi_evidence.genetic_source,
                "taxid": ncbi_evidence.taxid,
                "chromosome_accession": (
                    ncbi_evidence.chromosome_accession
                ),
                "chromosome_start": (
                    ncbi_evidence.chromosome_start
                ),
                "chromosome_stop": (
                    ncbi_evidence.chromosome_stop
                ),
                "exon_count": ncbi_evidence.exon_count,
                "assembly_accession": (
                    ncbi_evidence.assembly_accession
                ),
                "annotation_release": (
                    ncbi_evidence.annotation_release
                ),
            },

            "ensembl": {
                "species": ensembl_species_name,
                "gene": None,
                "orthologs": [],
                "metrics": None,
            },

            "uniprot": {
                "found": uniprot_evidence.found,
                "accession": uniprot_evidence.accession,
                "entry_name": uniprot_evidence.entry_name,
                "protein_name": uniprot_evidence.protein_name,
                "organism": uniprot_evidence.organism,
                "length": uniprot_evidence.length,
                "function": uniprot_evidence.function,
                "keywords": uniprot_evidence.keywords,
                "source": uniprot_evidence.source,
            },
        }

    ensembl_gene_id = ensembl_gene["id"]

    # --------------------------------------------------
    # 5. Felidae orthologues
    # --------------------------------------------------

    homology_result = get_felidae_homologies(
        ensembl_species=ensembl_species_name,
        ensembl_gene_id=ensembl_gene_id,
    )

    homologies = parse_felidae_homologies(
        homology_result
    )

    # --------------------------------------------------
    # 6. Structured ortholog evidence
    # --------------------------------------------------

    ortholog_evidence = build_ortholog_evidence(
        reference_species=species,
        reference_gene=gene,
        reference_ensembl_id=ensembl_gene_id,
        homologies=homologies,
    )

    metrics = calculate_ortholog_metrics(
        ortholog_evidence
    )

    # --------------------------------------------------
    # 7. Combined response
    # --------------------------------------------------

    return {
        "species": ncbi_evidence.species,
        "gene": ncbi_evidence.gene,

        # ----------------------------------------------
        # NCBI
        # ----------------------------------------------

        "ncbi": {
            "gene_id": ncbi_evidence.ncbi_gene_id,
            "description": ncbi_evidence.description,
            "chromosome": ncbi_evidence.chromosome,
            "genetic_source": ncbi_evidence.genetic_source,
            "taxid": ncbi_evidence.taxid,
            "chromosome_accession": (
                ncbi_evidence.chromosome_accession
            ),
            "chromosome_start": (
                ncbi_evidence.chromosome_start
            ),
            "chromosome_stop": (
                ncbi_evidence.chromosome_stop
            ),
            "exon_count": ncbi_evidence.exon_count,
            "assembly_accession": (
                ncbi_evidence.assembly_accession
            ),
            "annotation_release": (
                ncbi_evidence.annotation_release
            ),
        },

        # ----------------------------------------------
        # ENSEMBL
        # ----------------------------------------------

        "ensembl": {
            "species": ensembl_species_name,
            "gene_id": ensembl_gene_id,

            "display_name": ensembl_gene.get(
                "display_name"
            ),

            "assembly": ensembl_gene.get(
                "assembly_name"
            ),

            "biotype": ensembl_gene.get(
                "biotype"
            ),

            "orthologs": [
                {
                    "species": ortholog.species,
                    "gene_id": ortholog.gene_id,
                    "protein_id": ortholog.protein_id,
                    "percent_identity": (
                        ortholog.percent_identity
                    ),
                    "percent_positive": (
                        ortholog.percent_positive
                    ),
                    "orthology_type": (
                        ortholog.orthology_type
                    ),
                }
                for ortholog in ortholog_evidence.orthologs
            ],

            "metrics": metrics,

            "source": ortholog_evidence.source,
        },

        # ----------------------------------------------
        # UNIPROT
        # ----------------------------------------------

        "uniprot": {
            "found": uniprot_evidence.found,

            "accession": (
                uniprot_evidence.accession
            ),

            "entry_name": (
                uniprot_evidence.entry_name
            ),

            "protein_name": (
                uniprot_evidence.protein_name
            ),

            "organism": (
                uniprot_evidence.organism
            ),

            "length": (
                uniprot_evidence.length
            ),

            "function": (
                uniprot_evidence.function
            ),

            "keywords": (
                uniprot_evidence.keywords
            ),

            "source": (
                uniprot_evidence.source
            ),
        },
    }


# ==================================================
# GENE SEARCH
# ==================================================

@router.get("/genes")
def get_genes(
    species: str,
    query: str = "",
):

    try:

        genes = search_genes(
            species=species,
            query=query,
            limit=20,
        )

        return {
            "species": species,
            "query": query,
            "genes": genes,
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"NCBI gene search failed: {str(error)}",
        )


# ==================================================
# FELIDAE SPECIES
# ==================================================

@router.get("/species")
def get_species():

    return {
        "family": "Felidae",
        "species": get_felidae_species(),
    }