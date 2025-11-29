from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.request.company import CompanyWorkScheduleRequest
from backend.api.response.company import (
    CompanyErrorResponse,
    CompanyWorkScheduleResponse
)

from backend.api.conrollers.company.auth.parse_auth_token import get_current_company_from_token
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase
from backend.core.db_helper import db_helper

logger = init_logger('company', 'INFO')

router = APIRouter(tags=["company"])


@router.post("/schedule")
async def create_or_update_work_schedule(work_schedule: CompanyWorkScheduleRequest,
                                         company=Depends(get_current_company_from_token),
                                         company_use_case: ICompanyUseCase = Depends(
                                            di_container.get_company_use_cases
                                         ),
                                         session: AsyncSession = Depends(db_helper.session_getter)):
    try:
        updated_work_schedule = await company_use_case.update_work_schedule(
            session,
            company.id,
            work_schedule.model_dump()
        )
    except Exception as ex:
        logger.error("Failed to update company work schedule %s", str(ex), exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(error=f"Failed to update company work schedule").model_dump()
        )

    if updated_work_schedule is None:
        logger.error("Failed to find company work schedule by id %s", company.id)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(error=f"Failed to find company work schedule").model_dump()
        )

    return CompanyWorkScheduleResponse(work_schedule=updated_work_schedule).model_dump(by_alias=True)
