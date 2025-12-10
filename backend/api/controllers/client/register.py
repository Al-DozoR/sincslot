from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.request.service import ServiceCreateRequest

from backend.api.response.service import (
    ServiceEntityResponse,
    ServiceErrorResponse,
)

from backend.logger.logger import init_logger
from backend.api.controllers.company.auth.parse_auth_token import get_current_company_from_token
from backend.di_container.di_container import di_container
from backend.use_case.service_use_case import IServiceUseCase
from backend.core.db_helper import db_helper

logger = init_logger('register_client', 'INFO')

router = APIRouter()


@router.post("/")
async def register_client():
    pass
