from datetime import datetime
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from datetime import datetime, UTC

class ShortenedURL(Base):
    __tablename__ = "shortened_urls"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    original_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    short_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True
    )
    clicks: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(UTC),
    nullable=False
)