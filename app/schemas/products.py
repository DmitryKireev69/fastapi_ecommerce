from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from decimal import Decimal


class ProductBase(BaseModel):
    name: Annotated[
        str, Field(min_length=3, max_length=100, description='Название товара (3-100 символов')
    ]
    description: Annotated[
        str | None, Field(default=None, max_length=500, description='Описание товара (до 500 символов)')
    ]
    price: Annotated[Decimal, Field(gt=0, decimal_places=2, description='Цена товара (больше 0)')]
    image_url: Annotated[str, Field(default=None, max_length=200, description='URL изображения товара')]
    stock: Annotated[int, Field(ge=0, description='Количество товара на складе (0 или больше)')]
    category_id: Annotated[int, Field(description='ID категории, к которой относится товар')]

    model_config = ConfigDict(extra='forbid')

class Product(ProductBase):
    """
    Модель для ответа с данными продуктов.

    Используется в GET-запросах.
    """
    id: Annotated[int, Field(description='Уникальный идентификатор товара')]
    is_active: Annotated[bool, Field(description='Активность товара')]

    model_config = ConfigDict(
        **ProductBase.model_config,
        from_attributes=True
    )

class ProductCreate(ProductBase):
    """
    Модель для создания и обновления продукта.

    Используется в POST и PUT запросах.
    """
    pass
