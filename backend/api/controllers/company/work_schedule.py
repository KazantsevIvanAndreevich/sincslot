from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.request.company import CompanyWorkScheduleRequest
from backend.api.response.company import (
    CompanyErrorResponse,
    CompanyWorkScheduleResponse,
    CompanyWorkDayResponse,
)

from backend.api.controllers.company.auth.parse_auth_token import (
    get_current_company_from_token,
)
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase
from backend.core.db_helper import db_helper

logger = init_logger("company", "INFO")

router = APIRouter()


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": CompanyWorkScheduleResponse},
        status.HTTP_404_NOT_FOUND: {"model": CompanyErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CompanyErrorResponse},
    },
)
async def get_work_schedule_company(
    company=Depends(get_current_company_from_token),
    company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        work_schedule = await company_use_case.get_work_schedule_by_company_id(
            session=session, company_id=company.id
        )
    except Exception as ex:
        logger.error(
            "Failed to get company work schedule by id %s Error: %s",
            company.id,
            str(ex),
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(
                error="Failed to get company work schedule by id"
            ).model_dump(),
        )

    if work_schedule is None:
        logger.error("Failed to get company work schedule by id %s", company.id)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(
                error="Failed to get company work schedule by id"
            ).model_dump(),
        )

    work_schedule = [
        CompanyWorkDayResponse(
            day_of_week=ws.get("day_of_week"),
            work_start=ws.get("work_start"),
            work_end=ws.get("work_end"),
        ).model_dump(by_alias=True)
        for ws in work_schedule
    ]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompanyWorkScheduleResponse(work_schedule=work_schedule).model_dump(
            by_alias=True
        ),
    )


@router.post(
    "/",
    responses={
        status.HTTP_200_OK: {"model": CompanyWorkScheduleResponse},
        status.HTTP_404_NOT_FOUND: {"model": CompanyErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CompanyErrorResponse},
    },
)
async def create_or_update_work_schedule(
    work_schedule: CompanyWorkScheduleRequest,
    company=Depends(get_current_company_from_token),
    company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        updated_work_schedule = await company_use_case.update_work_schedule(
            session, company.id, work_schedule.model_dump()
        )
    except Exception as ex:
        logger.error(
            "Failed to update company work schedule %s", str(ex), exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(
                error="Failed to update company work schedule"
            ).model_dump(),
        )

    if updated_work_schedule is None:
        logger.error("Failed to find company work schedule by id %s", company.id)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(
                error="Failed to find company work schedule"
            ).model_dump(),
        )

    return CompanyWorkScheduleResponse(work_schedule=updated_work_schedule).model_dump(
        by_alias=True
    )
