from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse

from backend.api.controllers.company.auth.parse_auth_token import (
    get_current_company_from_token,
)
from backend.logger.logger import init_logger

logger = init_logger("health", "INFO")

router_health = APIRouter(tags=["health"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


@router_health.get("/health")
async def health():
    logger.info("health ok")
    return JSONResponse(status_code=status.HTTP_200_OK, content="ok")


@router_health.get("/health-auth")
async def health(
    token: str = Depends(oauth2_scheme), company=Depends(get_current_company_from_token)
):
    logger.info("health auth ok. Company id: %s", company.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": f"you have successfully logged in to company {company.name} account"
        },
    )
