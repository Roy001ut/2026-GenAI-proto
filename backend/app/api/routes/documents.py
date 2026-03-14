import uuid as uuid_module
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.database.session import get_db
from app.models.document import Document, DocumentType
from app.models.user import User
from app.services.document_service import DocumentService
from app.api.routes.auth import get_current_user

router = APIRouter()


@router.post("/upload/{document_type}")
async def upload_document(
    document_type: str,
    file: UploadFile = File(...),
    user_id: uuid_module.UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        doc_type = DocumentType[document_type.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid document type")

    try:
        file_path = await DocumentService.save_file(file, str(user_id))
        raw_text = await DocumentService.extract_text(file_path, file.content_type)

        document = Document(
            user_id=user_id,
            document_type=doc_type,
            original_filename=file.filename,
            file_path=file_path,
            raw_text=raw_text
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        return {"id": str(document.id), "filename": file.filename, "status": "uploaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def list_documents(
    user_id: uuid_module.UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    documents = db.query(Document).filter(Document.user_id == user_id).all()
    return [{"id": str(d.id), "document_type": d.document_type.value, "original_filename": d.original_filename} for d in documents]


@router.get("/{document_id}")
async def get_document(
    document_id: str,
    user_id: uuid_module.UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        doc_uuid = uuid_module.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid document ID")

    document = db.query(Document).filter(
        Document.id == doc_uuid,
        Document.user_id == user_id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"id": str(document.id), "document_type": document.document_type.value, "original_filename": document.original_filename}


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    user_id: uuid_module.UUID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        doc_uuid = uuid_module.UUID(document_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid document ID")

    document = db.query(Document).filter(
        Document.id == doc_uuid,
        Document.user_id == user_id
    ).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    db.delete(document)
    db.commit()
    return {"status": "deleted"}
