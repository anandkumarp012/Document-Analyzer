
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, DocumentAnalysis, init_db
from model import predict_category
from document_utils import (
    extract_text_from_pdf,
    extract_text_from_txt,
    generate_summary,
    extract_keywords,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AI-Powered Document Analyzer",
    description="Upload and analyze PDF or TXT documents using machine learning.",
    version="1.0.0",
    lifespan=lifespan,
)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


@app.get("/")
def home():
    return {
        "message": "AI-Powered Document Analyzer API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/documents/analyze")
async def analyze_document(file: UploadFile = File(...)):
    filename = file.filename or ""
    extension = filename.lower().rsplit(".", 1)

    try:
        if len(extension) != 2 or extension[1] not in {"pdf", "txt"}:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and TXT files are supported.",
            )

        content = await file.read(MAX_FILE_SIZE + 1)

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File exceeds the 5 MB limit.",
            )

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        if extension[1] == "pdf":
            text = extract_text_from_pdf(content)
        else:
            text = extract_text_from_txt(content)

        category = predict_category(text)
        summary = generate_summary(text)
        keywords = extract_keywords(text)

        db = SessionLocal()

        try:
            record = DocumentAnalysis(
                filename=filename,
                category=category,
                summary=summary,
                keywords=json.dumps(keywords),
                character_count=len(text),
            )

            db.add(record)
            db.commit()
            db.refresh(record)

            return {
                "id": record.id,
                "filename": record.filename,
                "category": record.category,
                "summary": record.summary,
                "keywords": keywords,
                "character_count": record.character_count,
                "created_at": record.created_at.isoformat(),
            }

        except Exception as exc:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Failed to save document analysis.",
            ) from exc

        finally:
            db.close()

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    finally:
        await file.close()


@app.get("/documents/history")
def get_document_history():
    db = SessionLocal()

    try:
        records = (
            db.query(DocumentAnalysis)
            .order_by(DocumentAnalysis.id.desc())
            .limit(100)
            .all()
        )

        return [
            {
                "id": record.id,
                "filename": record.filename,
                "category": record.category,
                "summary": record.summary,
                "keywords": json.loads(record.keywords),
                "character_count": record.character_count,
                "created_at": record.created_at.isoformat(),
            }
            for record in records
        ]

    finally:
        db.close()
