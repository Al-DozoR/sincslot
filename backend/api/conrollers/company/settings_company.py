from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.request.company import CompanyUpdateSettingsRequest
from backend.api.response.company import (
    CompanySuccessResponse,
    CompanyErrorResponse,
)
from backend.use_case.company_use_case import ICompanyUseCase
from backend.api.conrollers.company.auth.parse_auth_token import get_current_company_from_token
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.core.db_helper import db_helper

logger = init_logger('company', 'INFO')

router = APIRouter(tags=["company"])


@router.patch("/settings", responses={
    status.HTTP_200_OK: {"model": CompanyUpdateSettingsRequest},
    status.HTTP_400_BAD_REQUEST: {"model": CompanyErrorResponse},
    status.HTTP_409_CONFLICT: {"model": CompanyErrorResponse},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CompanyErrorResponse}
})
async def update_settings_company(company_settings: CompanyUpdateSettingsRequest,
                                  company=Depends(get_current_company_from_token),
                                  company_use_case: ICompanyUseCase = Depends(
                                            di_container.get_company_use_cases
                                         ),
                                  session: AsyncSession = Depends(db_helper.session_getter)):

    company_by_email = await company_use_case.get_company_by_email(session, company_settings.email)
    if company_by_email is not None:
        logger.warning("Failed to update a company with email %s it is already exist", company_settings.email)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=CompanyErrorResponse(error=f"company with email {company_settings.email} is already exist").model_dump()
        )

    company_by_phone = await company_use_case.get_company_by_phone(session, company_settings.phone)
    if company_by_phone is not None:
        logger.warning("Failed to update a company with phone %s it is already exist", company_settings.phone)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=CompanyErrorResponse(error=f"company with phone {company_settings.phone} is already exist").model_dump()
        )

    company_by_name = await company_use_case.get_company_by_name(session, company_settings.name)
    if company_by_name is not None:
        logger.warning("Failed to update a company with name %s it is already exist", company_settings.name)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=CompanyErrorResponse(error=f"user company name {company_settings.name} is already exist").model_dump()
        )

    company_to_update = company_settings.model_dump(exclude_none=True)

    if company_to_update.get("new_password") and company_to_update.get("new_repeat_password"):
        company_to_update["password"] = company_to_update.get("new_password")

    try:
        updated_data = await company_use_case.update_company_by_id(
            session=session,
            company_id=company.id,
            name=company_to_update.get("name"),
            email=company_to_update.get("email"),
            password=company_to_update.get("password"),
            phone=company_to_update.get("phone"),
            slug_booking_url=company_to_update.get("slug_booking_url"),
            description=company_to_update.get("description"),
            address=company_to_update.get("address"),
        )
    except Exception as ex:
        logger.error(f"Error occurred while updating company settings: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(error=f"Failed to update company").model_dump()
        )

    if updated_data is None:
        logger.error(f"Error occurred while updating company settings")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(error=f"Failed to update company").model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompanySuccessResponse(message="Company updated successfully").model_dump()
    )
