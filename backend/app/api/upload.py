import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.account import Account
from app.models.statement import Statement
from app.services.storage_service import save_upload_file
from app.tasks.ocr_task import process_statement
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/upload", tags=["upload"])

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = ["application/pdf", "image/jpeg", "image/png", "image/tiff"]

@router.post("/")
async def upload_statement(
    file: UploadFile = File(...),
    account_id: uuid.UUID = Form(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Validate MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")
    # Read content for size check and then reset
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    # Reset file pointer so storage_service can read it again
    await file.seek(0)

    # Verify account exists and belongs to current user
    result = await db.execute(
        select(Account).where(Account.id == account_id, Account.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found or access denied")

    # Save file
    file_path, file_hash = await save_upload_file(file)

    # Create Statement record with current month/year as placeholder
    now = datetime.utcnow()
    statement = Statement(
        account_id=account.id,
        period_month=now.month,
        period_year=now.year,
        file_url=file_path,
        file_hash=file_hash,
        status="pending",
    )
    db.add(statement)
    await db.commit()
    await db.refresh(statement)

    # Enqueue OCR processing task
    process_statement.delay(str(statement.id))

    return {"statement_id": str(statement.id), "status": "pending"}
