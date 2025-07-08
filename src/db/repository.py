from sqlalchemy import select

from src.db.base import SessionMaker
from src.db.models import Note
from src.db.schemas import BaseNote


async def get_all_notes() -> list[Note]:
    async with SessionMaker() as session:
        stmt = select(Note)
        res = await session.scalars(stmt)
        return res.all()


async def get_one(name: str) -> Note | None:
    async with SessionMaker() as session:
        stmt = select(Note).where(Note.name == name)
        res = await session.scalar(stmt)
        return res


async def create_note(new_note: BaseNote) -> None:
    async with SessionMaker() as session:
        note = Note(**new_note.model_dump())
        session.add(note)
        await session.commit()


async def update_note(note: Note) -> None:
    async with SessionMaker() as session:
        session.add(note)
        await session.commit()


async def delete_note(note: Note) -> None:
    async with SessionMaker() as session:
        await session.delete(note)
        await session.commit()