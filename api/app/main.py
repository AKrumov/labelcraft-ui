from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from . import auth, projects, datasets, annotations

init_db()

app = FastAPI(title="LabelCraft API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(datasets.router)
app.include_router(annotations.router)


@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}
