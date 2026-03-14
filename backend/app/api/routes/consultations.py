from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from app.database.session import get_db
from app.models.analysis import Consultation
from app.models.user import User
from app.api.routes.auth import get_current_user

router = APIRouter()


class ConsultationCreate(BaseModel):
    doctor_name: str
    summary: str
    diagnoses: list = []
    medications_prescribed: list = []


def _serialize(c: Consultation) -> dict:
    return {
        "id": str(c.id),
        "doctor_name": c.doctor_name,
        "summary": c.summary,
        "diagnoses": c.diagnoses,
        "medications_prescribed": c.medications_prescribed,
        "consultation_date": c.consultation_date.isoformat(),
    }


@router.post("/")
async def create_consultation(
    data: ConsultationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    c = Consultation(
        user_id=current_user.id,
        doctor_name=data.doctor_name,
        summary=data.summary,
        diagnoses=data.diagnoses,
        medications_prescribed=data.medications_prescribed,
        consultation_date=datetime.utcnow(),
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return _serialize(c)


@router.get("/")
async def list_consultations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Consultation)
        .filter(Consultation.user_id == current_user.id)
        .order_by(Consultation.consultation_date.desc())
        .all()
    )
    return [_serialize(c) for c in rows]
