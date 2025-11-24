from typing import Optional

from pydantic import EmailStr, ValidationError
from fastapi import APIRouter, status, Depends, UploadFile, File, Form, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from backend.api.requests.company import (
    CompanyCreateRequest,
    CompanyLoginRequest,
    CompanyRefreshTokenRequest,
    CompanyRecoverPasswordRequest,
    CompanyPhoneNumberRequest,
)
from backend.entity.company import CompanyEntity
from backend.logger.logger import init_logger
from backend.api.response.company import (
    CompanyTokensResponse,
    CompanyErrorResponse,
    CompanyRecoverPasswordResponse,
    CompanyRecoverPassword
)
from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase
from backend.use_case.token_use_case import IToken
from backend.core.db_helper import db_helper

logger = init_logger('auth_company', 'INFO')

router_auth_company = APIRouter(tags=["company"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


async def get_current_company_from_token(
        token: str = Depends(oauth2_scheme),
        token_use_case: IToken = Depends(di_container.get_token_use_case),
        company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
        session: AsyncSession = Depends(db_helper.session_getter)
) -> CompanyEntity | JSONResponse:
    try:
        payload = await token_use_case.decode_token(token)
    except JWTError as ex:
        logger.error("Error occurred while parsing token: %s. Error: %s", token, str(ex))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Failed to parse token",
        )

    company_id = payload.get("company_id")
    expired = payload.get("exp")

    if not await token_use_case.is_expired(expired):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )

    company = await company_use_case.get_company_by_id(session, company_id)
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Failed to find company by id {company_id} expired",
        )

    return company


@router_auth_company.post("/register", responses={
    status.HTTP_200_OK: {"model": CompanyTokensResponse},
    status.HTTP_400_BAD_REQUEST: {"model": CompanyErrorResponse},
    status.HTTP_409_CONFLICT: {"model": CompanyErrorResponse},
})
async def register(
        company: CompanyCreateRequest,
        company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
        session: AsyncSession = Depends(db_helper.session_getter)
) -> JSONResponse:
    if company.password.strip() != company.repeat_password.strip():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(error="passwords do not match").model_dump()
        )

    company_by_email = await company_use_case.get_company_by_email(session, company.email)
    if company_by_email is not None:
        logger.warning("Failed to create a company with email %s it is already exist", company.email)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=CompanyErrorResponse(error=f"user with email {company.email} is already exist").model_dump()
        )

    company_by_phone = await company_use_case.get_company_by_phone(session, company.phone)
    if company_by_phone is not None:
        logger.warning("Failed to create a company with phone %s it is already exist", company.phone)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=CompanyErrorResponse(error=f"user with phone {company.phone} is already exist").model_dump()
        )

    company_by_name = await company_use_case.get_company_by_name(session, company.name)
    if company_by_name is not None:
        logger.warning("Failed to create a company with name %s it is already exist", company.name)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=CompanyErrorResponse(error=f"user with name {company.name} is already exist").model_dump()
        )

    try:
        new_tokens = await company_use_case.save_company(
            session,
            name=company.name,
            email=company.email,
            phone=company.phone,
            address=company.address,
            password=company.password,
        )
    except Exception as ex:
        logger.error(f"Error occurred while registering new company: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(error=f"Failed to register company").model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CompanyTokensResponse(
            access_token=new_tokens.access_token,
            refresh_token=new_tokens.refresh_token,
        ).model_dump(by_alias=True)
    )


@router_auth_company.post("/login", responses={
    status.HTTP_201_CREATED: {"model": CompanyTokensResponse},
    status.HTTP_400_BAD_REQUEST: {"model": CompanyErrorResponse}
})
async def login(
        login_input: CompanyLoginRequest,
        company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    company = await company_use_case.get_company_by_email(session, login_input.email)
    if company is None:
        logger.warning("Failed to get company by email %s. Impossible to log in", login_input.email)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(
                error=f"Company with email {login_input.email} does not exist"
            ).model_dump()
        )

    if not await company_use_case.verify_password(login_input.password, company.password):
        logger.warning("Failed to verify password %s. Impossible to log in", login_input.password)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(
                error=f"Incorrect password"
            ).model_dump()
        )

    try:
        new_tokens = await company_use_case.login(session, company)
    except Exception as ex:
        logger.error(f"Error occurred while log in company: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(error=f"Failed to log in").model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CompanyTokensResponse(
            access_token=new_tokens.access_token,
            refresh_token=new_tokens.refresh_token,
        ).model_dump()
    )


@router_auth_company.post("/refresh-token", responses={
    status.HTTP_201_CREATED: {"model": CompanyTokensResponse},
    status.HTTP_400_BAD_REQUEST: {"model": CompanyErrorResponse}
})
async def refresh_tokens(
        refresh_token: CompanyRefreshTokenRequest,
        token_use_case: IToken = Depends(di_container.get_token_use_case),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    try:
        decoded_token = await token_use_case.decode_token(refresh_token.refresh_token)
    except JWTError as ex:
        logger.error("Failed to parse refresh token: %s", str(ex))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(error=f"Failed to parse refresh token").model_dump()
        )

    is_refresh = await token_use_case.is_refresh_token(decoded_token)
    if not is_refresh:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(error=f"Provided token is not refresh token").model_dump()
        )

    try:
        new_tokens = await token_use_case.update_tokens(session, refresh_token.refresh_token)
    except Exception as ex:
        logger.error(f"Error occurred while refreshing tokens %s:", str(ex), exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(error=f"Failed to register company").model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CompanyTokensResponse(
            access_token=new_tokens.access_token,
            refresh_token=new_tokens.refresh_token,
        ).model_dump(by_alias=True)
    )


@router_auth_company.post("/recover", responses={
    status.HTTP_200_OK: {"model": CompanyRecoverPassword},
    status.HTTP_404_NOT_FOUND: {"model": CompanyErrorResponse}
})
async def recover_password(
        recover_pass: CompanyRecoverPasswordRequest,
        company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
        session: AsyncSession = Depends(db_helper.session_getter)
) -> JSONResponse:
    company_by_email = await company_use_case.get_company_by_email(session, recover_pass.email)
    if company_by_email is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(
                error=f"user with email {recover_pass.email} does not exist"
            ).model_dump()
        )

    try:
        random_pass = await company_use_case.recover_company_by_email(session, recover_pass.email)
    except Exception as ex:
        logger.error(f"Error occurred while recovering: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(error=f"Failed to recover password").model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompanyRecoverPasswordResponse(
            login=recover_pass.email,
            new_password=random_pass
        ).model_dump()
    )
