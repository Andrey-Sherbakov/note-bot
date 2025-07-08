from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class Note(Base):
    __tablename__ = "notes"

    name: Mapped[str] = mapped_column(index=True)
    text: Mapped[str] = mapped_column()
