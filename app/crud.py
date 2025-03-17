import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.models import Note, NoteVersion
from app.schemas import NoteCreate, NoteUpdate


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def commit_handler(db: AsyncSession, message: str | None):
    try:
        await db.commit()
        if message:
            logger.info(message)
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {e}")
        raise


async def create_note(db: AsyncSession, note_data: NoteCreate) -> Optional[Note]:
    new_note = Note(**note_data.model_dump())
    db.add(new_note)
    await commit_handler(db, None)
    logger.info(f"New note created: {new_note}")
    await db.refresh(new_note)

    return new_note


async def get_note(db: AsyncSession, note_id: int) -> Optional[Note]:
    return await db.get(Note, note_id)


async def get_notes(db: AsyncSession) -> list[Note]:
    result = await db.execute(select(Note))
    return result.scalars().all()


async def update_note(db: AsyncSession, note_id: int, note_data: NoteUpdate) -> Optional[Note]:
    note = await db.get(Note, note_id)
    if not note:
        return None

    updated_note = note_data.model_dump(exclude_unset=True)
    if not updated_note:
        return note

    history_entry = NoteVersion(note_id=note.id, content=note.content)
    db.add(history_entry)

    for key, value in updated_note.items():
        setattr(note, key, value)

    await commit_handler(db, f"Note updated with ID: {note.id}")
    await db.refresh(note)
    return note


async def delete_note(db: AsyncSession, note_id: int) -> Optional[Note]:
    note = await db.get(Note, note_id)
    if not note:
        return None

    await db.delete(note)
    await commit_handler(db, f"Note deleted with ID: {note.id}")
    return note
