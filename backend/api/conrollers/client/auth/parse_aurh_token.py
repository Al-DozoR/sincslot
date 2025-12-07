from fastapi import APIRouter, status, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from backend.entity.client import ClientEntity
from backend.entity.company import CompanyEntity
from backend.logger.logger import init_logger
from backend.api.response.company import CompanyErrorResponse
from backend.di_container.di_container import di_container
from backend.use_case.client_use_case import IClientUseCase
from backend.use_case.company_use_case import ICompanyUseCase
from backend.use_case.token_use_case import IToken
from backend.core.db_helper import db_helper

logger = init_logger('client', 'INFO')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/company/auth/register")


async def get_current_client_from_token(
        token: str = Depends(oauth2_scheme),
        token_use_case: IToken = Depends(di_container.get_token_use_case),
        client_use_case: IClientUseCase = Depends(di_container.get_client_use_case),
        session: AsyncSession = Depends(db_helper.session_getter)
) -> ClientEntity | JSONResponse:

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

    client_id = payload_access_token.get("client_id")

    client = await client_use_case.get_client_by_id(session, client_id)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Failed to find client by id {client_id} expired",
        )

    return client
