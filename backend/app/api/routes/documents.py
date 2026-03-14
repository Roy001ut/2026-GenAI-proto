import uuid as uuid_module
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Document, DocumentType
from app.models.user import User
from app.services import document_service
from app.api.routes.auth import get_current_user

router = APIRouter()


@router.post("/upload/{document_type}")
async def upload_document(
    document_type: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        doc_type = DocumentType[document_type.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid document type: {document_type}")
    file_path = await document_service.save_file(file, str(current_user.id))
    raw_text = await document_service.extract_text(file_path, file.content_type or "")
    doc = Document(
        user_id=current_user.id,
        document_type=doc_type,
        original_filename=file.filename,
        file_path=file_path,
        raw_text=raw_text,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"id": str(doc.id), "filename": file.filename, "type": doc_type.value, "status": "uploaded"}


@router.get("/")
async def list_documents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    docs = db.query(Document).filter(Document.user_id == current_user.id).all()
    return [
        {"id": str(d.id), "document_type": d.document_type.value, "original_filename": d.original_filename}
        for d in docs
    ]


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        uid = uuid_module.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid document ID")
    doc = db.query(Document).filter(Document.id == uid, Document.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"id": str(doc.id), "document_type": doc.document_type.value,
            "original_filename": doc.original_filename, "raw_text": doc.raw_text}


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        uid = uuid_module.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid document ID")
    doc = db.query(Document).filter(Document.id == uid, Document.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return {"status": "deleted"}
