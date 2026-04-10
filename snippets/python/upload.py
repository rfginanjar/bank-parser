from fastapi import UploadFile, HTTPException

async def upload_endpoint(file: UploadFile) -> dict:
    # save file to storage, record in files table
    # return {'file_id': str}
    raise HTTPException(500, 'Not implemented')
