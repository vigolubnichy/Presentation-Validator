from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

Base = declarative_base()

class Validation(Base):
    __tablename__ = "validations"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    issues = relationship("Issue", back_populates="validation")

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    validation_id = Column(Integer, ForeignKey("validations.id"))
    slide_number = Column(Integer)
    rule = Column(String)
    message = Column(String)

    validation = relationship("Validation", back_populates="issues")
