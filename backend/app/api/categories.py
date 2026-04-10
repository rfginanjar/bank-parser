from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, exc
from app.database import get_db
from app.models.category import Category
from app.core.auth import get_current_user
from app.models.user import User
from uuid import UUID

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/")
async def list_categories(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Category).where(
        (Category.user_id == current_user.id) | (Category.is_default == True)
    )
    result = await db.execute(stmt)
    categories = result.scalars().all()
    return [
        {
            "id": str(cat.id),
            "name": cat.name,
            "color": cat.color,
            "is_default": cat.is_default
        }
        for cat in categories
    ]

@router.post("/")
async def create_category(
    name: str = Body(..., embed=True),
    color: str = Body(..., embed=True),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not color.startswith("#") or len(color) not in (4, 7):
        raise HTTPException(status_code=400, detail="Invalid color format")
    # Check duplicate name for this user
    stmt = select(Category).where(
        Category.name == name,
        Category.user_id == current_user.id
    )
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Category name already exists")
    cat = Category(name=name, color=color, is_default=False, user_id=current_user.id)
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return {
        "id": str(cat.id),
        "name": cat.name,
        "color": cat.color,
        "is_default": cat.is_default
    }

@router.put("/{category_id}")
async def update_category(
    category_id: UUID,
    name: str = Body(None, embed=True),
    color: str = Body(None, embed=True),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Category).where(
        Category.id == category_id,
        Category.user_id == current_user.id,
        Category.is_default == False
    )
    result = await db.execute(stmt)
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found or not editable")
    if name:
        # Check duplicate name for this user (excluding current)
        stmt2 = select(Category).where(
            Category.name == name,
            Category.user_id == current_user.id,
            Category.id != category_id
        )
        result2 = await db.execute(stmt2)
        if result2.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Category name already exists")
        cat.name = name
    if color:
        if not color.startswith("#") or len(color) not in (4, 7):
            raise HTTPException(status_code=400, detail="Invalid color format")
        cat.color = color
    await db.commit()
    await db.refresh(cat)
    return {
        "id": str(cat.id),
        "name": cat.name,
        "color": cat.color,
        "is_default": cat.is_default
    }

@router.delete("/{category_id}")
async def delete_category(
    category_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Category).where(
        Category.id == category_id,
        Category.user_id == current_user.id,
        Category.is_default == False
    )
    result = await db.execute(stmt)
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Custom category not found")
    await db.delete(cat)
    await db.commit()
    return {"message": "Deleted"}
