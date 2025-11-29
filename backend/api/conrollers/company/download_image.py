from fastapi import APIRouter, status, Depends, File, UploadFile
from starlette.responses import JSONResponse, FileResponse

from backend.api.response.company import (
    CompanySuccessResponse,
    CompanyErrorResponse,
)

from backend.api.conrollers.company.auth.parse_auth_token import get_current_company_from_token
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.file_use_case import IFileStorage

logger = init_logger('company', 'INFO')

router = APIRouter(tags=["company"])


@router.get("/logo/")
async def download_image(company=Depends(get_current_company_from_token),
                         file_storage_use_case: IFileStorage = Depends(di_container.get_file_storage_use_case)):

    try:
        file = await file_storage_use_case.get_file(company_id=company.id)
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

    if file is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(error=f"failed to find company logo by id {1}").model_dump()
        )

    filename, file_path = file[0], file[1]

    return FileResponse(
        path=file_path,
        media_type="image/jpeg",
        filename=filename,
        content_disposition_type="attachment"
    )
