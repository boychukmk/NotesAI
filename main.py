from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base, Note
import schemas, crud
from services.gemini_summerizer import summarize_text

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Notes Manager System")


@app.post("/notes/", response_model=schemas.NoteResponse,
         status_code=status.HTTP_201_CREATED, tags=["crud"])
def create_note(note_data: schemas.NoteCreate, db: Session = Depends(get_db)):
    if len(note_data.title) < 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Title must be at least 3 characters long.")
    return crud.create_note(db, note_data)


@app.get("/notes/{note_id}", response_model=schemas.NoteResponse, tags=["crud"])
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found.")
    return note


@app.get("/notes/", response_model=list[schemas.NoteResponse], tags=["crud"])
def get_notes(db: Session = Depends(get_db)):
    notes = crud.get_notes(db)
    if not notes:
        return []
    return notes


@app.put("/notes/{note_id}", response_model=schemas.NoteResponse, tags=["crud"])
def update_note(note_id: int, note_data: schemas.NoteUpdate, db: Session = Depends(get_db)):
    if not note_data.title and not note_data.content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="At least title or content must be updated.")

    updated_note = crud.update_note(db, note_id, note_data)
    if not updated_note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found.")
    return updated_note


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["crud"])
def delete_note(note_id: int, db: Session = Depends(get_db)):
    if not crud.delete_note(db, note_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Note not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/notes/{note_id}/history", response_model=list[schemas.NoteVersionResponse], tags=["history"])
def get_note_history(note_id: int, db: Session = Depends(get_db)):
    history = db.query(crud.NoteVersion).filter(crud.NoteVersion.note_id == note_id).all()
    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Note history not found.")
    return history


@app.post("/notes/{note_id}/summarize", tags=["ai-summarizer"])
def get_note_summary(note_id: int, db: Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    summary = summarize_text(note.content)
    return {"note_id": note_id, "summary": summary}