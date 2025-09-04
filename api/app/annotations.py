import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models
from .deps import get_db, get_current_user

router = APIRouter(prefix="/api/v1/images", tags=["annotations"])


@router.get("/{image_id}/annotations")
def get_annotations(image_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    image = db.query(models.ImageAsset).get(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    ann = db.query(models.Annotation).filter(models.Annotation.image_id == image_id).all()
    return [json.loads(a.data) | {"id": a.id, "class_id": a.class_id} for a in ann]


@router.post("/{image_id}/annotations")
def upsert_annotations(image_id: int, items: list[dict], db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    image = db.query(models.ImageAsset).get(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    for item in items:
        if "id" in item:
            ann = db.query(models.Annotation).get(item["id"])
            if not ann:
                continue
            if item.get("version", 0) != ann.version:
                raise HTTPException(status_code=409, detail="Version mismatch")
            ann.data = json.dumps(item)
            ann.version += 1
        else:
            ann = models.Annotation(image_id=image_id, class_id=item["class_id"], data=json.dumps(item))
            db.add(ann)
    db.commit()
    return {"status": "ok"}
