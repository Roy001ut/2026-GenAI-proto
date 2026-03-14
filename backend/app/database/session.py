from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# SQLite needs check_same_thread=False; Postgres needs pool settings
is_sqlite = settings.DATABASE_URL.startswith("sqlite")
engine_kwargs: dict = {"echo": settings.ENVIRONMENT == "development"}
if is_sqlite:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs.update({"pool_pre_ping": True, "pool_size": 10, "max_overflow": 20})

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
