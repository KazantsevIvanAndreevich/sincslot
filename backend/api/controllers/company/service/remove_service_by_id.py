from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.response.service import ServiceErrorResponse, ServiceRemoveResponse
from backend.api.controllers.company.auth.parse_auth_token import (
    get_current_company_from_token,
)
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.service_use_case import IServiceUseCase
from backend.core.db_helper import db_helper

logger = init_logger("remove_service_by_id", "INFO")

router = APIRouter()


@router.delete("/{service_id}")
async def remove_service_by_id(
    service_id: int,
    company=Depends(get_current_company_from_token),
    service_use_case: IServiceUseCase = Depends(di_container.get_service_use_case),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        is_removed = await service_use_case.remove_service_by_id(session, service_id)
    except Exception as ex:
        logger.error(
            "Error occurred while removing service by id by company %s Error: %s",
            service_id,
            company.id,
            str(ex),
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ServiceErrorResponse(
                error=f"Failed to remove service by id {service_id}"
            ).model_dump(),
        )

    if not is_removed:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ServiceErrorResponse(
                error=f"Failed to remove service with id {service_id}"
            ).model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ServiceRemoveResponse(is_removed=is_removed).model_dump(),
    )
