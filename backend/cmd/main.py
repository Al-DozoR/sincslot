import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from backend.api.conrollers.health import router_health
from backend.api.conrollers.company import router_company
from backend.core.config import settings
from backend.core.db_helper import db_helper
from backend.api.middleware.auth_middleware import AuthCompanyMiddleware
from backend.di_container.di_container import di_container


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

app.add_middleware(
    AuthCompanyMiddleware,
    exclude_path=["docs", "openapi", "health", "login", "register"],
    token_use_case=di_container.get_token_use_case(),
    company_use_case=di_container.get_company_use_cases()
)

app.include_router(
    router_health,
    prefix=settings.api.prefix,
)

app.include_router(
    router_company,
    prefix=settings.api_v1.prefix,
)

if __name__ == "__main__":
    logging.info(f'Start server: {settings.run.port}')
    uvicorn.run("main:app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
