from pyexpat.errors import messages

from fastapi import APIRouter, status, Depends, HTTPException
from starlette.responses import JSONResponse
from backend.api.requests.company import CreateCompanyRequest
from backend.api.response.company import (
    CreateCompanyResponse,
    CompanyByIdResponse,
    CompanyNotFoundByIdResponse,
    CreateCompanyErrorResponse,
)
from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase, CompanyUseCase
from backend.core.db_helper import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from backend.entity.company import CompanyEntity

router_company = APIRouter(tags=["company"])


@router_company.post("/", responses={
    status.HTTP_201_CREATED: {"model": CreateCompanyResponse},
    status.HTTP_400_BAD_REQUEST: {"model": CreateCompanyErrorResponse}
})
async def register_company(
        company: CreateCompanyRequest,
        company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
        session: AsyncSession = Depends(db_helper.session_getter)
) -> JSONResponse:
    if company.password != company.repeat_password:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=CreateCompanyErrorResponse(message="passwords do not match")
        )

    new_company = CompanyEntity(
        name=company.name,
        email=company.email,
        phone=company.phone,
        address=company.address,
        password=company.password
    )

    try:
        tokens = await company_use_case.save_company(session, new_company)
    except Exception as ex:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=CreateCompanyErrorResponse(message=f"{str(ex)}").model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CreateCompanyResponse(
            access_token=tokens.get("access_token"),
            refresh_token=tokens.get("refresh_token"),
        ).model_dump()
    )


@router_company.get("/{company_id}", responses={
    status.HTTP_200_OK: {"model": CompanyByIdResponse},
    status.HTTP_404_NOT_FOUND: {"model": CompanyNotFoundByIdResponse},
})
async def get_company_by_id(
        company_id: int,
        company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    company = await company_use_case.get_company_by_id(session, company_id)

    if company is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyNotFoundByIdResponse(
                message=f"failed to find a company with id {company_id}"
            ).model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompanyByIdResponse(
            **company.to_dict()
        ).model_dump()
    )
