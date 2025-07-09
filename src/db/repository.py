from sqlalchemy import select

from db.base import SessionMaker
from db.models import Note
from db.schemas import BaseNote


async def get_all_notes() -> list[Note]:
    async with SessionMaker() as session:
        stmt = select(Note)
        res = await session.scalars(stmt)
        return res.all()


async def get_by_name(name: str) -> Note | None:
    async with SessionMaker() as session:
        stmt = select(Note).where(Note.name == name)
        res = await session.scalar(stmt)
        return res


async def get_by_id(note_id: int) -> Note | None:
    async with SessionMaker() as session:
        stmt = select(Note).where(Note.id == note_id)
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


async def search_by_prefix(prefix: str, limit: int = 10):
    async with SessionMaker() as session:
        stmt = select(Note).where(Note.name.ilike(f"{prefix}%")).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()