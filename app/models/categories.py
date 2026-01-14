
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey
from typing import List


class Category(Base):

    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    products: Mapped[List['Product']] = relationship(back_populates='category')
    parent_id: Mapped[int | None] = mapped_column(ForeignKey('categories.id'))
    parent: Mapped['Category | None'] = relationship(back_populates='children', remote_side='Category.id',
                                                     foreign_keys='Category.parent_id')
    children: Mapped[List['Category']] = relationship(back_populates='parent', foreign_keys='Category.parent_id')

