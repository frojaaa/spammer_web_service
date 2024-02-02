from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from db import engine, Base
from apps.pagination import router
from settings import BASE_DIR

Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()

origins = [
    'http://localhost'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.mount("/static", StaticFiles(directory=BASE_DIR / 'sessions'), name='static')
