from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base
import schemas, crud


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Notes Manager System")


@app.post("/notes/", response_model=schemas.NoteResponse,
         status_code=status.HTTP_201_CREATED, tags=["notes"])
def create_note(note_data: schemas.NoteCreate, db: Session = Depends(get_db)):
    if len(note_data.title) < 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Title must be at least 3 characters long.")
    return crud.create_note(db, note_data)


@app.get("/notes/{note_id}", response_model=schemas.NoteResponse, tags=["notes"])
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found.")
    return note


@app.get("/notes/", response_model=list[schemas.NoteResponse], tags=["notes"])
def get_notes(db: Session = Depends(get_db)):
    notes = crud.get_notes(db)
    if not notes:
        return []
    return notes


@app.put("/notes/{note_id}", response_model=schemas.NoteResponse, tags=["notes"])
def update_note(note_id: int, note_data: schemas.NoteUpdate, db: Session = Depends(get_db)):
    if not note_data.title and not note_data.content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="At least title or content must be updated.")

    updated_note = crud.update_note(db, note_id, note_data)
    if not updated_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found.")
    return updated_note


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["notes"])
def delete_note(note_id: int, db: Session = Depends(get_db)):
    if not crud.delete_note(db, note_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found.")
    return Response(content={"Note deleted successfully"}, status_code=status.HTTP_204_NO_CONTENT)
