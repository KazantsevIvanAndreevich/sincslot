from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.response.service import (
    ServiceErrorResponse,
    ServiceEntityListResponse,
    ServiceEntityResponse,
)
from backend.api.controllers.company.auth.parse_auth_token import (
    get_current_company_from_token,
)
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.service_use_case import IServiceUseCase
from backend.core.db_helper import db_helper

logger = init_logger("get_services_by_company_id", "INFO")

router = APIRouter()


@router.get(
    "/",
    responses=(
        {
            status.HTTP_200_OK: {"model": ServiceEntityListResponse},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServiceErrorResponse},
        }
    ),
)
async def get_services_by_company_id(
    company=Depends(get_current_company_from_token),
    service_use_case: IServiceUseCase = Depends(di_container.get_service_use_case),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        services = await service_use_case.get_services_by_company_id(
            session, company_id=company.id
        )
    except Exception as ex:
        logger.error(
            "Error occurred while finding services by company_id %s Error: %s",
            company.id,
            str(ex),
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ServiceErrorResponse(
                error=f"Failed to get service by company id {company.id}: {str(ex)}"
            ).model_dump(),
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
