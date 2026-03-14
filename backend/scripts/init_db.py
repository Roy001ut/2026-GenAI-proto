#!/usr/bin/env python3
"""
Initialize MedAudit database: create tables + seed test user.

Usage (from backend/ directory):
  python -m scripts.init_db           # create tables + seed
  python -m scripts.init_db --reset   # drop all, recreate, seed
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("CLAUDE_API_KEY", "placeholder")

from app.database import engine, Base, SessionLocal  # noqa: E402
import app.models  # noqa: F401  — registers all models with Base
from app.models.user import User  # noqa: E402
from app.services.auth_service import hash_password  # noqa: E402

TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "test123"
TEST_NAME = "Test User"


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize MedAudit database")
    parser.add_argument("--reset", action="store_true", help="Drop and recreate all tables")
    args = parser.parse_args()

    if args.reset:
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)

    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == TEST_EMAIL).first()
        if existing:
            print(f"Test user already exists: {TEST_EMAIL}")
            user = existing
        else:
            user = User(
                email=TEST_EMAIL,
                password_hash=hash_password(TEST_PASSWORD),
                full_name=TEST_NAME,
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Created test user: {TEST_EMAIL}")
    finally:
        db.close()

    print()
    print("=" * 50)
    print("  Database ready")
    print("=" * 50)
    print(f"  Email    : {TEST_EMAIL}")
    print(f"  Password : {TEST_PASSWORD}")
    print(f"  User ID  : {user.id}")
    print("=" * 50)


if __name__ == "__main__":
    main()
