from pydantic import BaseModel, ConfigDict, constr
from datetime import datetime
from typing import List, Optional


class NoteBase(BaseModel):
    title: str
    content: constr(min_length=1, max_length=10000)


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteVersionResponse(BaseModel):
    id: int
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    versions: List[NoteVersionResponse] = []

    model_config = ConfigDict(from_attributes=True)
