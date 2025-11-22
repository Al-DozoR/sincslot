from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.response.company import (
    CompanyByIdResponse,
    CompaniesList,
    CompanyErrorResponse,
)
from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase
from backend.core.db_helper import db_helper

router_company = APIRouter(tags=["company"])


@router_company.get("/{company_id}", responses={
    status.HTTP_200_OK: {"model": CompanyByIdResponse},
    status.HTTP_404_NOT_FOUND: {"model": CompanyErrorResponse},
})
async def get_company_by_id(
        company_id: int,
        company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    try:
        company = await company_use_case.get_company_by_id(session, company_id)
    except Exception as ex:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(
                message=f"failed to find a company with id {company_id}"
            ).model_dump()
        )

    if company is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(
                message=f"failed to find a company with id {company_id}"
            ).model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompanyByIdResponse(
            **company.to_dict()
        ).model_dump()
    )


@router_company.get("/", responses={
    status.HTTP_200_OK: {"model": CompaniesList},
})
async def get_list_companies(
        company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        companies = await company_use_case.get_companies(session)
    except Exception as ex:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(
                message=f"failed to get companies"
            ).model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompaniesList(companies=[CompanyByIdResponse(**c.to_dict()) for c in companies]).model_dump())
