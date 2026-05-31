from fastapi import APIRouter, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from backend.logger.logger import init_logger
from backend.api.response.company import (
    CompanyTokensResponse,
    CompanyErrorResponse,
)
from backend.di_container.di_container import di_container
from backend.use_case.token_use_case import IToken
from backend.core.db_helper import db_helper

logger = init_logger("auth_company", "INFO")

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


@router.post(
    "/refresh-token",
    responses={
        status.HTTP_201_CREATED: {"model": CompanyTokensResponse},
        status.HTTP_400_BAD_REQUEST: {"model": CompanyErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CompanyErrorResponse},
    },
)
async def refresh_tokens(
    request: Request,
    token_use_case: IToken = Depends(di_container.get_token_use_case),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    refresh_token = request.cookies.get("refreshToken")

    if refresh_token is None:
        logger.error("Refresh token was not provided")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(
                error="Refresh token was not provided"
            ).model_dump(),
        )

    try:
        decoded_token = await token_use_case.decode_token(refresh_token)
    except JWTError as ex:
        logger.error("Failed to parse refresh token: %s", str(ex))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(
                error="Failed to parse refresh token"
            ).model_dump(),
        )

    is_refresh = await token_use_case.is_refresh_token(decoded_token.get("type"))
    if not is_refresh:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(
                error="Provided token is not refresh token"
            ).model_dump(),
        )

    try:
        new_tokens = await token_use_case.update_tokens(session, refresh_token)
    except Exception as ex:
        logger.error(
            "Error occurred while refreshing tokens %s:", str(ex), exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(error="Failed to update toens").model_dump(),
        )

    if new_tokens is None:
        logger.error(
            "Failed to update tokens. Probably refresh token was not in db %s:",
            refresh_token,
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(error="Failed to update tokens").model_dump(),
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
