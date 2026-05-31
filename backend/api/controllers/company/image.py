from fastapi import APIRouter, status, Depends, File, UploadFile
from starlette.responses import JSONResponse, FileResponse

from backend.api.response.company import (
    CompanySuccessResponse,
    CompanyErrorResponse,
)

from backend.api.controllers.company.auth.parse_auth_token import (
    get_current_company_from_token,
)
from backend.logger.logger import init_logger
from backend.di_container.di_container import di_container
from backend.use_case.file_use_case import IFileStorage

logger = init_logger("company", "INFO")

router = APIRouter()


@router.get("/")
async def download_image(
    company=Depends(get_current_company_from_token),
    file_storage_use_case: IFileStorage = Depends(
        di_container.get_file_storage_use_case
    ),
):
    try:
        file = await file_storage_use_case.get_file(company_id=company.id)
    except Exception as ex:
        logger.error(
            "Error occurred while getting company by id. Company id: %s Error: %s",
            company.id,
            str(ex),
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(error="failed to get logo image").model_dump(),
        )

    if file is None:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=CompanyErrorResponse(
                error=f"failed to find company logo by id {company.id}"
            ).model_dump(),
        )

    filename, file_path = file[0], file[1]

    return FileResponse(
        path=file_path,
        media_type="image/jpeg",
        filename=filename,
        content_disposition_type="attachment",
    )


@router.put("/")
async def upload_image(
    file: UploadFile = File(...),
    company=Depends(get_current_company_from_token),
    file_storage_use_case: IFileStorage = Depends(
        di_container.get_file_storage_use_case
    ),
):
    if not await file_storage_use_case.is_valid_size(file.size):
        logger.warning("Failed to save company logo %s it is too large", file.size)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(error="file logo is too large").model_dump(),
        )

    extension = await file_storage_use_case.get_extension(file.filename)
    if not extension:
        logger.warning(
            "Failed to save company logo %s it has incorrect extension", extension
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(
                error="file logo has invalid extension"
            ).model_dump(),
        )

    if not await file_storage_use_case.is_valid_extension(extension):
        logger.warning(
            "Failed to save company logo %s it has incorrect extension", file.filename
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(
                error="file logo has invalid extension"
            ).model_dump(),
        )

    try:
        filename = await file_storage_use_case.save_file(
            company_id=company.id, file=file.file
        )
    except Exception as ex:
        logger.error(
            "Error occurred while getting company by id. Company id: %s Error: %s",
            company.id,
            str(ex),
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=CompanyErrorResponse(
                error="failed to save logo image"
            ).model_dump(),
        )

    logger.info("Logo company %s saved successfully", filename)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=CompanySuccessResponse(
            message=f"Logo company {filename} saved successfully"
        ).model_dump(),
    )
