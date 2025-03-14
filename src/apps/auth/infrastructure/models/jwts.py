import uuid
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import UUID, DateTime, String

from core.database import Base


class RefreshJwtModel(Base):
    __tablename__ = "refresh_jwts"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    token: Mapped[str] = mapped_column(String, nullable=False)
    token_expire: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

