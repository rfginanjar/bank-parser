import hashlib
import os
from fastapi import UploadFile
from app.core.config import settings
import boto3
from botocore.exceptions import ClientError

UPLOAD_DIR = "uploads"


async def compute_file_hash(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()


async def save_upload_file(upload_file: UploadFile) -> tuple[str, str]:
    """Save file to storage (S3 or local). Returns (file_path, file_hash)."""
    contents = await upload_file.read()
    file_hash = await compute_file_hash(contents)

    if settings.storage_type == "s3":
        s3 = boto3.client(
            "s3",
            region_name=settings.s3_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        s3_key = f"uploads/{file_hash}{os.path.splitext(upload_file.filename)[1]}"
        s3.put_object(
            Bucket=settings.s3_bucket,
            Key=s3_key,
            Body=contents,
            ContentType=upload_file.content_type,
        )
        file_path = f"s3://{settings.s3_bucket}/{s3_key}"
    else:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        filename = f"{file_hash}{os.path.splitext(upload_file.filename)[1]}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(contents)

    return file_path, file_hash
