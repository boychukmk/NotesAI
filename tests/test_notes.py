import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from app.crud import update_note
from app.main import app
from app.models import Note
from app.schemas import NoteUpdate


@pytest.mark.asyncio
async def test_get_empty_notes(override_get_db):
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        response = await ac.get("/notes/")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_note(override_get_db):
    note_data = {"title": "Test Note", "content": "This is a test note content."}

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        response = await ac.post("/notes/", json=note_data)

    assert response.status_code == 201
    created_note = response.json()
    assert created_note["title"] == note_data["title"]
    assert created_note["content"] == note_data["content"]


@pytest.mark.asyncio
async def test_create_note_with_short_title(override_get_db):
    note_data = {"title": "Te", "content": "This is a test note content."}

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        response = await ac.post("/notes/", json=note_data)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["msg"] == "String should have at least 3 characters" for error in errors)


@pytest.mark.asyncio
async def test_get_note_by_id(override_get_db):
    note_data = {"title": "Test Note", "content": "This is a test note content."}

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        create_response = await ac.post("/notes/", json=note_data)
        note_id = create_response.json()["id"]

        response = await ac.get(f"/notes/{note_id}")

    assert response.status_code == 200
    retrieved_note = response.json()
    assert retrieved_note["title"] == note_data["title"]
    assert retrieved_note["content"] == note_data["content"]


@pytest.mark.asyncio
async def test_get_note_not_found(override_get_db):
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        response = await ac.get("/notes/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found."


@pytest.mark.asyncio
async def test_get_all_notes(override_get_db):
    notes = [
        {"title": "Note 1", "content": "Content of note 1"},
        {"title": "Note 2", "content": "Content of note 2"},
    ]

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        for note in notes:
            await ac.post("/notes/", json=note)

        response = await ac.get("/notes/")

    assert response.status_code == 200
    retrieved_notes = response.json()
    assert len(retrieved_notes) == len(notes)
    assert {note["title"] for note in retrieved_notes} == {note["title"] for note in notes}


@pytest.mark.asyncio
async def test_update_note(override_get_db):
    original_note = {"title": "Old Title", "content": "Old Content"}
    updated_note = {"title": "Updated Title", "content": "Updated Content"}

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        create_response = await ac.post("/notes/", json=original_note)
        note_id = create_response.json()["id"]

        update_response = await ac.put(f"/notes/{note_id}", json=updated_note)

    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["title"] == updated_note["title"]
    assert updated_data["content"] == updated_note["content"]


@pytest.mark.asyncio
async def test_update_note_not_found(override_get_db):
    updated_data = {"title": "Updated Title", "content": "Updated Content"}

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        response = await ac.put("/notes/9999", json=updated_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found."


@pytest.mark.asyncio
async def test_update_note_invalid_data(override_get_db):
    note_data = {"title": "Valid Title", "content": "Valid Content"}
    invalid_data = {"title": "", "content": "Updated content"}

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        create_response = await ac.post("/notes/", json=note_data)
        note_id = create_response.json()["id"]

        response = await ac.put(f"/notes/{note_id}", json=invalid_data)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(error["msg"] == "String should have at least 3 characters" for error in errors)


@pytest.mark.asyncio
async def test_delete_note(override_get_db):
    note_data = {"title": "Note to Delete", "content": "Content to delete"}

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        create_response = await ac.post("/notes/", json=note_data)
        note_id = create_response.json()["id"]

        delete_response = await ac.delete(f"/notes/{note_id}")
        get_response = await ac.get(f"/notes/{note_id}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_note_not_found(override_get_db):
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as ac:
        response = await ac.delete("/notes/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found."


@pytest.mark.asyncio
async def test_update_note_when_no_note_provided(override_get_db, test_db_session):
    result = await update_note(test_db_session, note_data=None, note_id=1)
    assert result is None


@pytest.mark.asyncio
async def test_update_note_when_updated_data_is_present(override_get_db, test_db_session):
    note = Note(id=1, title="Title", content="Original content")
    test_db_session.add(note)
    await test_db_session.commit()

    updated_note_data = NoteUpdate(content="Updated content")

    result = await update_note(db=test_db_session, note_id=1, note_data=updated_note_data)

    assert result.id == note.id
    assert result.title == note.title
    assert result.content == updated_note_data.content

    updated_note = await test_db_session.get(Note, note.id)
    assert updated_note.content == updated_note_data.content

    history_entry = await test_db_session.execute(
        text("SELECT * FROM note_versions WHERE note_id = :note_id"),
        {"note_id": note.id}
    )
    history_entry = history_entry.fetchall()

    assert len(history_entry) > 0
    assert history_entry[0].content == "Original content"
