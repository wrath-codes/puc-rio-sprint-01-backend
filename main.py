import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.config.database import create_db
from src.routers import main_router

description = """
# API de Receitas

API para gerenciar receitas.

Usuários podem criar, editar, deletar e visualizar receitas.
Também podem criar, editar, deletar e visualizar ingredientes e passos das receitas.

## Endpoints
"""

tags_metadata = [
    {
        "name": "Docs",
        "description": "Redirect to docs.",
    },
    {
        "name": "Recipes",
        "description": "Operations with recipes.",
    },
    {
        "name": "Ingredients",
        "description": "Operations with ingredients.",
    },
    {
        "name": "Steps",
        "description": "Operations with steps.",
    },
]

# Create FastAPI app
app = FastAPI(description=description, openapi_tags=tags_metadata)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Include router
app.include_router(main_router, prefix="/api")


@app.get("/", tags=["Docs"])
def index():
    """Redirect to docs"""
    docs = RedirectResponse(url="/docs")
    return docs


if __name__ == "__main__":
    create_db()

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
