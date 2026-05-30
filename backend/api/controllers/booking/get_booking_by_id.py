from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.logger.logger import init_logger
from backend.api.response.booking import (
    BookingErrorResponse,
    BookingCalendarScheduleResponse,
)

from backend.di_container.di_container import di_container
from backend.use_case.booking_use_case import IBookingUseCase
from backend.use_case.company_use_case import ICompanyUseCase
from backend.core.db_helper import db_helper

logger = init_logger("get_booking_by_id", "INFO")

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


@router.get(
    "/company/{slug}/service/{service_id}",
    responses={
        status.HTTP_200_OK: {"model": BookingCalendarScheduleResponse},
        status.HTTP_400_BAD_REQUEST: {"model": BookingErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": BookingErrorResponse},
    },
)
async def get_booking_by_id(
    slug: str,
    service_id: int,
    booking_use_case: IBookingUseCase = Depends(di_container.get_booking_use_case),
    company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    company = await company_use_case.get_company_by_slug(session, slug)

    work_schedule = await company_use_case.get_work_schedule_by_company_id(
        session, company.id
    )
    if work_schedule is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=BookingErrorResponse(
                error=f"Failed to find work schedule for company {company.id}"
            ),
        )

    try:
        calendar_schedule = await booking_use_case.get_calendar_schedule_booking(
            session, service_id, company.id, work_schedule
        )
    except Exception as ex:
        logger.warning("Error occurred: %s", str(ex))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=BookingErrorResponse(
                error=f"Error occurred: {str(ex)}"
            ).model_dump(),
        )

    if calendar_schedule is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=BookingErrorResponse(
                error=f"Service with id {service_id} was not found"
            ).model_dump(),
        )

    result = BookingCalendarScheduleResponse(
        id=calendar_schedule.get("id"),
        name=calendar_schedule.get("name"),
        duration=calendar_schedule.get("duration"),
        price=calendar_schedule.get("price"),
        schedule=calendar_schedule.get("schedule"),
    ).model_dump(exclude_none=True, by_alias=True)

    result["schedule"] = calendar_schedule.get("schedule")

    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
