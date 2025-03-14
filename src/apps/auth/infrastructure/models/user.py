import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import UUID, LargeBinary, String

from core.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
