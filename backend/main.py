import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from backend.api.conrollers.health import router_health
from backend.api.conrollers.company import router_company
from backend.core.config import settings
from core.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router_health,
    prefix=settings.api.prefix,
)

app.include_router(
    router_company,
    prefix=settings.api.prefix,
)

if __name__ == "__main__":
    logging.info(f'Start server: {settings.run.port}')
    uvicorn.run("main:app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
