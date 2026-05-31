from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.response.service import ServiceErrorResponse, ServiceEntityResponse
from backend.api.controllers.company.auth.parse_auth_token import (
    get_current_company_from_token,
)
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.service_use_case import IServiceUseCase
from backend.core.db_helper import db_helper

logger = init_logger("get_service_by_id", "INFO")

router = APIRouter()


@router.get(
    "/{service_id}",
    responses=(
        {
            status.HTTP_200_OK: {"model": ServiceEntityResponse},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServiceErrorResponse},
            status.HTTP_404_NOT_FOUND: {"model": ServiceErrorResponse},
        }
    ),
)
async def get_service_by_id(
    service_id: int,
    company=Depends(get_current_company_from_token),
    service_use_case: IServiceUseCase = Depends(di_container.get_service_use_case),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        service = await service_use_case.get_service_by_id(session, service_id)
    except Exception as ex:
        logger.error(
            "Error occurred while finding service by id %s Error: %s",
            service_id,
            str(ex),
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ServiceErrorResponse(
                error=f"Failed to get service by id {service_id}: {str(ex)}"
            ).model_dump(),
        )

    if service is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ServiceErrorResponse(
                error=f"Failed to find service by id {service_id}"
            ).model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ServiceEntityResponse(
            id=service.id,
            name=service.name,
            price=service.price,
            duration=service.duration,
            description=service.description,
        ).model_dump(exclude_none=True, by_alias=True),
    )
