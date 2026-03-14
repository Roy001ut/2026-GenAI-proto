from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.database.session import get_db
from app.models.analysis import Consultation
from app.api.routes.auth import get_current_user

router = APIRouter()


class ConsultationCreate(BaseModel):
    doctor_name: str
    summary: str
    diagnoses: list = []
    medications_prescribed: list = []


@router.post("/")
async def create_consultation(
    data: ConsultationCreate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    user_id = await get_current_user(authorization, db)

    consultation = Consultation(
        user_id=user_id,
        doctor_name=data.doctor_name,
        summary=data.summary,
        diagnoses=data.diagnoses,
        medications_prescribed=data.medications_prescribed,
        consultation_date=datetime.utcnow()
    )
    db.add(consultation)
    db.commit()

    return consultation


@router.get("/")
async def list_consultations(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    user_id = await get_current_user(authorization, db)

    consultations = db.query(Consultation).filter(
        Consultation.user_id == user_id
    ).order_by(Consultation.consultation_date.desc()).all()

    return consultations
