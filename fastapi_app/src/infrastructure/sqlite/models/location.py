from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from infrastructure.sqlite.database import Base


class Location(Base):
    __tablename__ = "blog_location"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self):
        return f"<Location(id={self.id}, name='{self.name}')>"