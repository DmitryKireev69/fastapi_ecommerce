from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from app.schemas.categories import Category as CategorySchema, CategoryCreate
from app.models.categories import Category as CategoryModel
from app.models.products import Product as ProductModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db_async_db

router = APIRouter(
    prefix="/categories",
    tags=["Категории"],
)

@router.get("/", summary='Получить категорий', response_model=list[CategorySchema])
async def get_categories(db: AsyncSession = Depends(get_db_async_db)):
    """Получает всех список всех категорий"""
    stmp = select(CategoryModel).filter_by(is_active=True)
    result = await db.scalars(stmp)
    return result.all()


@router.get("/{category_id}", summary='Получить категорию', response_model=CategorySchema)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db_async_db)):
    """Получает категорию по идентификатору"""
    stmp = select(CategoryModel).filter_by(id=category_id, is_active=True)
    result = await db.scalars(stmp)
    db_category = result.one_or_none()
    # db_category = await db.get(CategoryModel, category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Категория с id {category_id} не найдена!')
    return db_category

@router.post("/", summary='Создать категорию', status_code=status.HTTP_201_CREATED, response_model=CategorySchema)
async def create_category(data_category: CategoryCreate, db: AsyncSession = Depends(get_db_async_db)):
    """Создает категорию"""
    if data_category.parent_id is not None:
        parent_id = data_category.parent_id
        stmp = select(CategoryModel).filter_by(id=parent_id, is_active=True)
        result = await db.scalars(stmp)
        parent = result.one_or_none()
        if parent is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Родитель с идентификатором {parent_id} не найден!')

    db_category = CategoryModel(**data_category.model_dump())
    db.add(db_category)
    await db.commit()
    return db_category


@router.put('/category/{category_id}', summary='Обновить категорию', response_model=CategorySchema)
async def update_category(category_id: int, category_data: CategoryCreate, db: AsyncSession = Depends(get_db_async_db)):
    """Обновляет категорию"""
    stmp = select(CategoryModel).filter_by(id=category_id, is_active=True)
    result = await db.scalars(stmp)
    db_category  = result.one_or_none()
    if db_category  is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Категория с идентификатором {category_id} не найдена!')
    parent_id = db_category.parent_id
    if parent_id is not None:
        stmp = select(CategoryModel).filter_by(id=parent_id, is_active=True)
        parent = await db.scalars(stmp)
        if parent.one_or_none() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Родитель с идентификатором {parent_id} не найден!')

    update_data = category_data.model_dump(exclude_unset=True)
    await db.execute(
        update(CategoryModel)
        .values(**update_data)
        .filter_by(id=category_id)
    )
    await db.commit()
    return db_category

@router.delete("/{category_id}", summary='Удалить категорию', response_model=CategorySchema)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db_async_db)):
    """Удаляет категорию"""
    stmp = select(CategoryModel).filter_by(id=category_id, is_active=True)
    result = await db.scalars(stmp)
    db_category = result.one_or_none()
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Категория не найдена')

    db_category.is_active = False
    await db.commit()
    return db_category
