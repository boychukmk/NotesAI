from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


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
        passive_deletes=True,
        order_by="NoteVersion.created_at.desc()",
        lazy = "selectin"
    )

    def __repr__(self):
        return f"Note(id={self.id} title={self.title})"


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

    def __repr__(self):
        return f"NoteVersion(id={self.id} note_id={self.note_id})"
