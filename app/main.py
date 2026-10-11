
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router


app = FastAPI(
    title="ResearchCopilot API",
    description=(
        "An AI-powered research assistant that searches, "
        "analyzes, and summarizes research papers."
    ),
    version="1.0.0",
)

# Allow the local frontend to communicate with the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "null",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Welcome to ResearchCopilot",
        "docs": "/docs",
        "health": "/api/health",
    }
