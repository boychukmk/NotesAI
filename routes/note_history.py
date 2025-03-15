from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import crud, schemas
from database import get_db


router = APIRouter(prefix="/history", tags=["Note History"])


@router.get("/{note_id}", response_model=list[schemas.NoteVersionResponse])
async def get_note_history(note_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(crud.NoteVersion).filter(crud.NoteVersion.note_id == note_id)
    result = await db.execute(stmt)
    history = result.scalars().all()
    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Note history not found.")
    return history
