import uuid as uuid_module
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.document import Document
from app.models.analysis import DrugAnalysis, BillAnalysis, InsuranceAnalysis
from app.models.user import User
from app.services import ai_service
from app.api.routes.auth import get_current_user

router = APIRouter()


class DrugRequest(BaseModel):
    drug_name: str
    dosage: str


class BillRequest(BaseModel):
    document_id: str
    patient_diagnosis: Optional[str] = None


class InsuranceRequest(BaseModel):
    document_id: str


def _get_doc(db: Session, document_id: str) -> Document:
    try:
        uid = uuid_module.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid document ID")
    doc = db.query(Document).filter(Document.id == uid).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.post("/drug")
async def analyze_drug(
    req: DrugRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = ai_service.analyze_drug(req.drug_name, req.dosage)
    db.add(DrugAnalysis(user_id=current_user.id, drug_name=req.drug_name, dosage=req.dosage, result=result))
    db.commit()
    return result


@router.post("/bill")
async def analyze_bill(
    req: BillRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = _get_doc(db, req.document_id)
    result = ai_service.analyze_bill(doc.raw_text or "", req.patient_diagnosis or "")
    db.add(BillAnalysis(user_id=current_user.id, document_id=doc.id, result=result))
    db.commit()
    return result


@router.post("/insurance")
async def analyze_insurance(
    req: InsuranceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = _get_doc(db, req.document_id)
    result = ai_service.analyze_insurance(doc.raw_text or "")
    db.add(InsuranceAnalysis(user_id=current_user.id, document_id=doc.id, result=result))
    db.commit()
    return result
