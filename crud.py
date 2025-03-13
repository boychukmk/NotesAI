import logging
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Note, NoteVersion
from schemas import NoteCreate, NoteUpdate


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def commit_handler(db: Session, message: str | None):
    try:
        db.commit()
        if message:
            logger.info(message)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise


def create_note(db: Session, note_data: NoteCreate) -> Optional[Note]:
    new_note = Note(**note_data.model_dump())
    db.add(new_note)
    commit_handler(db, None)
    logger.info(f"New note created: {new_note}")
    db.refresh(new_note)

    return new_note


def get_note(db: Session, note_id: int) -> Optional[Note]:
    return db.get(Note, note_id)


def get_notes(db: Session) -> list[Note]:
    return db.query(Note).all()


def update_note(db: Session, note_id: int, note_data: NoteUpdate) -> Optional[Note]:
    note = db.get(Note, note_id)
    if not note:
        return None

    updated_note = note_data.model_dump(exclude_unset=True)
    if not updated_note:
        return note

    history_entry = NoteVersion(note_id=note.id, content=note.content)
    db.add(history_entry)

    for key, value in updated_note.items():
        setattr(note, key, value)

    commit_handler(db, f"Note updated with ID: {note.id}")
    db.refresh(note)
    return note


def delete_note(db: Session, note_id: int) -> Optional[Note]:
    note = db.get(Note, note_id)
    if not note:
        return None

    history_entry = NoteVersion(note_id=note.id, content=note.content)
    db.add(history_entry)
    commit_handler(db, f"Note history with ID: {note.id} saved")

    db.delete(note)
    commit_handler(db, f"Note deleted with ID: {note.id}")
    return note
