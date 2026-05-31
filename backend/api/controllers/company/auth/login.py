from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.request.company import (
    CompanyLoginRequest,
)
from backend.logger.logger import init_logger
from backend.api.response.company import (
    CompanyTokensResponse,
    CompanyErrorResponse,
)
from backend.di_container.di_container import di_container
from backend.use_case.company_use_case import ICompanyUseCase
from backend.core.db_helper import db_helper

logger = init_logger("auth_company", "INFO")

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


@router.post(
    "/login",
    responses={
        status.HTTP_201_CREATED: {"model": CompanyTokensResponse},
        status.HTTP_404_NOT_FOUND: {"model": CompanyErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CompanyErrorResponse},
    },
)
async def login_company(
    login_input: CompanyLoginRequest,
    company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    company = await company_use_case.get_company_by_email(session, login_input.email)
    if company is None:
        logger.warning(
            "Failed to get company by email %s. Impossible to log in", login_input.email
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(
                error=f"Company with email {login_input.email} does not exist"
            ).model_dump(),
        )
    if not company.is_active:
        logger.warning("Company %s is inactive. Login forbidden", login_input.email)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=CompanyErrorResponse(
                error="Company is deactivated and cannot log in"
            ).model_dump(),
        )
    if not await company_use_case.verify_password(
        login_input.password, company.password
    ):
        logger.warning(
            "Failed to verify password %s. Impossible to log in", login_input.password
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(error="Incorrect password").model_dump(),
        )

    try:
        new_tokens = await company_use_case.login(session, company)
    except Exception as ex:
        logger.error(f"Error occurred while log in company: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(error="Failed to log in").model_dump(),
        )

    response = JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CompanyTokensResponse(
            access_token=new_tokens.access_token,
        ).model_dump(by_alias=True),
    )

    response.set_cookie(
        key="refreshToken",
        value=new_tokens.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/api/v1/company/auth/refresh-token",
    )

    return response
