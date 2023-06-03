from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import api
from database.db import engine, Base
from settings.meta import title, description, version, tags_metadata

app = FastAPI(
    title=title,
    description=description,
    version=version,
    openapi_tags=tags_metadata
)

Base.metadata.create_all(bind=engine)
app.include_router(api.router)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
