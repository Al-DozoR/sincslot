from datetime import timezone

from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.request.booking import BookingCreateRequest
from backend.api.response.booking import BookingGetById, BookingErrorResponse
from backend.logger.logger import init_logger
from backend.api.controllers.client.auth.parse_aurh_token import get_current_client_from_token
from backend.di_container.di_container import di_container
from backend.use_case.booking_use_case import IBookingUseCase
from backend.core.db_helper import db_helper

logger = init_logger('create_booking', 'INFO')

router = APIRouter()


@router.post("/company/{company_id}/service/{service_id}", responses={
    status.HTTP_200_OK: {"model": BookingGetById},
    status.HTTP_409_CONFLICT: {"model": BookingErrorResponse},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": BookingErrorResponse},
})
async def create_booking(
        service_id: int,
        company_id: int,
        create_booking_request: BookingCreateRequest,
        client=Depends(get_current_client_from_token),
        booking_use_case: IBookingUseCase = Depends(di_container.get_booking_use_case),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    booking = await booking_use_case.get_booking_by_service_id_and_client_id(session, service_id, client.id)
    if booking is not None:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=BookingErrorResponse(
                error=f"Client with id {client.id} has already booked the service with id {service_id}").model_dump()
        )

    time_start = create_booking_request.start_booking.replace(tzinfo=timezone.utc)
    time_end = create_booking_request.end_booking.replace(tzinfo=timezone.utc)

    try:
        if not await booking_use_case.is_booking_time_in_work_schedule(session, company_id, time_start, time_end):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=BookingErrorResponse(
                    error=f"Время начала или окончания услуги не укладывается в расписание кампании").model_dump()
            )
    except Exception as ex:
        logger.error("Failed to check company schedule for booking for client id %s. Error %s", client.id, str(ex))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=BookingErrorResponse(
                error=f"Failed to check company schedule for booking for client id {client.id}"
            ).model_dump()
        )

    try:
        booking_id = await booking_use_case.save_booking(
            session,
            service_id,
            client_id=client.id,
            time_start=create_booking_request.start_booking.replace(tzinfo=timezone.utc),
            time_end=create_booking_request.end_booking.replace(tzinfo=timezone.utc),
        )
    except Exception as ex:
        logger.error("Failed to create booking for client id %s. Error %s", client.id, str(ex))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=BookingErrorResponse(
                error=f"Failed to create booking for client {client.id}"
            ).model_dump()
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=BookingGetById(booking_id=booking_id).model_dump()
    )
