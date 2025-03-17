from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.routes.notes import router as notes_router
from app.routes.note_history import router as note_history_router
from app.routes.summarizer import router as summarizer_router
from app.routes.analytics import router as analytics_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Notes Manager System")


app.include_router(notes_router)
app.include_router(note_history_router)
app.include_router(summarizer_router)
app.include_router(analytics_router)
