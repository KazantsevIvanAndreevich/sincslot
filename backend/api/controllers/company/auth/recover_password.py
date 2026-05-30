from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.request.company import CompanyRecoverPasswordRequest
from backend.logger.logger import init_logger
from backend.api.response.company import (
    CompanyErrorResponse,
    CompanyRecoverPasswordResponse,
)
from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase
from backend.core.db_helper import db_helper

logger = init_logger("auth_company", "INFO")

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


@router.post(
    "/recover",
    responses={
        status.HTTP_200_OK: {"model": CompanyRecoverPasswordResponse},
        status.HTTP_404_NOT_FOUND: {"model": CompanyErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CompanyErrorResponse},
    },
)
async def recover_password(
    recover_pass: CompanyRecoverPasswordRequest,
    company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    company_by_email = await company_use_case.get_company_by_email(
        session, recover_pass.email
    )
    if company_by_email is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(
                error=f"user with email {recover_pass.email} does not exist"
            ).model_dump(),
        )

    try:
        await company_use_case.recover_company_by_email(session, recover_pass.email)
    except Exception as ex:
        logger.error(f"Error occurred while recovering: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(
                error="Failed to recover password"
            ).model_dump(),
        )

    return Response(status_code=status.HTTP_200_OK)
