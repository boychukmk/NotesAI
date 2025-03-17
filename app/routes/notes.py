from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/notes", tags=["Notes CRUD"])


@router.post("/", response_model=schemas.NoteResponse,
         status_code=status.HTTP_201_CREATED)
async def create_note(note_data: schemas.NoteCreate, db: AsyncSession = Depends(get_db)):
    if len(note_data.title) < 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Title must be at least 3 characters long.")
    return await crud.create_note(db, note_data)


@router.get("/{note_id}", response_model=schemas.NoteResponse)
async def get_note(note_id: int, db: AsyncSession = Depends(get_db)):
    note = await crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found.")
    return note


@router.get("/", response_model=list[schemas.NoteResponse])
async def get_notes(db: AsyncSession = Depends(get_db)):
    notes = await crud.get_notes(db)
    if not notes:
        return []
    return notes


@router.put("/{note_id}", response_model=schemas.NoteResponse)
async def update_note(note_id: int, note_data: schemas.NoteUpdate, db: AsyncSession = Depends(get_db)):
    if not note_data.title and not note_data.content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="At least title or content must be updated.")

    updated_note = await crud.update_note(db, note_id, note_data)
    if not updated_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found.")
    return updated_note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    if not await crud.delete_note(db, note_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
