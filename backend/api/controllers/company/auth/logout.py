from fastapi import APIRouter, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.logger.logger import init_logger
from backend.api.response.company import (
    CompanyErrorResponse,
    CompanySuccessResponse,
)
from backend.api.controllers.company.auth.parse_auth_token import (
    get_current_company_from_token,
)
from backend.di_container.di_container import di_container
from backend.use_case.token_use_case import IToken
from backend.core.db_helper import db_helper

logger = init_logger("auth_company", "INFO")

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


@router.delete(
    "/logout",
    responses={
        status.HTTP_200_OK: {"model": CompanySuccessResponse},
        status.HTTP_404_NOT_FOUND: {"model": CompanyErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CompanyErrorResponse},
    },
)
async def logout(
    request: Request,
    company=Depends(get_current_company_from_token),
    token_use_case: IToken = Depends(di_container.get_token_use_case),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    refresh_token = request.cookies.get("refreshToken")
    if refresh_token is None:
        logger.error("Refresh token was not provided")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(
                error="Refresh token was not provided"
            ).model_dump(),
        )

    payload = await token_use_case.decode_token(refresh_token)
    if not int(payload.get("company_id")) == company.id:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(
                error="Companies ids from access token and from refresh token do not match"
            ).model_dump(),
        )

    try:
        await token_use_case.revoke_tokens(session, refresh_token, True)
    except Exception as ex:
        logger.error(f"Error occurred while revoking tokens: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(error="Failed to revoke token").model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompanySuccessResponse(message="Success logout").model_dump(),
    )
