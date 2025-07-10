from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Note(Base):
    __tablename__ = "notes"

    name: Mapped[str] = mapped_column(index=True)
    text: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(index=True)
