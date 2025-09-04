from api.app.main import app  # noqa: F401 - ensures startup runs
from api.app.database import SessionLocal
from api.app import models


def test_default_admin_created():
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email == "labelcraft").first()
        assert user is not None
    finally:
        db.close()
