from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db, SessionLocal
from .security import get_password_hash
from . import auth, projects, datasets, annotations, models


def ensure_admin_user() -> None:
    """Create a default admin user if the database is empty."""
    db = SessionLocal()
    try:
        if db.query(models.User).count() == 0:
            admin = models.User(
                email="labelcraft", password_hash=get_password_hash("Asex1993")
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()


init_db()
ensure_admin_user()

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
