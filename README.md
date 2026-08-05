# BioFelid AI

AI-assisted genomic prioritization tool for threatened felid conservation.

BioFelid AI aggregates evidence from **NCBI Gene**, **UniProt**, and **Ensembl** to help researchers identify which genes in endangered or critically-threatened Felidae species deserve deeper experimental investigation. A custom scoring algorithm — the **BioFelid Research Priority Score (BRPS)** — synthesises threat status, conservation signals, functional relevance, variant evidence, and literature signals into a single actionable priority tier.

---

## Features

- **Species selector** — pre-loaded list of Felidae species with IUCN threat status
- **Gene search** — live autocomplete backed by NCBI Gene (debounced, per-species)
- **Multi-source evidence** — NCBI genomic location, UniProt protein annotation, Ensembl ortholog conservation metrics
- **BRPS scoring** — outputs a 0–100 score and a tier: *Exploratory*, *Moderate*, or *High Priority*

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, Vite 8 |
| Backend | FastAPI 0.141, Python 3.14 |
| External APIs | NCBI Datasets, UniProt REST, Ensembl REST |

---

## Project Structure

```
BioFelid-AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # /api/analyze, /api/genes, /api/species
│   │   ├── data_sources/
│   │   │   ├── ncbi.py            # NCBI Gene evidence
│   │   │   ├── uniprot.py         # UniProt protein evidence
│   │   │   ├── ensembl.py         # Ensembl ortholog evidence
│   │   │   ├── taxonomy.py        # Felidae species list
│   │   │   └── iucn.py            # IUCN threat status helpers
│   │   ├── models/
│   │   │   └── evidence.py        # Pydantic models
│   │   ├── scoring/
│   │   │   └── brps.py            # BRPS scoring algorithm
│   │   └── main.py                # FastAPI app entry point
│   ├── tests/
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx                # Main UI component
    │   └── App.css
    ├── index.html
    └── package.json
```

---

## Getting Started

### Prerequisites

- Python ≥ 3.12
- Node.js ≥ 18

### Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Run the development server
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs: `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/species` | List all Felidae species |
| `GET` | `/api/genes?species=&query=` | Search genes for a species (NCBI) |
| `GET` | `/api/analyze?species=&gene=` | Full multi-source evidence + BRPS score |
| `GET` | `/health` | Health check |

---

## BRPS Algorithm

The **BioFelid Research Priority Score** is calculated as:

| Component | Max points |
|---|---|
| IUCN Threat Status (LC→CR) | 0–20 |
| Conservation score | 0–25 |
| Functional relevance | 0–20 |
| Variant evidence | 0–15 |
| Literature signal | 0–20 |
| **Total** | **0–100** |

Tiers: **< 35** → Exploratory · **35–64** → Moderate · **≥ 65** → High Priority

---

## Running Tests

```bash
cd backend
pytest
```

---

## License

MIT
