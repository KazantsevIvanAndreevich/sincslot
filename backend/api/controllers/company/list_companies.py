from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.response.company import (
    ListCompanyEntityResponse,
    ListCompanyElemResponse,
)

from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase
from backend.core.db_helper import db_helper

logger = init_logger("list_companies", "INFO")

router = APIRouter()


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": ListCompanyEntityResponse},
    },
)
async def get_company_booking_schedule(
    limit: int | None = None,
    offset: int | None = None,
    company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    try:
        companies = await company_use_case.list_companies(session, limit, offset)
    except Exception as ex:
        logger.error(f"failed to get list companies: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="failed to get list companies",
        )

    list_companies_response: list[dict] = []

    for company in companies:
        list_companies_response.append(
            ListCompanyElemResponse(
                id=company.id,
                name=company.name,
                email=company.email,
                phone=company.phone,
                description=company.description,
                address=company.address,
                slug=company.booking_url.split("/")[-1],
            ).model_dump(exclude_none=True)
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=list_companies_response)
