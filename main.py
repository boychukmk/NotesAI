from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from routes.notes import router as notes_router
from routes.note_history import router as note_history_router
from routes.summarizer import router as summarizer_router
from routes.analytics import router as analytics_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Notes Manager System")


app.include_router(notes_router)
app.include_router(note_history_router)
app.include_router(summarizer_router)
app.include_router(analytics_router)
