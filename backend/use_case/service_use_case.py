from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from backend.logger.logger import init_logger
from backend.repository.service_repository import IServiceRepository
from backend.entity.service import ServiceEntity

logger = init_logger("company_use_case", "INFO")


class IServiceUseCase(ABC):
    @abstractmethod
    async def save_service(
        self,
        session: AsyncSession,
        name: str,
        duration: int,
        price: int,
        company_id: int,
        description: str | None = None,
    ) -> ServiceEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_service_by_id(
        self, session: AsyncSession, service_id: int
    ) -> ServiceEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_services_by_company_id(
        self, session: AsyncSession, company_id: int
    ) -> list[ServiceEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update_service_by_id(
        self,
        session: AsyncSession,
        service_id: int,
        name: str,
        duration: int,
        price: int,
        description: str | None = None,
    ) -> ServiceEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def remove_service_by_id(
        self, session: AsyncSession, service_id: int
    ) -> bool:
        raise NotImplementedError


class ServiceUseCase(IServiceUseCase):
    def __init__(self, service_repository: IServiceRepository):
        self.service_repository = service_repository

    async def save_service(
        self,
        session: AsyncSession,
        name: str,
        duration: int,
        price: int,
        company_id: int,
        description: str | None = None,
    ):
        return await self.service_repository.save_service(
            session,
            ServiceEntity(
                name=name,
                duration=duration,
                price=price,
                company_id=company_id,
                description=description,
                is_active=True,
            ),
        )

    async def get_service_by_id(self, session: AsyncSession, service_id: int):
        return await self.service_repository.get_service_by_id(session, service_id)

    async def get_services_by_company_id(
        self, session: AsyncSession, company_id: int
    ) -> list[ServiceEntity]:
        return await self.service_repository.get_services_by_company_id(
            session, company_id
        )

    async def update_service_by_id(
        self,
        session: AsyncSession,
        service_id: int,
        name: str,
        duration: int,
        price: int,
        description: str | None = None,
    ) -> ServiceEntity | None:
        data_to_update = {
            "name": name,
            "duration": duration,
            "price": price,
            "description": description,
        }

        return await self.service_repository.update_service(
            session, service_id, data_to_update
        )

    async def remove_service_by_id(
        self, session: AsyncSession, service_id: int
    ) -> bool:
        return await self.service_repository.remove_service(session, service_id)
