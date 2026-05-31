from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.request.service import ServiceCreateRequest

from backend.api.response.service import (
    ServiceEntityResponse,
    ServiceErrorResponse,
)

from backend.logger.logger import init_logger
from backend.api.controllers.company.auth.parse_auth_token import (
    get_current_company_from_token,
)
from backend.di_container.di_container import di_container
from backend.use_case.service_use_case import IServiceUseCase
from backend.core.db_helper import db_helper

logger = init_logger("create_service", "INFO")

router = APIRouter()


@router.post(
    "/",
    responses={
        status.HTTP_201_CREATED: {"model": ServiceEntityResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ServiceErrorResponse},
    },
)
async def create_service(
    service: ServiceCreateRequest,
    company=Depends(get_current_company_from_token),
    service_use_case: IServiceUseCase = Depends(di_container.get_service_use_case),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    try:
        new_service = await service_use_case.save_service(
            session,
            name=service.name,
            price=service.price,
            duration=service.duration,
            description=service.description,
            company_id=company.id,
        )
    except Exception as ex:
        logger.error("Failed to save service %s", str(ex), exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ServiceErrorResponse(error="Failed to save service").model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=ServiceEntityResponse(
            id=new_service.id,
            name=new_service.name,
            price=new_service.price,
            duration=new_service.duration,
            description=new_service.description,
            company_id=new_service.company_id,
        ).model_dump(exclude_none=True, by_alias=True),
    )
