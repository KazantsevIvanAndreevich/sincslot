from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.request.company import CompanyCreateRequest
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
    "/register",
    responses={
        status.HTTP_200_OK: {"model": CompanyTokensResponse},
        status.HTTP_400_BAD_REQUEST: {"model": CompanyErrorResponse},
        status.HTTP_409_CONFLICT: {"model": CompanyErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CompanyErrorResponse},
    },
)
async def register(
    company: CompanyCreateRequest,
    company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    if company.password.strip() != company.repeat_password.strip():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(error="passwords do not match").model_dump(),
        )

    company_by_email = await company_use_case.get_company_by_email(
        session, company.email
    )
    if company_by_email is not None:
        logger.warning(
            "Failed to create a company with email %s it is already exist",
            company.email,
        )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=CompanyErrorResponse(
                error=f"company with email {company.email} is already exist"
            ).model_dump(),
        )

    company_by_phone = await company_use_case.get_company_by_phone(
        session, company.phone
    )
    if company_by_phone is not None:
        logger.warning(
            "Failed to create a company with phone %s it is already exist",
            company.phone,
        )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=CompanyErrorResponse(
                error=f"company with phone {company.phone} is already exist"
            ).model_dump(),
        )

    company_by_name = await company_use_case.get_company_by_name(session, company.name)
    if company_by_name is not None:
        logger.warning(
            "Failed to create a company with name %s it is already exist", company.name
        )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=CompanyErrorResponse(
                error=f"company with name {company.name} is already exist"
            ).model_dump(),
        )

    try:
        new_tokens = await company_use_case.save_company(
            session,
            name=company.name,
            email=company.email,
            phone=company.phone,
            address=company.address,
            password=company.password,
        )
    except Exception as ex:
        logger.error(f"Error occurred while registering new company: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(
                error="Failed to register company"
            ).model_dump(),
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
