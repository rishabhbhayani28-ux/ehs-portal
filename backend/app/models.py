from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

# User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    incidents = relationship("Incident", back_populates="owner")

# Incident table
class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    date_reported = Column(DateTime, default=datetime.utcnow)
    reported_by_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="incidents")
    actions = relationship("Action", back_populates="incident")

# Action table (corrective / preventive action)
class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    status = Column(String, default="Open")  # Open, In Progress, Closed
    due_date = Column(DateTime, nullable=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))

    incident = relationship("Incident", back_populates="actions")
