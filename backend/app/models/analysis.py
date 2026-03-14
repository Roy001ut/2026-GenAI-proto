from sqlalchemy import Column, String, Text, Numeric, Integer, DateTime, ForeignKey, func, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.database.base import Base


class DrugAnalysis(Base):
    __tablename__ = "drug_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    drug_name = Column(String(255), nullable=False)
    dosage = Column(String(100))
    frequency = Column(String(100))
    what_is_it = Column(Text)
    treats = Column(JSONB, default=[])
    side_effects = Column(JSONB, default=[])
    insurance_coverage = Column(JSONB, default={})
    alternate_salts = Column(JSONB, default=[])
    red_flags = Column(JSONB, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BillAnalysis(Base):
    __tablename__ = "bill_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    bill_provider = Column(String(255))
    total_amount = Column(Numeric(10, 2))
    charges = Column(JSONB, default=[])
    red_flags = Column(JSONB, default=[])
    fraud_risk_score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InsuranceAnalysis(Base):
    __tablename__ = "insurance_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    provider_name = Column(String(255))
    premium_amount = Column(Numeric(10, 2))
    deductible = Column(JSONB, default={})
    copays = Column(JSONB, default={})
    coverage_breakdown = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LabReport(Base):
    __tablename__ = "lab_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
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

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    doctor_name = Column(String(255))
    raw_transcript = Column(Text)
    summary = Column(Text)
    diagnoses = Column(JSONB, default=[])
    medications_prescribed = Column(JSONB, default=[])
    tests_ordered = Column(JSONB, default=[])
    action_items = Column(JSONB, default=[])
    consultation_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
