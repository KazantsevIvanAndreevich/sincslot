from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.response.company import (
    CompanyBySlugResponse,
    CompanyErrorResponse,
)

from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase
from backend.core.db_helper import db_helper

logger = init_logger("get_company_by_slug", "INFO")

router = APIRouter()


@router.get(
    "/{slug}",
    responses={
        status.HTTP_200_OK: {"model": CompanyBySlugResponse},
        status.HTTP_404_NOT_FOUND: {"model": CompanyErrorResponse},
    },
)
async def get_company_by_slug(
    slug: str,
    company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    try:
        company = await company_use_case.get_company_by_slug(session, slug)
    except Exception as ex:
        logger.error(
            "Error occurred while getting company by slug. Company slug: %s Error: %s",
            slug,
            str(ex),
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(
                error=f"failed to find a company with slug {slug}"
            ).model_dump(),
        )

    if company is None:
        logger.warning("Failed to find company by slug. Company slug: %s", slug)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(
                error=f"failed to find a company with slug {slug}"
            ).model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompanyBySlugResponse(**company.to_dict()).model_dump(),
    )
