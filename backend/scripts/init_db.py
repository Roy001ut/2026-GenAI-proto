#!/usr/bin/env python3
"""
Initialize the MedAudit database and seed a test user.

Usage (from backend/ directory):
    python -m scripts.init_db
    python -m scripts.init_db --reset   # drop and recreate all tables first
"""
import sys
import argparse
import uuid

# Ensure the backend package is importable when run from the backend/ directory
sys.path.insert(0, ".")

import bcrypt
from sqlalchemy import text
from app.database.session import engine
from app.database.base import Base

# Import all models so SQLAlchemy knows about them
from app.models.user import User
from app.models.document import Document
from app.models.analysis import (
    DrugAnalysis, BillAnalysis, InsuranceAnalysis, LabReport, Consultation
)
from app.database.session import SessionLocal

# ── Test credentials ──────────────────────────────────────────────────────────
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "test123"
TEST_FULL_NAME = "Test User"
# ─────────────────────────────────────────────────────────────────────────────


def create_tables(reset: bool = False) -> None:
    if reset:
        print("Dropping all tables…")
        Base.metadata.drop_all(bind=engine)
    print("Creating tables…")
    Base.metadata.create_all(bind=engine)


def seed_test_user(db) -> User:
    existing = db.query(User).filter(User.email == TEST_EMAIL).first()
    if existing:
        print(f"Test user already exists: {TEST_EMAIL}")
        return existing

    hashed = bcrypt.hashpw(TEST_PASSWORD.encode(), bcrypt.gensalt()).decode()
    user = User(
        id=uuid.uuid4(),
        email=TEST_EMAIL,
        password_hash=hashed,
        full_name=TEST_FULL_NAME,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created test user: {TEST_EMAIL}")
    return user


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize MedAudit database")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate all tables")
    args = parser.parse_args()

    create_tables(reset=args.reset)

    db = SessionLocal()
    try:
        user = seed_test_user(db)
    finally:
        db.close()

    print()
    print("=" * 50)
    print("  Database initialized successfully")
    print("=" * 50)
    print(f"  User ID  : {user.id}")
    print(f"  Email    : {TEST_EMAIL}")
    print(f"  Password : {TEST_PASSWORD}")
    print("=" * 50)


if __name__ == "__main__":
    main()
