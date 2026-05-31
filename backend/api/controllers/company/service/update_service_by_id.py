from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.request.service import ServiceUpdateRequest
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


@router.patch(
    "/{service_id}",
    responses=(
        {
            status.HTTP_200_OK: {"model": ServiceEntityResponse},
            status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServiceErrorResponse},
        }
    ),
)
async def update_service_by_id(
    service_id: int,
    data_to_update: ServiceUpdateRequest,
    company=Depends(get_current_company_from_token),
    service_use_case: IServiceUseCase = Depends(di_container.get_service_use_case),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        updated_service = await service_use_case.update_service_by_id(
            session,
            service_id=service_id,
            name=data_to_update.name,
            price=data_to_update.price,
            duration=data_to_update.duration,
            description=data_to_update.description,
        )
    except Exception as ex:
        logger.error(
            "Failed to update service %s Error: %s", service_id, str(ex), exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ServiceErrorResponse(error="Failed to update service").model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=ServiceEntityResponse(
            id=updated_service.id,
            name=updated_service.name,
            price=updated_service.price,
            duration=updated_service.duration,
            description=updated_service.description,
        ).model_dump(exclude_none=True, by_alias=True),
    )
