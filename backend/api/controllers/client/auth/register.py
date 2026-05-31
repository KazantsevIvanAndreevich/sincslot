from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.request.client import ClientRegisterRequest
from backend.api.response.client import ClientErrorResponse, ClientTokensResponse
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.client_use_case import IClientUseCase
from backend.core.db_helper import db_helper

logger = init_logger("client", "INFO")

router = APIRouter()


@router.post(
    "/register",
    responses={
        status.HTTP_200_OK: {"model": ClientTokensResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ClientErrorResponse},
        status.HTTP_409_CONFLICT: {"model": ClientErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ClientErrorResponse},
    },
)
async def register_client(
    register_request: ClientRegisterRequest,
    client_use_case: IClientUseCase = Depends(di_container.get_client_use_case),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    client_by_phone = await client_use_case.get_client_by_phone(
        session, register_request.phone
    )
    if client_by_phone is not None:
        logger.warning(
            "Failed to create a client with phone %s it is already exist",
            register_request.phone,
        )
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=ClientErrorResponse(
                error=f"client with phone {register_request.phone} is already exist"
            ).model_dump(),
        )

    try:
        new_tokens = await client_use_case.save_client(
            session, register_request.name, register_request.phone
        )
    except Exception as ex:
        logger.error(f"Error occurred while registering new client: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ClientErrorResponse(error="Failed to register client").model_dump(),
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
