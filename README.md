# BioFelid AI

> **AI-powered conservation genomics platform for endangered Felidae research.**

BioFelid AI is an AI-assisted conservation genomics platform that helps researchers explore genomic evidence across endangered and threatened Felidae species.

Instead of manually consulting multiple biological databases, BioFelid AI integrates genomic, protein, and comparative genomics evidence into a single interface, allowing researchers to rapidly inspect candidate genes for conservation research.

The platform currently integrates **NCBI Gene**, **UniProt**, and **Ensembl Compara**, providing a unified workflow for biological evidence exploration.

---

# Demo

**Video demonstration**

https://drive.google.com/file/d/1HdIK5Y50C5mhtJzxmMRssSvglmbmw9q4/view?usp=drive_link

---

# The Problem

Conservation genomics research requires scientists to gather information from numerous independent biological databases.

To evaluate a single candidate gene, researchers often need to manually inspect:

- genomic annotation
- protein annotation
- comparative genomics
- ortholog conservation
- species information

This process is repetitive, fragmented, and time-consuming.

BioFelid AI simplifies this workflow by automatically aggregating biological evidence into a single interface.

---

# How It Works

```text
Select a Felidae species
          │
          ▼
Search a candidate gene
          │
          ▼
Retrieve biological evidence
 ├── NCBI Gene
 ├── UniProt
 └── Ensembl Compara
          │
          ▼
Integrated evidence report
```

---

# Features

- Interactive Felidae species selector
- Conservation status displayed for every species
- Intelligent gene search powered by NCBI Gene
- Automatic retrieval of genomic annotations
- Protein information from UniProt
- Comparative genomics using Ensembl Compara
- Felidae ortholog analysis
- Protein identity metrics across species
- Fast React interface
- FastAPI backend
- Modular architecture designed for future expansion

---

# Built with IBM Bob

BioFelid AI was developed with **IBM Bob** as the primary AI-assisted software engineering partner.

Throughout development, IBM Bob assisted with:

- application architecture
- backend implementation
- frontend development
- API integration
- debugging
- refactoring
- testing
- documentation
- iterative feature development

The scientific rationale, biological interpretation, software architecture, and implementation decisions were continuously refined during development with IBM Bob acting as an AI development assistant.

---

# IBM Challenge Alignment

## Wildcard — Build Intelligent Systems for the Future of Work

BioFelid AI is designed as an intelligent assistant for conservation genomics research.

Instead of replacing researchers, it augments scientific workflows by automatically collecting and organizing biological evidence from multiple authoritative databases.

The platform helps researchers:

- reduce repetitive evidence gathering
- integrate heterogeneous biological data
- rapidly inspect candidate genes
- compare comparative genomics evidence
- focus human expertise on biological interpretation rather than manual data collection

BioFelid AI is intended to support scientific decision-making, not replace expert judgment.

---

# Architecture

```text
                React Frontend
                       │
                       ▼
                FastAPI Backend
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
 NCBI Gene        UniProt REST     Ensembl REST
```

---

# Tech Stack

| Layer | Technology |
|--------|------------|
| Frontend | React 19 |
| Build Tool | Vite |
| Backend | FastAPI |
| Language | Python 3.14 |
| APIs | NCBI Datasets |
| APIs | UniProt REST |
| APIs | Ensembl REST |
| AI Development | IBM Bob |

---

# Project Structure

```
BioFelid-AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── data_sources/
│   │   │   ├── ncbi.py
│   │   │   ├── uniprot.py
│   │   │   ├── ensembl.py
│   │   │   ├── taxonomy.py
│   │   │   └── iucn.py
│   │   ├── models/
│   │   ├── scoring/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── App.css
    │   └── assets/
    ├── package.json
    └── vite.config.js
```

---

# Getting Started

## Requirements

- Python 3.12+
- Node.js 18+

---

## Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
# source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

API documentation:

```
http://127.0.0.1:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Application:

```
http://localhost:5173
```

---

# API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/species` | Retrieve Felidae species |
| GET | `/api/genes` | Search genes using NCBI |
| GET | `/api/analyze` | Multi-source biological evidence |
| GET | `/health` | Health check |

---

# Current Evidence Sources

BioFelid AI currently integrates information from:

- NCBI Gene
- UniProt
- Ensembl Compara

These sources provide:

- genomic annotation
- chromosome location
- exon counts
- protein annotation
- protein function
- comparative genomics
- Felidae orthologs
- protein identity metrics

---

# Future Work

Planned future versions include:

- Biological pathway enrichment
- Automated literature mining
- Gene interaction networks
- Variant pathogenicity evidence
- Functional conservation scoring
- AI-assisted biological interpretation
- Exportable research reports

---

# Limitations

BioFelid AI is a research-support platform.

It aggregates publicly available biological evidence but **does not perform clinical interpretation, disease diagnosis, or extinction risk prediction.**

Results should be interpreted as research-support information rather than definitive biological conclusions.

External database availability may also affect individual analyses.

---

# License

MIT License
