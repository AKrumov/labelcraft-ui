from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Float
from sqlalchemy.orm import relationship
from .database import Base
import enum


class RoleEnum(str, enum.Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User")


class ProjectMember(Base):
    __tablename__ = "project_members"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(Enum(RoleEnum), default=RoleEnum.viewer)


class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class ImageAsset(Base):
    __tablename__ = "image_assets"
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    rel_path = Column(String, nullable=False)
    width = Column(Integer)
    height = Column(Integer)
    mime = Column(String)
    sha256 = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ClassLabel(Base):
    __tablename__ = "class_labels"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String, nullable=False)
    color = Column(String, default="#ffffff")
    keybind = Column(String, nullable=True)


class Annotation(Base):
    __tablename__ = "annotations"
    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("image_assets.id"))
    class_id = Column(Integer, ForeignKey("class_labels.id"))
    type = Column(String, default="box")  # box or polygon
    data = Column(Text)  # JSON string
    source = Column(String, default="human")
    confidence = Column(Float, nullable=True)
    version = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by = Column(Integer, ForeignKey("users.id"))
