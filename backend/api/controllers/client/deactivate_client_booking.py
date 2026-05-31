from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.booking_use_case import IBookingUseCase
from backend.api.controllers.client.auth.parse_aurh_token import (
    get_current_client_from_token,
)
from backend.api.response.company import CompanyErrorResponse
from backend.core.db_helper import db_helper

logger = init_logger("deactivate_client_booking", "INFO")

router = APIRouter()


@router.post(
    "/{booking_id}/cancel",
    responses={
        status.HTTP_200_OK: {"description": "Booking cancelled"},
        status.HTTP_404_NOT_FOUND: {"model": CompanyErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CompanyErrorResponse},
    },
)
async def deactivate_client_booking(
    booking_id: int,
    client=Depends(get_current_client_from_token),
    booking_use_case: IBookingUseCase = Depends(di_container.get_booking_use_case),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        booking = await booking_use_case.get_booking_by_id(session, booking_id)
    except Exception as ex:
        logger.error(
            "Failed to get booking by id %s. Error: %s",
            booking_id,
            str(ex),
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(error="Failed to get booking").model_dump(),
        )

    if booking is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(error="Booking not found").model_dump(),
        )

    if booking.client_id != client.id:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(error="Booking not found").model_dump(),
        )

    try:
        await booking_use_case.update_booking_by_id(
            session=session,
            booking_id=booking_id,
            status="cancelled",
        )
    except Exception as ex:
        logger.error(
            "Failed to cancel booking %s. Error: %s", booking_id, str(ex), exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(error="Failed to cancel booking").model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Booking cancelled successfully"},
    )
