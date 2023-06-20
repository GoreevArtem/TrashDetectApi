import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import api
import utils.create_sourse
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

# origins = [
#     "http://localhost",
#     "http://localhost:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def app_startup():
    utils.create_sourse.create_dir(path=os.path.join("..", "source_users_photo"))
