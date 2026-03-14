from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from pydantic import BaseModel
from app.database.session import get_db
from app.models.analysis import LabReport
from app.models.user import User
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
    data: LabReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    status = "normal"
    if data.test_value < data.normal_range_min:
        status = "low"
    elif data.test_value > data.normal_range_max:
        status = "high"

    report = LabReport(
        user_id=current_user.id,
        test_name=data.test_name,
        test_value=data.test_value,
        unit=data.unit,
        normal_range_min=data.normal_range_min,
        normal_range_max=data.normal_range_max,
        status=status,
        test_date=data.test_date,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return {
        "id": str(report.id),
        "test_name": report.test_name,
        "test_value": float(report.test_value),
        "unit": report.unit,
        "status": report.status,
        "test_date": str(report.test_date),
    }


@router.get("/all-reports")
async def list_lab_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reports = (
        db.query(LabReport)
        .filter(LabReport.user_id == current_user.id)
        .order_by(LabReport.test_date.desc())
        .all()
    )
    grouped: dict = {}
    for r in reports:
        grouped.setdefault(r.test_name, []).append({
            "id": str(r.id),
            "test_value": float(r.test_value),
            "unit": r.unit,
            "status": r.status,
            "test_date": str(r.test_date),
        })
    return grouped


@router.get("/trends/{test_name}")
async def get_trends(
    test_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reports = (
        db.query(LabReport)
        .filter(LabReport.user_id == current_user.id, LabReport.test_name == test_name)
        .order_by(LabReport.test_date)
        .all()
    )
    if len(reports) < 2:
        return {"message": "Need at least 2 data points for trend analysis", "test_name": test_name}

    values = [float(r.test_value) for r in reports]
    direction = "stable"
    if values[-1] > values[0]:
        direction = "increasing"
    elif values[-1] < values[0]:
        direction = "decreasing"

    days = (reports[-1].test_date - reports[0].test_date).days
    rate = ((values[-1] - values[0]) / days * 30) if days > 0 else 0

    return {
        "test_name": test_name,
        "direction": direction,
        "rate_per_month": round(rate, 2),
        "baseline": values[0],
        "current": values[-1],
        "count": len(reports),
    }
