from sqlalchemy import String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from infrastructure.sqlite.database import Base


class Comment(Base):
    __tablename__ = "blog_comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(0))
    created_at: Mapped[datetime] = mapped_column(DateTime)

    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("auth_user.id"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_post.id"))

    like: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __repr__(self):
        return f"<Comment(id={self.id}, author_id={self.author_id}, post_id={self.post_id})>"