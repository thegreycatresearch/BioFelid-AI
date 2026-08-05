import { useEffect, useRef, useState } from "react";
import "./App.css";

function App() {
  const [species, setSpecies] = useState("Panthera tigris");
  const [gene, setGene] = useState("BRCA2");

  const [speciesList, setSpeciesList] = useState([]);
  const [speciesLoading, setSpeciesLoading] = useState(true);

  const [evidence, setEvidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [geneResults, setGeneResults] = useState([]);
  const [geneSearch, setGeneSearch] = useState("");
  const [geneLoading, setGeneLoading] = useState(false);
  const [geneDropdownOpen, setGeneDropdownOpen] = useState(false);
  const [geneError, setGeneError] = useState(null);
  const geneDebounceRef = useRef(null);
  const selectedSpecies = speciesList.find(
  (item) => item.scientific_name === species
);
  // --------------------------------
  // LOAD FELIDAE SPECIES
  // --------------------------------

  useEffect(() => {
    async function loadSpecies() {
      try {
        setSpeciesLoading(true);

        const response = await fetch(
          "http://127.0.0.1:8000/api/species"
        );

        if (!response.ok) {
          throw new Error("Could not load Felidae species.");
        }

        const data = await response.json();

        setSpeciesList(data.species || []);

      } catch (err) {
        setError(err.message);
      } finally {
        setSpeciesLoading(false);
      }
    }

    loadSpecies();
  }, []);

  // cleanup debounce on unmount
  useEffect(() => {
    return () => {
      if (geneDebounceRef.current) {
        clearTimeout(geneDebounceRef.current);
      }
    };
  }, []);

  function searchGenes(query) {
    setGeneSearch(query);
    setGene("");
    setGeneDropdownOpen(true);
    setGeneError(null);

    // cancel any pending debounced fetch
    if (geneDebounceRef.current) {
      clearTimeout(geneDebounceRef.current);
    }

    if (query.trim().length < 2) {
      setGeneResults([]);
      setGeneLoading(false);
      return;
    }

    setGeneLoading(true);

    geneDebounceRef.current = setTimeout(async () => {
      try {
        const params = new URLSearchParams({
          species,
          query: query.trim(),
        });

        const response = await fetch(
          `http://127.0.0.1:8000/api/genes?${params}`
        );

        if (!response.ok) {
          const errorData = await response.json();

          throw new Error(
            errorData.detail || "Could not search genes."
          );
        }

        const data = await response.json();

        setGeneResults(data.genes || []);
      } catch (err) {
        setGeneError(err.message);
        setGeneResults([]);
      } finally {
        setGeneLoading(false);
      }
    }, 350);
  }

  // --------------------------------
  // ANALYZE
  // --------------------------------

  async function analyzeCandidate() {
    setLoading(true);
    setError(null);
    setEvidence(null);

    try {
      const params = new URLSearchParams({
        species,
        gene,
      });

      const response = await fetch(
        `http://127.0.0.1:8000/api/analyze?${params}`
      );

      if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
          errorData.detail || "Analysis failed."
        );
      }

      const data = await response.json();

      setEvidence(data);

    } catch (err) {
      setError(err.message);

    } finally {
      setLoading(false);
    }
  }

