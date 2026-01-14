from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from app.schemas.products import ProductCreate, Product as ProductSchema
from app.database import get_db_async_db
from app.models.products import Product as ProductModel
from app.models.categories import Category as CategoryModel
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/products",
    tags=["Товары"],
)

async def get_category(category_id: int, db: AsyncSession):
    """Получение категории"""
    stmp = select(CategoryModel).filter_by(id=category_id, is_active=True)
    result = await db.scalars(stmp)
    category = result.one_or_none()
    if not category:
        raise HTTPException(detail='Категория не найдена', status_code=status.HTTP_404_NOT_FOUND)
    return category

async def get_product(product_id: int, db: AsyncSession):
    """Получение продукта"""
    stmp = select(ProductModel).filter_by(id=product_id, is_active=True)
    result = await db.scalars(stmp)
    product = result.one_or_none()
    if not product:
        raise HTTPException(detail='Продукт не найден', status_code=status.HTTP_404_NOT_FOUND)
    return product

@router.get("/", summary='Получить все товары', response_model=list[ProductSchema])
async def get_products(db: AsyncSession = Depends(get_db_async_db)):
    """Возвращает список всех товаров"""
    stmp = select(ProductModel).filter_by(is_active=True)
    result = await db.scalars(stmp)
    return result.all()

@router.post('/', summary='Создать товар', response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(data_category: ProductCreate, db: AsyncSession = Depends(get_db_async_db)):
    """Создаёт новый товар"""
    await get_category(data_category.category_id, db)
    product = ProductModel(**data_category.model_dump())
    db.add(product)
    await db.commit()
    return product

@router.get('/categories/{category_id}', summary='Получение товара по категории', response_model=list[ProductSchema])
async def get_product_by_category(category_id: int, db: AsyncSession = Depends(get_db_async_db)):
    """Возвращает список товаров в указанной категории по её ID"""
    await get_category(category_id, db)
    stmp = select(ProductModel).filter_by(category_id=category_id, is_active=True)
    result = await db.scalars(stmp)
    return result.all()

@router.get('/{product_id}', summary='Получить информацию о товаре', response_model=ProductSchema)
async def get_detail_product(product_id: int, db: AsyncSession = Depends(get_db_async_db)):
    """Получает детальную информацию о товаре"""
    return await get_product(product_id, db)

@router.put('/{product_id}', summary='Обновить продукт', response_model=ProductSchema)
async def update_product(product_id: int, data_category: ProductCreate, db: AsyncSession = Depends(get_db_async_db)):
    """Обновляет продукт"""
    product = await get_product(product_id, db)
    await get_category(data_category.category_id, db)

    update_data = data_category.model_dump(exclude_unset=True)
    await db.execute(
        update(ProductModel)
        .filter_by(id=product_id)
        .values(**update_data)
    )
    await db.commit()
    return product

@router.delete('/{product_id}', summary='Удалить продукт')
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db_async_db)):
    """Удаляет продукт"""
    product = await get_product(product_id, db)
    product.is_active = False
    await db.commit()
    return {'status': 'success', 'message': f'Продукт с идентификатором {product_id} удален!'}

