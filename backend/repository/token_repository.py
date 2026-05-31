from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from backend.entity.token import TokenEntity
from backend.repository.models.token import Token
from backend.repository.unit_of_work.unit_of_work import UnitOfWork


class ITokenRepository(ABC):
    @abstractmethod
    async def save_tokens(
        self,
        session: AsyncSession,
        access_token: str,
        refresh_token: str,
        is_revoke: bool,
    ) -> TokenEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_tokens_by_refresh_token(
        self, session: AsyncSession, refresh_token: str
    ) -> TokenEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_tokens_by_access_token(
        self, session: AsyncSession, access_token: str
    ) -> TokenEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update_tokens(
        self, session: AsyncSession, tokens: TokenEntity, refresh_token: str
    ) -> TokenEntity:
        raise NotImplementedError

    @abstractmethod
    async def update_revoke(
        self, session: AsyncSession, refresh_token: str, is_revoke: bool
    ) -> None:
        raise NotImplementedError


class TokenRepository(ITokenRepository):
    async def save_tokens(
        self,
        session: AsyncSession,
        access_token: str,
        refresh_token: str,
        is_revoke: bool,
    ) -> TokenEntity:
        new_tokens = Token(
            access_token=access_token,
            refresh_token=refresh_token,
            is_revoke=is_revoke,
        )

        async with UnitOfWork(session) as uow:
            await uow.add(new_tokens)

        return TokenEntity(
            access_token=new_tokens.access_token,
            refresh_token=new_tokens.refresh_token,
            is_revoke=is_revoke,
        )

    async def get_tokens_by_refresh_token(
        self, session: AsyncSession, refresh_token: str
    ) -> TokenEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Token).where(Token.refresh_token == refresh_token)
            tokens = await uow.execute_query(query)
            tokens_scalar = tokens.scalar()
            if tokens_scalar is None:
                return

        return TokenEntity(
            access_token=tokens_scalar.access_token,
            refresh_token=tokens_scalar.refresh_token,
            is_revoke=tokens_scalar.is_revoke,
        )

    async def get_tokens_by_access_token(
        self, session: AsyncSession, access_token: str
    ) -> TokenEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Token).where(Token.access_token == access_token)
            tokens = await uow.execute_query(query)
            tokens_scalar = tokens.scalar()
            if tokens_scalar is None:
                return

        return TokenEntity(
            access_token=tokens_scalar.access_token,
            refresh_token=tokens_scalar.refresh_token,
            is_revoke=tokens_scalar.is_revoke,
        )

    async def update_tokens(
        self, session: AsyncSession, tokens: TokenEntity, refresh_token: str
    ) -> TokenEntity:
        async with UnitOfWork(session) as uow:
            query = (
                update(Token)
                .where(Token.refresh_token == tokens.refresh_token)
                .values(
                    access_token=tokens.access_token,
                    refresh_token=tokens.refresh_token,
                    is_revoke=tokens.is_revoke,
                )
            )
            await uow.execute_query(query)

        return tokens

    async def update_revoke(
        self, session: AsyncSession, refresh_token: str, is_revoke: bool
    ):
        async with UnitOfWork(session) as uow:
            query = (
                update(Token)
                .where(Token.refresh_token == refresh_token)
                .values(
                    is_revoke=is_revoke,
                )
            )
            await uow.execute_query(query)
