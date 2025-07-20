from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, BigInteger, func

from src.core.db import Base


class Note(Base):
    __tablename__ = "notes"

    name: Mapped[str] = mapped_column(index=True)
    text: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
