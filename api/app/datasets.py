import os
import hashlib
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from PIL import Image
from . import models, schemas
from .deps import get_db, get_current_user

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

router = APIRouter(prefix="/api/v1/datasets", tags=["datasets"])


@router.post("/{project_id}", response_model=schemas.DatasetOut)
def create_dataset(project_id: int, dataset: schemas.DatasetCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    # ensure user has access to project
    membership = db.query(models.ProjectMember).filter_by(project_id=project_id, user_id=user.id).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not a project member")
    db_dataset = models.Dataset(project_id=project_id, name=dataset.name, description=dataset.description)
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset


@router.post("/{dataset_id}/upload", response_model=dict)
def upload_image(dataset_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    dataset = db.query(models.Dataset).get(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    membership = db.query(models.ProjectMember).filter_by(project_id=dataset.project_id, user_id=user.id).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not a project member")
    content = file.file.read()
    sha = hashlib.sha256(content).hexdigest()
    ext = Path(file.filename).suffix
    rel_dir = Path("images") / str(dataset.project_id) / str(dataset.id) / sha[:2]
    abs_dir = DATA_DIR / rel_dir
    abs_dir.mkdir(parents=True, exist_ok=True)
    rel_path = rel_dir / f"{sha}{ext}"
    abs_path = DATA_DIR / rel_path
    with open(abs_path, "wb") as f:
        f.write(content)
    width = height = None
    try:
        with Image.open(abs_path) as im:
            width, height = im.size
    except Exception:
        pass
    image = models.ImageAsset(dataset_id=dataset.id, rel_path=str(rel_path), width=width, height=height, mime=file.content_type, sha256=sha)
    db.add(image)
    db.commit()
    db.refresh(image)
    return {"id": image.id, "rel_path": image.rel_path}