return (
  <main className="app">

      {/* -------------------------------- */}
      {/* HEADER */}
      {/* -------------------------------- */}

      <section className="hero">

        <p className="eyebrow">
          CONSERVATION GENOMICS
        </p>

        <h1>
          BioFelid AI
        </h1>

        <p className="subtitle">
          Explore genomic evidence for felid
          conservation research.
        </p>

      </section>


      {/* -------------------------------- */}
      {/* SEARCH */}
      {/* -------------------------------- */}

      <section className="search-card">

        <h2>
          Analyze a candidate
        </h2>


        {/* SPECIES */}

        <label htmlFor="species">Species</label>
        
        <select
          className="species-select"
          id="species"
          value={species}
          disabled={loading || speciesLoading}
          onChange={(event) => {
            setSpecies(event.target.value);
            setGene("");
            setGeneSearch("");
            setGeneResults([]);
          }}
        >
          {speciesLoading ? (
            <option>Loading species...</option>
          ) : (
            speciesList.map((item) => (
              <option
                key={item.taxid}
                value={item.scientific_name}
              >
                {item.scientific_name}
              </option>
            ))
          )}
        </select>

        {selectedSpecies && (
          <div className="conservation-status">
            <span>Conservation status</span>
            <strong>{selectedSpecies.conservation_status}</strong>
          </div>
        )}
      
        {/* GENE */}

<div className="gene-search">

  <label htmlFor="gene">
    Candidate gene
  </label>

  <p className="field-help">
    Search for a gene symbol or name to explore genomic evidence.
  </p>

  <div className="gene-input-wrapper">

    <span className="gene-search-icon">
      ⌕
    </span>

    <input
      id="gene"
      type="text"
      value={geneSearch}
      onChange={(event) => {
        searchGenes(event.target.value);
      }}
      onFocus={() => {
        if (geneSearch.trim().length >= 2) {
          setGeneDropdownOpen(true);
        }
      }}
      onKeyDown={(event) => {
        if (event.key === "Escape") {
          setGeneDropdownOpen(false);
        }
      }}
      placeholder="Search by gene symbol..."
      autoComplete="off"
    />

    {geneLoading && (
      <span className="gene-spinner" />
    )}

  </div>

  {geneDropdownOpen && geneSearch.trim().length >= 2 && (
    <div className="gene-dropdown">

      {geneLoading && (
        <div className="gene-status">
          <span className="gene-spinner" />
          <span>Searching NCBI...</span>
        </div>
      )}

      {!geneLoading && geneError && (
        <div className="gene-status">
          <span className="gene-status-icon">⚠</span>
          <div>
            <strong>Search unavailable</strong>
            <span>Could not reach NCBI. Try again in a moment.</span>
          </div>
        </div>
      )}

      {!geneLoading && !geneError && geneResults.length === 0 && (
        <div className="gene-status">
          <span className="gene-status-icon">⌕</span>

          <div>
            <strong>No genes found</strong>
            <span>
              Try another gene symbol or search term.
            </span>
          </div>
        </div>
      )}

      {!geneLoading && geneResults.length > 0 && (
        <>
          <div className="gene-results-header">
            <span>NCBI Gene results</span>
            <span>{geneResults.length}</span>
          </div>

          <div className="gene-results-list">

            {geneResults.map((result) => (
              <button
                type="button"
                key={result.gene_id}
                className="gene-result"
                onClick={() => {
                  setGene(result.symbol);
                  setGeneSearch(result.symbol);
                  setGeneResults([]);
                  setGeneDropdownOpen(false);
                }}
              >

                <div className="gene-result-main">

                  <span className="gene-symbol">
                    {result.symbol}
                  </span>

                  <span className="gene-description">
                    {result.description ||
                      "No description available"}
                  </span>

                </div>

                <span className="gene-id">
                  NCBI · {result.gene_id}
                </span>

              </button>
            ))}

          </div>
        </>
      )}

    </div>
  )}

  {gene && (
    <div className="selected-gene">
      <span className="selected-gene-check">✓</span>

      <div>
        <span>Selected candidate</span>
        <strong>{gene}</strong>
      </div>
    </div>
  )}

</div>
        
        {/* BUTTON */}

        <button
          type="button"
          onClick={analyzeCandidate}
          disabled={
            loading ||
            speciesLoading ||
            !species
          }
        >

          {loading
            ? "Analyzing..."
            : "Analyze candidate"}

        </button>

      </section>


      {/* -------------------------------- */}
      {/* ERROR */}
      {/* -------------------------------- */}

      {error && (

        <section className="result-card error-card">

          <p className="eyebrow">
            ANALYSIS ERROR
          </p>

          <h2>
            Something went wrong
          </h2>

          <p>
            {error}
          </p>

        </section>

      )}


      {/* -------------------------------- */}
      {/* RESULTS */}
      {/* -------------------------------- */}

      {evidence && (

        <>

          {/* OVERVIEW */}

          <section className="result-card">

            <p className="eyebrow">
              CANDIDATE ANALYSIS
            </p>

            <h2>
              {evidence.gene} · {evidence.species}
            </h2>

            <p className="source-note">
              Evidence assembled from NCBI Gene,
              Ensembl Compara, and UniProt.
            </p>

          </section>


          {/* NCBI */}

          {evidence.ncbi && (

            <section className="result-card">

              <p className="eyebrow">
                NCBI GENE EVIDENCE
              </p>

              <h2>
                Gene annotation
              </h2>

              <div className="evidence-grid">

                <div>
                  <span>
                    NCBI Gene ID
                  </span>

                  <strong>
                    {evidence.ncbi.gene_id}
                  </strong>
                </div>

                <div>
                  <span>
                    Description
                  </span>

                  <strong>
                    {evidence.ncbi.description ||
                      "Not available"}
                  </strong>
                </div>

                <div>
                  <span>
                    Chromosome
                  </span>

                  <strong>
                    {evidence.ncbi.chromosome ||
                      "Not available"}
                  </strong>
                </div>

                <div>
                  <span>
                    Exons
                  </span>

                  <strong>
                    {evidence.ncbi.exon_count ??
                      "Not available"}
                  </strong>
                </div>

                <div>
                  <span>
                    Taxonomy ID
                  </span>

                  <strong>
                    {evidence.ncbi.taxid ??
                      "Not available"}
                  </strong>
                </div>

                <div>
                  <span>
                    Genetic source
                  </span>

                  <strong>
                    {evidence.ncbi.genetic_source ||
                      "Not available"}
                  </strong>
                </div>

                <div>
                  <span>
                    Assembly
                  </span>

                  <strong>
                    {evidence.ncbi.assembly_accession ||
                      "Not available"}
                  </strong>
                </div>

                <div>
                  <span>
                    Annotation release
                  </span>

                  <strong>
                    {evidence.ncbi.annotation_release ||
                      "Not available"}
                  </strong>
                </div>

              </div>

            </section>

          )}


          {/* ENSEMBL */}

          {evidence.ensembl && (

            <section className="result-card">

              <p className="eyebrow">
                ENSEMBL GENE EVIDENCE
              </p>

              <h2>
                Comparative genomics
              </h2>

              <div className="evidence-grid">

                <div>
                  <span>
                    Ensembl Gene ID
                  </span>

                  <strong>
                    {evidence.ensembl.gene_id ||
                      "Not available"}
                  </strong>
                </div>

                <div>
                  <span>
                    Species model
                  </span>

                  <strong>
                    {evidence.ensembl.species ||
                      "Not available"}
                  </strong>
                </div>

                <div>
                  <span>
                    Assembly
                  </span>

                  <strong>
                    {evidence.ensembl.assembly ||
                      "Not available"}
                  </strong>
                </div>

                <div>
                  <span>
                    Biotype
                  </span>

                  <strong>
                    {evidence.ensembl.biotype ||
                      "Not available"}
                  </strong>
                </div>

                <div>
                  <span>
                    Felidae orthologs
                  </span>

                  <strong>
                    {evidence.ensembl.metrics
                      ?.ortholog_count ??
                      "Not available"}
                  </strong>
                </div>

                <div>
                  <span>
                    One-to-one orthologs
                  </span>

                  <strong>
                    {evidence.ensembl.metrics
                      ?.one_to_one_count ??
                      "Not available"}
                  </strong>
                </div>

                <div>
                  <span>
                    Mean protein identity
                  </span>

                  <strong>
                    {evidence.ensembl.metrics
                      ?.mean_percent_identity != null
                      ? `${evidence.ensembl.metrics.mean_percent_identity}%`
                      : "Not available"}
                  </strong>
                </div>
                
                {/* VISUAL METRICS */}
                <div className="metric-cards">

                  <div className="metric-card">
                    <span>Felidae orthologs</span>
                    <strong>
                      {evidence.ensembl.metrics?.ortholog_count ?? "—"}
                    </strong>
                  </div>

                  <div className="metric-card">
                    <span>One-to-one orthologs</span>
                    <strong>
                      {evidence.ensembl.metrics?.one_to_one_count ?? "—"}
                    </strong>
                  </div>

                  <div className="metric-card">
                    <span>Mean protein identity</span>
                    <strong>
                      {evidence.ensembl.metrics?.mean_percent_identity != null
                        ? `${evidence.ensembl.metrics.mean_percent_identity}%`
                        : "—"}
                    </strong>
                  </div>

                </div>

                <div>
                  <span>
                    Identity range
                  </span>

                  <strong>
                    {evidence.ensembl.metrics
                      ? `${evidence.ensembl.metrics.min_percent_identity}% – ${evidence.ensembl.metrics.max_percent_identity}%`
                      : "Not available"}
                  </strong>
                </div>

              </div>

            </section>

          )}


          {/* ORTHOLOGS */}

          {evidence.ensembl?.orthologs && (

            <section className="result-card">

              <p className="eyebrow">
                FELIDAE ORTHOLOGS
              </p>

              <h2>
                Comparative evidence
              </h2>

              {evidence.ensembl.orthologs.length > 0 ? (

                <div className="table-wrapper">

                  <table>

                    <thead>

                      <tr>
                        <th>
                          Species
                        </th>

                        <th>
                          Identity
                        </th>

                        <th>
                          Positive
                        </th>

                        <th>
                          Type
                        </th>
                      </tr>

                    </thead>

                    <tbody>

                      {evidence.ensembl.orthologs.map(
                        (ortholog) => (

                          <tr
                            key={
                              ortholog.gene_id ||
                              ortholog.species
                            }
                          >

                            <td>
                              {ortholog.species}
                            </td>

                            <td>
                              {ortholog.percent_identity != null
                                ? `${ortholog.percent_identity}%`
                                : "—"}
                            </td>

                            <td>
                              {ortholog.percent_positive != null
                                ? `${ortholog.percent_positive}%`
                                : "—"}
                            </td>

                            <td>
                              {ortholog.orthology_type ||
                                "—"}
                            </td>

                          </tr>

                        )
                      )}

                    </tbody>

                  </table>

                </div>

              ) : (

                <p className="source-note">
                  No Felidae orthologues were found.
                </p>

              )}

              <p className="source-note">
                Source:{" "}
                {evidence.ensembl.source ||
                  "Ensembl Compara"}
              </p>

            </section>

          )}


          {/* UNIPROT */}

          {evidence.uniprot && (

            <section className="result-card">

              <p className="eyebrow">
                UNIPROT PROTEIN EVIDENCE
              </p>

              <h2>
                Protein annotation
              </h2>

              {evidence.uniprot.found ? (

                <>

                  <div className="evidence-grid">

                    <div>
                      <span>
                        Accession
                      </span>

                      <strong>
                        {evidence.uniprot.accession ||
                          "Not available"}
                      </strong>
                    </div>

                    <div>
                      <span>
                        Entry name
                      </span>

                      <strong>
                        {evidence.uniprot.entry_name ||
                          "Not available"}
                      </strong>
                    </div>

                    <div>
                      <span>
                        Organism
                      </span>

                      <strong>
                        {evidence.uniprot.organism ||
                          "Not available"}
                      </strong>
                    </div>

                    <div>
                      <span>
                        Protein length
                      </span>

                      <strong>
                        {evidence.uniprot.length != null
                          ? `${evidence.uniprot.length} aa`
                          : "Not available"}
                      </strong>
                    </div>

                    {evidence.uniprot.reviewed != null && (

                      <div>

                        <span>
                          Database status
                        </span>

                        <strong>
                          {evidence.uniprot.reviewed
                            ? "Reviewed · Swiss-Prot"
                            : "Unreviewed · TrEMBL"}
                        </strong>

                      </div>

                    )}

                    <div>
                      <span>
                        Source
                      </span>

                      <strong>
                        {evidence.uniprot.source ||
                          "UniProt"}
                      </strong>
                    </div>

                  </div>


                  {evidence.uniprot.protein_name && (

                    <div className="text-block">

                      <span>
                        Protein
                      </span>

                      <p>
                        {evidence.uniprot.protein_name}
                      </p>

                    </div>

                  )}


                  {evidence.uniprot.function && (

                    <div className="text-block">

                      <span>
                        Function
                      </span>

                      <p>
                        {evidence.uniprot.function}
                      </p>

                    </div>

                  )}


                  {evidence.uniprot.keywords &&
                    evidence.uniprot.keywords.length > 0 && (

                    <div className="text-block">

                      <span>
                        Keywords
                      </span>

                      <div className="keyword-list">

                        {evidence.uniprot.keywords.map(
                          (keyword) => (

                            <span
                              className="keyword"
                              key={keyword}
                            >
                              {keyword}
                            </span>

                          )
                        )}

                      </div>

                    </div>

                  )}

                </>

              ) : (

                <div className="empty-state">

                  <p>
                    No UniProt record was found for
                    this species/gene combination.
                  </p>

                </div>

              )}

            </section>

          )}

        </>
      )}


      {/* -------------------------------- */}
      {/* DISCLAIMER */}
      {/* -------------------------------- */}

      <p className="disclaimer">

        BioFelid AI is a research-support prototype.
        It does not predict extinction risk or replace
        expert conservation assessment.

      </p>

    </main>
  );
}

export default App;