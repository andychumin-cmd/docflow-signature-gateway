from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

engine = create_engine("sqlite:///docflow.db", echo=False)
Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department = Column(String, default="Отдел")
    is_active = Column(Boolean, default=True)
    keys = relationship("PublicKey", back_populates="employee")

class PublicKey(Base):
    __tablename__ = "public_keys"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    key_fingerprint = Column(String, unique=True, nullable=False)
    key_id = Column(String, nullable=False)
    armored_key = Column(Text, nullable=False)
    valid_from = Column(DateTime, default=datetime.utcnow)
    valid_to = Column(DateTime, nullable=True)
    revoked = Column(Boolean, default=False)
    employee = relationship("Employee", back_populates="keys")

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    direction = Column(String, CheckConstraint("direction IN ('in','out')"), nullable=False)
    filename = Column(String, nullable=False)
    file_hash = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class SignatureCheck(Base):
    __tablename__ = "signature_checks"
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    key_id = Column(Integer, ForeignKey("public_keys.id"), nullable=True)
    signature_file = Column(String, nullable=False)
    status = Column(String, CheckConstraint("status IN ('valid','invalid','unknown_key','missing_sig')"), nullable=False)
    details = Column(Text)
    checked_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
