from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base

# Import all models so SQLAlchemy knows about every table
import app.models  # noqa: F401

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedAudit API",
    description="AI-Powered Medical Analysis System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.routes import auth, documents, analysis_routes, health_wallet, consultations  # noqa: E402

app.include_router(auth.router,             prefix="/api/auth",         tags=["auth"])
app.include_router(documents.router,        prefix="/api/documents",    tags=["documents"])
app.include_router(analysis_routes.router,  prefix="/api/analysis",     tags=["analysis"])
app.include_router(health_wallet.router,    prefix="/api/health-wallet", tags=["health-wallet"])
app.include_router(consultations.router,    prefix="/api/consultations", tags=["consultations"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
