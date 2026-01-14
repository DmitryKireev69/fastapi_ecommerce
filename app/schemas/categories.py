from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50, description='Название категории (3-50 символов)')]
    parent_id: Annotated[int | None, Field(default=None, description='ID родительской категории, если есть')]

    model_config = ConfigDict(extra='forbid')


class Category(CategoryBase):
    """
    Модель для ответа с данными категории.

    Используется в GET-запросах.
    """
    id: Annotated[int, Field(description='Уникальный идентификатор категории')]
    is_active: Annotated[bool, Field(description='Активность категории')]

    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid'
    )

class CategoryCreate(CategoryBase):
    """
    Модель для создания и обновления категории.

    Используется в POST и PUT запросах.
    """
    pass


