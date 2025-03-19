import pytest
from httpx import AsyncClient, ASGITransport
from app.models import Note, NoteVersion
from app.main import app


@pytest.mark.asyncio
async def test_get_note_history(test_db_session, override_get_db):
    note = Note(title="Test Note", content="Initial content")
    test_db_session.add(note)
    await test_db_session.commit()
    await test_db_session.refresh(note)

    version1 = NoteVersion(note_id=note.id, content="Version 1")
    version2 = NoteVersion(note_id=note.id, content="Version 2")

    test_db_session.add_all([version1, version2])
    await test_db_session.commit()

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        response = await ac.get(f"/history/{note.id}")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["content"] == "Version 1"
    assert data[1]["content"] == "Version 2"


@pytest.mark.asyncio
async def test_get_note_history_not_found(test_db_session, override_get_db):
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        response = await ac.get("/history/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Note history not found."}
