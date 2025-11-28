from fastapi import APIRouter, status, Depends, File, UploadFile
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.response.company import (
    CompanyByIdResponse,
    CompanySuccessResponse,
    CompanyErrorResponse,
)
from backend.api.conrollers.company.auth import get_current_company_from_token
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase
from backend.use_case.file_use_case import IFileStorage
from backend.core.db_helper import db_helper

logger = init_logger('company', 'INFO')

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
        logger.error(
            "Error occurred while getting company by id. Company id: %s Error: %s",
            company_id,
            str(ex),
            exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(
                error=f"failed to find a company with id {company_id}"
            ).model_dump()
        )

    if company is None:
        logger.warning("Failed to find company by id. Company id: %s", company_id)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(
                error=f"failed to find a company with id {company_id}"
            ).model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompanyByIdResponse(
            **company.to_dict()
        ).model_dump()
    )


@router_company.put("/logo")
async def upload_image(file: UploadFile = File(...),
                       company=Depends(get_current_company_from_token),
                       file_storage_use_case: IFileStorage = Depends(di_container.get_file_storage_use_case)):
    if not await file_storage_use_case.is_valid_size(file.size):
        logger.warning("Failed to save company logo %s it is too large", file.size)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(error="file logo is too large").model_dump()
        )

    extension = await file_storage_use_case.get_extension(file.filename)
    if not extension:
        logger.warning("Failed to save company logo %s it has incorrect extension", extension)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(error=f"file logo has invalid extension").model_dump()
        )

    if not await file_storage_use_case.is_valid_extension(extension):
        logger.warning("Failed to save company logo %s it has incorrect extension", file.filename)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(error=f"file logo has invalid extension").model_dump()
        )

    try:
        filename = await file_storage_use_case.save_file(company_id=company.id, extension=extension, file=file.file)
    except Exception as ex:
        logger.error(
            "Error occurred while getting company by id. Company id: %s Error: %s",
            company.id,
            str(ex),
            exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(error=f"failed to save logo image").model_dump()
        )

    logger.info("Logo company %s saved successfully", filename)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CompanySuccessResponse(message=f"Logo company {filename} saved successfully").model_dump()
    )
