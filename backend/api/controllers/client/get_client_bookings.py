import json

from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.response.client import ClientBookingsResponse
from backend.api.response.company import CompanyErrorResponse
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.booking_use_case import IBookingUseCase
from backend.api.controllers.client.auth.parse_aurh_token import (
    get_current_client_from_token,
)
from backend.core.db_helper import db_helper

logger = init_logger("get_client_bookings", "INFO")

router = APIRouter()


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": ClientBookingsResponse},
        status.HTTP_404_NOT_FOUND: {"model": CompanyErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CompanyErrorResponse},
    },
)
async def get_client_bookings(
    client=Depends(get_current_client_from_token),
    booking_use_case: IBookingUseCase = Depends(di_container.get_booking_use_case),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        client_bookings = await booking_use_case.get_booking_by_client(
            session, client_id=client.id
        )
    except Exception as ex:
        logger.warning(
            "Failed to get client booking by client id %s. Error %s", client.id, str(ex)
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(
                error=f"Failed to get client booking by client id {client.id}"
            ).model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        media_type="application/json",
        content=json.loads(
            ClientBookingsResponse(client_bookings=client_bookings).model_dump_json(
                by_alias=True
            )
        ),
    )
