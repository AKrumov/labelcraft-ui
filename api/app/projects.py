from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .deps import get_db, get_current_user

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])


@router.post("/", response_model=schemas.ProjectOut)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_project = models.Project(name=project.name, owner_id=user.id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    # owner is automatically a member
    member = models.ProjectMember(project_id=db_project.id, user_id=user.id, role=models.RoleEnum.owner)
    db.add(member)
    db.commit()
    return db_project


@router.get("/", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    memberships = db.query(models.ProjectMember).filter(models.ProjectMember.user_id == user.id).all()
    project_ids = [m.project_id for m in memberships]
    return db.query(models.Project).filter(models.Project.id.in_(project_ids)).all()


@router.get("/{project_id}", response_model=schemas.ProjectDetailOut)
def get_project(project_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    membership = (
        db.query(models.ProjectMember)
        .filter_by(project_id=project_id, user_id=user.id)
        .first()
    )
    if not membership:
        raise HTTPException(status_code=403, detail="Not a project member")
    project = db.query(models.Project).get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
