from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.request.company import CompanyUpdateSettingsRequest
from backend.api.response.company import (
    CompanySettingsResponse,
    CompanyErrorResponse,
)
from backend.use_case.company_use_case import ICompanyUseCase
from backend.api.controllers.company.auth.parse_auth_token import (
    get_current_company_from_token,
)
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.core.db_helper import db_helper

logger = init_logger("company_settings", "INFO")

router = APIRouter()


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {"model": CompanySettingsResponse},
        status.HTTP_400_BAD_REQUEST: {"model": CompanyErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CompanyErrorResponse},
    },
)
async def get_settings_company(
    company=Depends(get_current_company_from_token),
    company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    try:
        company_by_id = await company_use_case.get_company_by_id(session, company.id)
    except Exception as ex:
        logger.error(
            "Error occurred while getting company by id. Company id: %s Error: %s",
            company.id,
            str(ex),
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(
                error=f"failed to find a company with id {company.id}"
            ).model_dump(),
        )

    if company_by_id is None:
        logger.warning("Failed to find company by id. Company id: %s", company.id)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(
                error=f"failed to find a company with id {company.id}"
            ).model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompanySettingsResponse(
            name=company_by_id.name,
            address=company_by_id.address,
            email=company_by_id.email,
            phone=company_by_id.phone,
            slug_booking_url=company_by_id.booking_url.split("/")[-1],
            description=company_by_id.description,
        ).model_dump(by_alias=True),
    )


@router.patch(
    "/",
    responses={
        status.HTTP_200_OK: {"model": CompanySettingsResponse},
        status.HTTP_400_BAD_REQUEST: {"model": CompanyErrorResponse},
        status.HTTP_409_CONFLICT: {"model": CompanyErrorResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": CompanyErrorResponse},
    },
)
async def update_settings_company(
    company_settings: CompanyUpdateSettingsRequest,
    company=Depends(get_current_company_from_token),
    company_use_case: ICompanyUseCase = Depends(di_container.get_company_use_cases),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    company_by_email = await company_use_case.get_company_by_email(
        session, company_settings.email
    )
    if company_by_email is not None:
        if company_by_email.id != company.id:
            logger.warning(
                "Failed to update a company with email %s it is already exist",
                company_settings.email,
            )
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=CompanyErrorResponse(
                    error=f"company with email {company_settings.email} is already exist"
                ).model_dump(),
            )

    company_by_phone = await company_use_case.get_company_by_phone(
        session, company_settings.phone
    )
    if company_by_phone is not None:
        if company_by_phone.id != company.id:
            logger.warning(
                "Failed to update a company with phone %s it is already exist",
                company_settings.phone,
            )
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=CompanyErrorResponse(
                    error=f"company with phone {company_settings.phone} is already exist"
                ).model_dump(),
            )

    company_by_name = await company_use_case.get_company_by_name(
        session, company_settings.name
    )
    if company_by_name is not None:
        if company_by_name.id != company.id:
            logger.warning(
                "Failed to update a company with name %s it is already exist",
                company_settings.name,
            )
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=CompanyErrorResponse(
                    error=f"user company name {company_settings.name} is already exist"
                ).model_dump(),
            )

    company_by_slug = await company_use_case.get_company_by_booking_url_slug(
        session, company_settings.slug_booking_url
    )
    if company_by_slug is not None:
        if company_by_slug.id != company.id:
            logger.warning(
                "Failed to update a company with booking url slug %s it is already exist",
                company_settings.name,
            )
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=CompanyErrorResponse(
                    error=f"user company booking url {company_settings.slug_booking_url} is already exist"
                ).model_dump(),
            )

    company_to_update = company_settings.model_dump()

    new_password = company_to_update.get("new_password")
    new_repeat_password = company_to_update.get("new_repeat_password")

    is_empty_pass = new_password != "" and new_repeat_password != ""
    is_null_pass = new_password is not None and new_repeat_password is not None

    if is_empty_pass and is_null_pass:
        company_by_id = await company_use_case.get_company_by_id(session, company.id)

        is_match_password = await company_use_case.verify_password(
            company_settings.current_password, company_by_id.password
        )

        if not is_match_password:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=CompanyErrorResponse(
                    error="Incorrect current password. Impossible to set new password"
                ).model_dump(),
            )

        company_to_update["password"] = company_to_update.get("new_password")
    else:
        company_to_update["password"] = ""

    try:
        updated_data = await company_use_case.update_company_by_id(
            session=session,
            company_id=company.id,
            name=company_to_update.get("name"),
            email=company_to_update.get("email"),
            password=company_to_update.get("password"),
            phone=company_to_update.get("phone"),
            slug_booking_url=company_to_update.get("slug_booking_url"),
            description=company_to_update.get("description"),
            address=company_to_update.get("address"),
        )
    except Exception as ex:
        logger.error(f"Error occurred while updating company settings: {str(ex)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=CompanyErrorResponse(error="Failed to update company").model_dump(),
        )

    if updated_data is None:
        logger.error("Error occurred while updating company settings")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=CompanyErrorResponse(error="Failed to update company").model_dump(),
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=CompanySettingsResponse(
            name=updated_data.name,
            address=updated_data.address,
            email=updated_data.email,
            phone=updated_data.phone,
            slug_booking_url=updated_data.booking_url.split("/")[-1],
            description=updated_data.description,
        ).model_dump(by_alias=True),
    )
