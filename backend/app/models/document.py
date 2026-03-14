import uuid
import enum
from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, Uuid, JSON, func
from app.database import Base


class DocumentType(str, enum.Enum):
    PRESCRIPTION = "prescription"
    BILL = "bill"
    LAB_REPORT = "lab_report"
    CONSULTATION = "consultation"
    INSURANCE_POLICY = "insurance_policy"


class Document(Base):
    __tablename__ = "documents"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    original_filename = Column(String(255))
    file_path = Column(String(255))
    raw_text = Column(Text)
    extracted_data = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
