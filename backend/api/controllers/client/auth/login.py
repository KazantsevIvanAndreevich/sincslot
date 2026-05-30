from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.request.client import ClientLoginRequest
from backend.api.response.client import ClientErrorResponse, ClientTokensResponse
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.client_use_case import IClientUseCase
from backend.core.db_helper import db_helper

logger = init_logger("client", "INFO")

router_client_auth_login = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


@router_client_auth_login.post(
    "/login",
    responses={
        status.HTTP_201_CREATED: {"model": ClientTokensResponse},
        status.HTTP_404_NOT_FOUND: {"model": ClientErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ClientErrorResponse},
    },
)
async def login_client(
    login_input: ClientLoginRequest,
    client_use_case: IClientUseCase = Depends(di_container.get_client_use_case),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    client = await client_use_case.get_client_by_phone(session, login_input.phone)
    if client is None:
        logger.warning(
            "Failed to get client by phone %s. Impossible to log in", login_input.phone
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ClientErrorResponse(
                error=f"Client with email {login_input.phone} does not exist"
            ).model_dump(),
        )

    try:
        new_tokens = await client_use_case.login(session, client)
    except Exception as ex:
        logger.error(f"Error occurred while log in client: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ClientErrorResponse(error="Failed to log in").model_dump(),
        )

    response = JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=ClientTokensResponse(
            access_token=new_tokens.access_token,
        ).model_dump(by_alias=True),
    )

    response.set_cookie(
        key="refreshToken",
        value=new_tokens.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/api/v1/company/refresh-token",
    )

    return response
