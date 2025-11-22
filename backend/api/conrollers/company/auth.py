from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from backend.api.requests.company import (
    CompanyCreateRequest,
    CompanyLoginRequest,
    CompanyRefreshTokenRequest,
    CompanyRecoverPasswordRequest
)
from backend.api.response.company import CompanyTokensResponse, CompanyErrorResponse, CompanyRecoverPasswordResponse

from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase
from backend.use_case.token_use_case import IToken
from backend.core.db_helper import db_helper

router_auth_company = APIRouter(tags=["company"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


async def get_current_company_from_token(
        token: str = Depends(oauth2_scheme),
        token_use_case: IToken = Depends(di_container.get_token_use_case),
        company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
        session: AsyncSession = Depends(db_helper.session_getter)
):

    try:
        payload = await token_use_case.decode_token(token)
    except JWTError as ex:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=CompanyErrorResponse(message="Failed to parse token")
        )

    company_id = payload.get("company_id")
    expired = payload.get("exp")

    if not await token_use_case.is_expired(expired):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=CompanyErrorResponse(message="Token expired")
        )

    company = await company_use_case.get_company_by_id(session, company_id)
    if company is None:
        return

    return company


@router_auth_company.post("/register", responses={
    status.HTTP_200_OK: {"model": CompanyTokensResponse},
    status.HTTP_400_BAD_REQUEST: {"model": CompanyErrorResponse}
})
async def register(
        company: CompanyCreateRequest,
        company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
        session: AsyncSession = Depends(db_helper.session_getter)
) -> JSONResponse:
    if company.password != company.repeat_password:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(message="passwords do not match")
        )

    company_by_email = await company_use_case.get_company_by_email(session, company.email)
    if company_by_email is not None:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=CompanyErrorResponse(message=f"user with email {company.email} is already exist").model_dump()
        )

    company_by_phone = await company_use_case.get_company_by_phone(session, company.phone)
    if company_by_phone is not None:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=CompanyErrorResponse(message=f"user with phone {company.phone} is already exist").model_dump()
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
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(message=f"Failed to register company").model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CompanyTokensResponse(
            access_token=new_tokens.access_token,
            refresh_token=new_tokens.refresh_token,
        ).model_dump()
    )


@router_auth_company.post("/login", responses={
    status.HTTP_201_CREATED: {"model": CompanyTokensResponse},
    status.HTTP_400_BAD_REQUEST: {"model": CompanyErrorResponse}
})
async def login(
        login_input: CompanyLoginRequest,
        company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
        session: AsyncSession = Depends(db_helper.session_getter),
):

    if not login_input.email and not login_input.phone:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(message="email or phone is required to log in").model_dump()
        )

    try:
        new_tokens = await company_use_case.login(session, login_input.email, login_input.password)
    except Exception as ex:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(message=f"Failed to register company").model_dump()
        )

    if not new_tokens:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(message="email or phone or password is incorrect").model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CompanyTokensResponse(
            access_token=new_tokens.get("access_token"),
            refresh_token=new_tokens.get("refresh_token"),
        ).model_dump()
    )


@router_auth_company.post("/refresh_token", responses={
    status.HTTP_201_CREATED: {"model": CompanyTokensResponse},
    status.HTTP_400_BAD_REQUEST: {"model": CompanyErrorResponse}
})
async def refresh_tokens(
        refresh_token: CompanyRefreshTokenRequest,
        token_use_case: IToken = Depends(di_container.get_token_use_case),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        new_tokens = await token_use_case.update_tokens(session, refresh_token.refresh_token)
    except Exception as ex:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(message=f"Failed to register company").model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CompanyTokensResponse(
            access_token=new_tokens.access_token,
            refresh_token=new_tokens.refresh_token,
        ).model_dump()
    )


@router_auth_company.post("/recover")
async def recover_password(
    recover_pass: CompanyRecoverPasswordRequest,
    company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
    session: AsyncSession = Depends(db_helper.session_getter)
):
    company_by_email = await company_use_case.get_company_by_email(session, recover_pass.email)
    if company_by_email is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(
                message=f"user with email {recover_pass.email} does not exist"
            ).model_dump()
        )

    random_pass = await company_use_case.recover_company_by_email(session, recover_pass.email)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompanyRecoverPasswordResponse(
            login=recover_pass.email,
            new_password=random_pass
        ).model_dump()
    )
