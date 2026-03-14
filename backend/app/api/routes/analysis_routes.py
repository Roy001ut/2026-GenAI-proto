import uuid as uuid_module
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.database.session import get_db
from app.models.document import Document
from app.models.analysis import DrugAnalysis, BillAnalysis, InsuranceAnalysis
from app.models.user import User
from app.services.drug_service import DrugService
from app.services.bill_service import BillService
from app.services.insurance_service import InsuranceService
from app.api.routes.auth import get_current_user

router = APIRouter()


class DrugAnalysisRequest(BaseModel):
    drug_name: str
    dosage: str


class BillAnalysisRequest(BaseModel):
    document_id: str
    patient_diagnosis: Optional[str] = None


class InsuranceAnalysisRequest(BaseModel):
    document_id: str


def _get_document(db: Session, document_id: str) -> Document:
    try:
        doc_uuid = uuid_module.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid document ID")
    doc = db.query(Document).filter(Document.id == doc_uuid).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.post("/drug")
async def analyze_drug(
    request: DrugAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    analysis = DrugService.analyze_drug(request.drug_name, request.dosage)
    db.add(DrugAnalysis(
        user_id=current_user.id,
        drug_name=request.drug_name,
        dosage=request.dosage,
        what_is_it=analysis.get("what_is_it", ""),
        treats=analysis.get("treats", []),
        side_effects=analysis.get("side_effects", []),
        insurance_coverage=analysis.get("insurance_coverage", {}),
        alternate_salts=analysis.get("generic_available", False),
        red_flags=analysis.get("red_flags", []),
    ))
    db.commit()
    return analysis


@router.post("/bill")
async def analyze_bill(
    request: BillAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = _get_document(db, request.document_id)
    analysis = BillService.analyze_bill(doc.raw_text, request.patient_diagnosis)
    db.add(BillAnalysis(
        user_id=current_user.id,
        document_id=doc.id,
        charges=analysis.get("charges", []),
        red_flags=analysis.get("red_flags", []),
        fraud_risk_score=analysis.get("fraud_risk_score", 0),
    ))
    db.commit()
    return analysis


@router.post("/insurance")
async def analyze_insurance(
    request: InsuranceAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = _get_document(db, request.document_id)
    analysis = InsuranceService.parse_insurance_policy(doc.raw_text)
    db.add(InsuranceAnalysis(
        user_id=current_user.id,
        document_id=doc.id,
        provider_name=analysis.get("provider_name", ""),
        deductible=analysis.get("deductible", {}),
        copays=analysis.get("copays", {}),
        coverage_breakdown=analysis.get("coverage", {}),
    ))
    db.commit()
    return analysis
