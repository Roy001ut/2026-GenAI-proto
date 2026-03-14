import uuid as uuid_module
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel
from app.database.session import get_db
from app.models.analysis import LabReport
from app.api.routes.auth import get_current_user

router = APIRouter()


class LabReportCreate(BaseModel):
    test_name: str
    test_value: float
    unit: str
    normal_range_min: float
    normal_range_max: float
    test_date: date


@router.post("/lab-reports")
async def add_lab_report(
    lab_data: LabReportCreate,
    user_id: uuid_module.UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    status = "normal"
    if lab_data.test_value < lab_data.normal_range_min:
        status = "low"
    elif lab_data.test_value > lab_data.normal_range_max:
        status = "high"

    lab_report = LabReport(
        user_id=user_id,
        test_name=lab_data.test_name,
        test_value=lab_data.test_value,
        unit=lab_data.unit,
        normal_range_min=lab_data.normal_range_min,
        normal_range_max=lab_data.normal_range_max,
        status=status,
        test_date=lab_data.test_date
    )
    db.add(lab_report)
    db.commit()

    return lab_report


@router.get("/all-reports")
async def list_lab_reports(
    user_id: uuid_module.UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reports = db.query(LabReport).filter(
        LabReport.user_id == user_id
    ).order_by(LabReport.test_date.desc()).all()

    organized = {}
    for report in reports:
        if report.test_name not in organized:
            organized[report.test_name] = []
        organized[report.test_name].append(report)

    return organized


@router.get("/trends/{test_name}")
async def get_lab_trends(
    test_name: str,
    user_id: uuid_module.UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    reports = db.query(LabReport).filter(
        LabReport.user_id == user_id,
        LabReport.test_name == test_name
    ).order_by(LabReport.test_date).all()

    if len(reports) < 2:
        return {"message": "Need at least 2 reports for trend analysis", "test_name": test_name}

    values = [float(r.test_value) for r in reports]
    direction = "stable"
    if values[-1] > values[0]:
        direction = "improving"
    elif values[-1] < values[0]:
        direction = "declining"

    days_diff = (reports[-1].test_date - reports[0].test_date).days
    value_diff = values[-1] - values[0]
    rate_per_month = (value_diff / days_diff * 30) if days_diff > 0 else 0

    return {
        "test_name": test_name,
        "trend": {
            "direction": direction,
            "rate_of_change": round(rate_per_month, 2),
            "baseline": values[0],
            "current": values[-1],
            "count": len(reports)
        }
    }
