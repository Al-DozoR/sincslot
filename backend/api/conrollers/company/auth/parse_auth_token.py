from fastapi import APIRouter, status, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from backend.entity.company import CompanyEntity
from backend.logger.logger import init_logger
from backend.api.response.company import CompanyErrorResponse
from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase
from backend.use_case.token_use_case import IToken
from backend.core.db_helper import db_helper

logger = init_logger('auth_company', 'INFO')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


async def get_current_company_from_token(
        token: str = Depends(oauth2_scheme),
        token_use_case: IToken = Depends(di_container.get_token_use_case),
        company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
        session: AsyncSession = Depends(db_helper.session_getter)
) -> CompanyEntity | JSONResponse:

    is_revoke = await token_use_case.is_revoke(session, token)
    if is_revoke is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token was not found",
        )

    if is_revoke is True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is already revoked",
        )

    try:
        payload_access_token = await token_use_case.decode_token(token)
    except JWTError as ex:
        logger.error("Error occurred while parsing token: %s. Error: %s", token, str(ex))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to parse token. Probably token is expired",
        )

    company_id = payload_access_token.get("company_id")

    company = await company_use_case.get_company_by_id(session, company_id)
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Failed to find company by id {company_id} expired",
        )

    return company
