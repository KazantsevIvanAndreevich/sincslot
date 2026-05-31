from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.logger.logger import init_logger
from backend.api.response.service import (
    ServiceErrorResponse,
    ServiceEntityListResponse,
    ServiceEntityResponse,
)
from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase
from backend.use_case.service_use_case import IServiceUseCase
from backend.core.db_helper import db_helper

logger = init_logger("get_services_by_company_alias", "INFO")

router = APIRouter()


@router.get(
    "/{alias}",
    responses={
        status.HTTP_200_OK: {"model": ServiceEntityListResponse},
        status.HTTP_404_NOT_FOUND: {"model": ServiceErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServiceErrorResponse},
    },
)
async def get_services_by_company_alias(
    alias: str,
    company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
    service_use_case: IServiceUseCase = Depends(di_container.get_service_use_case),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        company = await company_use_case.get_company_by_booking_url_slug(session, alias)
        if company is None or not company.is_active:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=ServiceErrorResponse(error="Company not found").model_dump(),
            )

        services = await service_use_case.get_services_by_company_id(
            session, company_id=company.id
        )

    except Exception as ex:
        logger.error(
            "Error while getting services by company alias %s: %s",
            alias,
            str(ex),
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ServiceErrorResponse(error="Failed to get services").model_dump(),
        )

    response_services = [
        ServiceEntityResponse(
            id=s.id,
            name=s.name,
            price=s.price,
            duration=s.duration,
            description=s.description,
        )
        for s in services
    ]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ServiceEntityListResponse(services=response_services).model_dump(
            exclude_none=True, by_alias=True
        ),
    )
