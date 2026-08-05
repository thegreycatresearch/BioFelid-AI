from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BioFelid AI",
    description="AI-assisted genomic prioritization for threatened felid conservation",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {
        "project": "BioFelid AI",
        "status": "running",
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }