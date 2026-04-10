from fastapi import APIRouter
from app.api.auth import router as auth_router
from app.api.upload import router as upload_router
from app.api.validation import router as validation_router
from app.api.dashboard import router as dashboard_router
from app.api.accounts import router as accounts_router
from app.api.transactions import router as transactions_router
from app.api.transactions_export import router as transactions_export_router
from app.api.categories import router as categories_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(upload_router)
api_router.include_router(validation_router)
api_router.include_router(dashboard_router)
api_router.include_router(accounts_router)
api_router.include_router(transactions_router)
api_router.include_router(transactions_export_router)
api_router.include_router(categories_router)
