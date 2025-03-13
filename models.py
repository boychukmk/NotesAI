from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    versions = relationship(
        "NoteVersion",
        back_populates="note",
        cascade="all, delete",
        order_by="desc(NoteVersion.created_at)"
    )


class NoteVersion(Base):
    __tablename__ = "note_versions"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"),nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    note = relationship(
        "Note",
        back_populates="versions"
    )
