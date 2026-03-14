from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging

from app.config import settings
from app.database.session import engine
from app.models import user, document, analysis
from app.api.routes import auth, documents, analysis_routes, health_wallet, consultations

# Create tables
user.User.metadata.create_all(bind=engine)
document.Document.metadata.create_all(bind=engine)
analysis.DrugAnalysis.metadata.create_all(bind=engine)
analysis.BillAnalysis.metadata.create_all(bind=engine)
analysis.InsuranceAnalysis.metadata.create_all(bind=engine)
analysis.LabReport.metadata.create_all(bind=engine)
analysis.Consultation.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MedAudit API",
    description="AI-Powered Medical Analysis System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok", "environment": settings.ENVIRONMENT}


# Include routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(analysis_routes.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(health_wallet.router, prefix="/api/health-wallet", tags=["health-wallet"])
app.include_router(consultations.router, prefix="/api/consultations", tags=["consultations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=(settings.ENVIRONMENT == "development")
    )
