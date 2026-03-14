from sqlalchemy import Column, String, Text, DateTime, Enum, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
import enum
from app.database.base import Base


class DocumentType(str, enum.Enum):
    PRESCRIPTION = "prescription"
    BILL = "bill"
    LAB_REPORT = "lab_report"
    CONSULTATION = "consultation"
    INSURANCE_POLICY = "insurance_policy"


class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    original_filename = Column(String(255))
    file_path = Column(String(255))
    raw_text = Column(Text)
    extracted_data = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Document {self.original_filename}>"
