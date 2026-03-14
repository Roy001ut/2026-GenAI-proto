import uuid
from sqlalchemy import Column, String, Text, Numeric, Integer, DateTime, ForeignKey, Uuid, JSON, Date, func
from app.database import Base


class DrugAnalysis(Base):
    __tablename__ = "drug_analyses"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    drug_name = Column(String(255), nullable=False)
    dosage = Column(String(100))
    result = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BillAnalysis(Base):
    __tablename__ = "bill_analyses"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    document_id = Column(Uuid(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    result = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InsuranceAnalysis(Base):
    __tablename__ = "insurance_analyses"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    document_id = Column(Uuid(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    result = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LabReport(Base):
    __tablename__ = "lab_reports"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    test_name = Column(String(255), nullable=False)
    test_value = Column(Numeric(10, 2))
    unit = Column(String(50))
    normal_range_min = Column(Numeric(10, 2))
    normal_range_max = Column(Numeric(10, 2))
    status = Column(String(50))
    test_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    doctor_name = Column(String(255))
    summary = Column(Text)
    diagnoses = Column(JSON, default=list)
    medications_prescribed = Column(JSON, default=list)
    consultation_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
