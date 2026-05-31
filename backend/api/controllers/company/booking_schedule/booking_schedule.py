import json
from enum import StrEnum

from fastapi import APIRouter, status, Depends, Query
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.controllers.company.auth.parse_auth_token import (
    get_current_company_from_token,
)
from backend.api.response.company import (
    CompanyBookingScheduleResponse,
    CompanyErrorResponse,
)

from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase
from backend.core.db_helper import db_helper

logger = init_logger("booking_schedule", "INFO")

router = APIRouter()


class SortByEnum(StrEnum):
    client_name = "clientName"
    service_name = "serviceName"
    date = "date"
    time = "time"


class SortOrderEnum(StrEnum):
    asc = "asc"
    desc = "desc"


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": CompanyBookingScheduleResponse},
    },
)
async def get_company_booking_schedule(
    sort_by: SortByEnum | None = Query(default=SortByEnum.client_name, alias="sortBy"),
    sort_order: SortOrderEnum | None = Query(
        default=SortOrderEnum.asc, alias="sortOrder"
    ),
    company=Depends(get_current_company_from_token),
    company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    try:
        company_booking_schedule = await company_use_case.get_company_booking_schedule(
            session,
            company.id,
            str(sort_by.value),
            str(sort_order.value),
        )
    except Exception as ex:
        logger.error(
            "Error occurred while getting company booking schedule. Company id: %s Error: %s",
            company.id,
            str(ex),
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(
                error=f"failed to get company booking schedule by company id {company.id}"
            ).model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=json.loads(
            CompanyBookingScheduleResponse(
                bookings=company_booking_schedule
            ).model_dump_json(by_alias=True)
        ),
    )
