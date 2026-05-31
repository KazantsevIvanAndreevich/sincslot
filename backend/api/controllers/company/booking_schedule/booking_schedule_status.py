from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.controllers.company.auth.parse_auth_token import (
    get_current_company_from_token,
)
from backend.api.request.company import CompanyBookingScheduleStatus
from backend.api.response.booking import BookingErrorResponse
from backend.api.response.company import CompanyBookingStatusResponse
from backend.entity.booking import BookingStatus
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.booking_use_case import IBookingUseCase
from backend.core.db_helper import db_helper

logger = init_logger("booking_schedule_status", "INFO")

router = APIRouter()


@router.patch(
    "/{booking_id}",
    responses={
        status.HTTP_200_OK: {"model": CompanyBookingScheduleStatus},
    },
)
async def change_booking_schedule_status(
    booking_id: int,
    booking_status: BookingStatus,
    company=Depends(get_current_company_from_token),
    booking_use_case: IBookingUseCase = Depends(di_container.get_booking_use_case),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    booking_by_id = await booking_use_case.get_booking_by_id(session, booking_id)
    if booking_by_id is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=BookingErrorResponse(
                error=f"Booking with id {booking_id} does not exist"
            ).model_dump(),
        )

    updated_booking = await booking_use_case.update_booking_by_id(
        session, booking_id, str(booking_status.value)
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompanyBookingStatusResponse(
            status=updated_booking.status
        ).model_dump(),
    )
