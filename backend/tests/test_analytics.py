import pytest
from app.services.analytics import NoteAnalytics
from app.models import Note


@pytest.fixture
def note_analytics(test_db_session):
    return NoteAnalytics(test_db_session)


@pytest.mark.asyncio
async def test_get_word_count(note_analytics, test_db_session):
    note1 = Note(title="title", content="Hello world")
    note2 = Note(title="title", content="This is a test note")

    test_db_session.add_all([note1, note2])

    await test_db_session.commit()

    result = await note_analytics.get_word_count()
    assert result == 7


@pytest.mark.asyncio
async def test_get_word_count_empty_db(note_analytics):
    result = await note_analytics.get_word_count()
    assert result == 0


@pytest.mark.asyncio
async def test_get_average_length(note_analytics, test_db_session):
    note1 = Note(title="title", content="Short")
    note2 = Note(title="title", content="This is longer")

    test_db_session.add_all([note1, note2])

    await test_db_session.commit()

    result = await note_analytics.get_average_length()
    assert result == (5 + 14) / 2


@pytest.mark.asyncio
async def test_get_average_length_empty_db(note_analytics):
    result = await note_analytics.get_average_length()
    assert result == 0


@pytest.mark.asyncio
async def test_get_top_notes(note_analytics, test_db_session):
    notes = [
        Note(title="title", content="shortest"),
        Note(title="title", content="much longer note"),
        Note(title="title", content="a bit longer than short"),
        Note(title="title", content="short"),
        Note(title="title", content="small"),
        Note(title="title", content="bigger one note"),
    ]

    test_db_session.add_all(notes)

    await test_db_session.commit()

    result = await note_analytics.get_top_notes()

    longest = sorted(notes, key=lambda n: len(n.content), reverse=True)[:3]
    shortest = sorted(notes, key=lambda n: len(n.content))[:3]

    assert len(result["longest"]) == 3
    assert len(result["shortest"]) == 3

    assert [n["id"] for n in result["longest"]] == [n.id for n in longest]
    assert [n["id"] for n in result["shortest"]] == [n.id for n in shortest]


@pytest.mark.asyncio
async def test_get_character_count(note_analytics, test_db_session):
    note1 = Note(title="title", content="abc")
    note2 = Note(title="title", content="defg")

    test_db_session.add_all([note1, note2])

    await test_db_session.commit()

    result = await note_analytics.get_character_count()
    assert result == 7


@pytest.mark.asyncio
async def test_get_character_count_empty_db(note_analytics):
    result = await note_analytics.get_character_count()
    assert result == 0


@pytest.mark.asyncio
async def test_get_median_length(note_analytics, test_db_session):
    notes = [
        Note(title="title", content="a"),
        Note(title="title", content="abcd"),
        Note(title="title", content="abcdefg"),
    ]

    test_db_session.add_all(notes)

    await test_db_session.commit()

    result = await note_analytics.get_median_length()
    assert result == 4


@pytest.mark.asyncio
async def test_get_median_length_empty_db(note_analytics):
    result = await note_analytics.get_median_length()
    assert result == 0
