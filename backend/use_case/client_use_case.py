from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from backend.entity.client import ClientEntity
from backend.entity.token import TokenEntity
from backend.logger.logger import init_logger
from backend.repository.client_repository import IClientRepository
from backend.use_case.token_use_case import IToken

logger = init_logger("company_use_case", "INFO")


class IClientUseCase(ABC):
    @abstractmethod
    async def save_client(
        self,
        session: AsyncSession,
        name: str,
        phone: str,
    ):
        raise NotImplementedError

    @abstractmethod
    async def get_client_by_id(
        self, session: AsyncSession, client_id: int
    ) -> ClientEntity:
        raise NotImplementedError

    async def get_client_by_name(
        self, session: AsyncSession, name: str
    ) -> ClientEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_client_by_phone(
        self, session: AsyncSession, phone: str
    ) -> ClientEntity:
        raise NotImplementedError

    @abstractmethod
    async def login(self, session: AsyncSession, client: ClientEntity) -> TokenEntity:
        raise NotImplementedError


class ClientUseCase(IClientUseCase):
    def __init__(self, client_repository: IClientRepository, token: IToken):
        self.client_repository = client_repository
        self.token = token

    async def save_client(
        self,
        session: AsyncSession,
        name: str,
        phone: str,
    ) -> TokenEntity:
        client = await self.client_repository.save_client(session, name, phone)

        access_token = await self.token.create_access_token_client(
            client_id=client.id, client_name=client.name, client_phone=client.phone
        )
        refresh_token = await self.token.create_refresh_token_client(
            client_id=client.id, client_name=client.name, client_phone=client.phone
        )

        tokens = await self.token.save_tokens(
            session, access_token, refresh_token, is_revoke=False
        )

        return tokens

    async def get_client_by_id(
        self, session: AsyncSession, client_id: int
    ) -> ClientEntity:
        return await self.client_repository.get_client_by_id(session, client_id)

    async def get_client_by_name(
        self, session: AsyncSession, name: str
    ) -> ClientEntity:
        return await self.client_repository.get_client_by_name(session, name)

    async def get_client_by_phone(
        self, session: AsyncSession, phone: str
    ) -> ClientEntity:
        return await self.client_repository.get_client_by_phone(session, phone)

    async def login(self, session: AsyncSession, client: ClientEntity) -> TokenEntity:
        access_token = await self.token.create_access_token_client(
            client_id=client.id, client_name=client.name, client_phone=client.phone
        )
        refresh_token = await self.token.create_refresh_token_client(
            client_id=client.id, client_name=client.name, client_phone=client.phone
        )

        tokens = await self.token.save_tokens(
            session, access_token, refresh_token, is_revoke=False
        )

        return tokens
