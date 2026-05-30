import os
import aiofiles
from typing import BinaryIO
from abc import ABC, abstractmethod

from backend.core.config import FileCompanyLogoSettings


class IFileStorage(ABC):
    @abstractmethod
    async def is_valid_extension(self, extension: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_extension(self, filename: str) -> str | bool:
        raise NotImplementedError

    @abstractmethod
    async def is_valid_size(self, size: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def save_file(self, company_id: int, file: BinaryIO) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get_file(self, company_id: int) -> tuple[str, str] | None:
        raise NotImplementedError

    @abstractmethod
    async def remove_file(self, filename: str) -> bool:
        raise NotImplementedError


class FileCompanyLogoStorage(IFileStorage):
    def __init__(self, file_company_logo_settings: FileCompanyLogoSettings):
        self.file_company_logo_settings = file_company_logo_settings

    async def get_extension(self, filename: str) -> str | bool:
        if "." not in filename:
            return False

        return filename.split(".")[-1]

    async def is_valid_extension(self, extension: str) -> bool:
        return extension in self.file_company_logo_settings.valid_extensions

    async def is_valid_size(self, size: int) -> bool:
        return self.file_company_logo_settings.max_file_size_mb * 1024 * 1024 > size

    async def save_file(self, company_id: int, file: BinaryIO) -> str:
        if not os.path.isdir(self.file_company_logo_settings.path_file):
            os.mkdir(self.file_company_logo_settings.path_file)

        filename: str = f"{company_id}_company_logo.jpeg"

        path_to_save: str = os.path.join(
            self.file_company_logo_settings.path_file, filename
        )

        async with aiofiles.open(path_to_save, "wb") as buffer:
            data = file.read()
            await buffer.write(data)

        return filename

    async def get_file(self, company_id: int) -> tuple[str, str] | None:
        files = os.listdir(self.file_company_logo_settings.path_file)

        for file in files:
            file_id = file.split("_")[0]
            if int(file_id) == company_id:
                return file, os.path.join(
                    self.file_company_logo_settings.path_file, file
                )

    async def remove_file(self, company_id: int) -> bool:
        files = os.listdir(self.file_company_logo_settings.path_file)

        for file in files:
            file_id = file.split("_")[0]
            if int(file_id) == company_id:
                os.remove(
                    os.path.join(self.file_company_logo_settings.path_file, filename)
                )
                return True

        return False
