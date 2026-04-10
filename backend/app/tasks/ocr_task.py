import uuid
from datetime import datetime, timedelta
from sqlalchemy import select
from . import celery_app
from app.database import AsyncSessionLocal
from app.models.statement import Statement
from app.models.pending_review import PendingReview
from app.services.ocr_service import run_ocr
from app.services.parser_service import parse_transactions
from app.services.storage_service import compute_file_hash
from app.core.config import settings


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
async def process_statement(self, statement_id: str):
    async with AsyncSessionLocal() as db:
        # Fetch statement
        result = await db.execute(select(Statement).where(Statement.id == statement_id))
        statement = result.scalar_one_or_none()
        if not statement:
            raise ValueError(f"Statement {statement_id} not found")

        try:
            statement.status = "processing"
            await db.commit()

            # Determine file path
            if statement.file_url.startswith("s3://"):
                # Download from S3 to temporary location (simplified: assume local fallback)
                raise NotImplementedError("S3 download not implemented in MVP")
            else:
                file_path = statement.file_url

            # Run OCR
            text = run_ocr(file_path)

            # Parse transactions
            transactions = parse_transactions(text)

            # Prepare raw_transactions (list of dicts with ISO strings for dates)
            raw_transactions = []
            for t in transactions:
                raw_transactions.append({
                    "date": t["date"].isoformat() if hasattr(t["date"], "isoformat") else str(t["date"]),
                    "description": t["description"],
                    "mutation_amount": str(t["mutation_amount"]),
                    "type": t["type"],
                    "balance": str(t["balance"]),
                    "category": None,
                })

            # Create PendingReview
            pending = PendingReview(
                statement_id=statement.id,
                raw_transactions=raw_transactions,
                validation_token=uuid.uuid4(),
                expires_at=datetime.utcnow() + timedelta(hours=24),
            )
            db.add(pending)
            statement.status = "extracted"
            await db.commit()

        except Exception as exc:
            statement.status = "error"
            await db.commit()
            raise self.retry(exc=exc)
