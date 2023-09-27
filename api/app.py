from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from db.database import create_db_and_tables
from api.routers.schedule import router as schedule_router

tags_metadata = [
    {
        "name": "Расписание",
        "description": "Набор точек API для получения информации о расписании"
    }
]

app = FastAPI(
    title="Документация API приложения \"Расписание СурГУ\"",
    openapi_tags=tags_metadata,
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prefix_router = APIRouter(prefix="/api")
prefix_router.include_router(schedule_router)
app.include_router(prefix_router)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
