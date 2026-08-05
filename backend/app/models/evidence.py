from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GeneEvidence:
    species: str
    gene: str
    ncbi_gene_id: str
    description: str
    chromosome: str
    genetic_source: str
    taxid: int
    chromosome_accession: str
    chromosome_start: int
    chromosome_stop: int
    exon_count: int
    assembly_accession: str
    annotation_release: str


@dataclass
class OrthologRecord:
    species: str
    gene_id: Optional[str]
    protein_id: Optional[str]
    percent_identity: Optional[float]
    percent_positive: Optional[float]
    orthology_type: Optional[str]


@dataclass
class OrthologEvidence:
    reference_species: str
    reference_gene: str
    reference_ensembl_id: str
    felidae_ortholog_count: int
    orthologs: list[OrthologRecord]
    source: str = "Ensembl Compara"

@dataclass
class UniProtEvidence:
    species: str
    gene: str
    found: bool

    accession: Optional[str] = None
    entry_name: Optional[str] = None
    protein_name: Optional[str] = None
    organism: Optional[str] = None
    length: Optional[int] = None

    function: Optional[str] = None
    keywords: list[str] = field(default_factory=list)

    reviewed: bool = False

    source: str = "UniProt"