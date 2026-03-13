from sqlalchemy import String, Text, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from infrastructure.sqlite.database import Base


class Category(Base):
    __tablename__ = "blog_category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text)
    slug: Mapped[str] = mapped_column(String(64), unique=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self):
        return f"<Category(id={self.id}, title='{self.title}')>"