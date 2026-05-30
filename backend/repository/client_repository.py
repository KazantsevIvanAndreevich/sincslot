from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.entity.client import ClientEntity
from backend.repository.models.client import Client
from backend.repository.unit_of_work.unit_of_work import UnitOfWork


class IClientRepository(ABC):
    @abstractmethod
    async def save_client(
        self,
        session: AsyncSession,
        name: str,
        phone: str,
    ) -> ClientEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_client_by_id(
        self, session: AsyncSession, client_id: int
    ) -> ClientEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_client_by_name(
        self, session: AsyncSession, name: str
    ) -> ClientEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_client_by_phone(
        self, session: AsyncSession, phone: str
    ) -> ClientEntity | None:
        raise NotImplementedError


class ClientRepository(IClientRepository):
    async def save_client(
        self,
        session: AsyncSession,
        name: str,
        phone: str,
    ) -> ClientEntity:
        new_client = Client(
            name=name,
            phone=phone,
        )

        async with UnitOfWork(session) as uow:
            await uow.add(new_client)

        return new_client.to_client_entity()

    async def get_client_by_id(
        self, session: AsyncSession, client_id: int
    ) -> ClientEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Client).where(Client.id == client_id)
            client = await uow.execute_query(query)
            client_scalar: Client | None = client.scalar()
            if client_scalar is None:
                return

        return client_scalar.to_client_entity()

    async def get_client_by_name(
        self, session: AsyncSession, name: str
    ) -> ClientEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Client).where(Client.name == name)
            client = await uow.execute_query(query)
            client_scalar: Client | None = client.scalar()
            if client_scalar is None:
                return

        return client_scalar.to_client_entity()

    async def get_client_by_phone(
        self, session: AsyncSession, phone: int
    ) -> ClientEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Client).where(Client.phone == phone)
            client = await uow.execute_query(query)
            client_scalar: Client | None = client.scalar()
            if client_scalar is None:
                return

        return client_scalar.to_client_entity()
