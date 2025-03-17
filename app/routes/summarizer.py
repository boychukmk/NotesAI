from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Note
from app.services.gemini_summerizer import summarize_text


router = APIRouter(prefix="/summarizer", tags=["AI Summarizer"])


@router.post("/{note_id}")
async def get_note_summary(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    summary = summarize_text(note.content)
    return {"note_id": note_id, "summary": summary}
