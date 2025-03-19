from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.analytics import NoteAnalytics


router = APIRouter(prefix="/analytics", tags=["Notes Analytics"])


@router.get("/")
async def get_analytics(db: AsyncSession = Depends(get_db)):
    analytics_service = NoteAnalytics(db)

    return {
        "total_word_count": await analytics_service.get_word_count(),
        "average_note_length": await analytics_service.get_average_length(),
        "most_common_words": await analytics_service.get_most_common_words(),
        "top_notes": await analytics_service.get_top_notes(),
        "total_character_count": await analytics_service.get_character_count(),
        "median_note_length": await analytics_service.get_median_length(),
        "common_bigrams": await analytics_service.get_common_bigrams(),
        "common_trigrams": await analytics_service.get_common_trigrams()
    }
