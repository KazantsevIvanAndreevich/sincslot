from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from backend.core.config import JWT
from backend.repository.token_repository import ITokenRepository
from backend.entity.token import TokenEntity, AccessTokenEntity, RefreshTokenEntity


class IToken(ABC):
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
    async def update_tokens(
        self, session: AsyncSession, refresh_token: str
    ) -> TokenEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def create_access_token_client(
        self, client_id: int, client_name: str, client_phone: str
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def create_refresh_token_client(
        self, client_id: int, client_name: str, client_phone: str
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    async def create_access_token(self, company_id: int) -> str:
        raise NotImplementedError

    @abstractmethod
    async def create_refresh_token(self, company_id: int) -> str:
        raise NotImplementedError

    @abstractmethod
    async def revoke_tokens(
        self, session: AsyncSession, refresh_token: str, is_revoke: bool
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def is_revoke(self, session: AsyncSession, access_token: str) -> bool | None:
        raise NotImplementedError

    @abstractmethod
    async def decode_token(self, token: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def is_expired(self, expired: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def is_refresh_token(self, payload: dict) -> bool:
        raise NotImplementedError


class Token(IToken):
    def __init__(
        self,
        token_repository: ITokenRepository,
        jwt_settings: JWT,
    ):
        self.token_repository: ITokenRepository = token_repository
        self.jwt_settings = jwt_settings

    async def save_tokens(
        self,
        session: AsyncSession,
        access_token: str,
        refresh_token: str,
        is_revoke: bool,
    ) -> TokenEntity:
        return await self.token_repository.save_tokens(
            session, access_token, refresh_token, is_revoke
        )

    async def update_tokens(
        self, session: AsyncSession, refresh_token: str
    ) -> TokenEntity | None:
        tokens = await self.token_repository.get_tokens_by_refresh_token(
            session, refresh_token
        )
        if tokens is None:
            return

        payload = await self.decode_token(tokens.refresh_token)

        new_access_token = await self.create_access_token_client(
            client_id=payload.get("client_id"),
            client_name=payload.get("client_name"),
            client_phone=payload.get("client_phone"),
        )
        new_refresh_token = await self.create_refresh_token_client(
            client_id=payload.get("client_id"),
            client_name=payload.get("client_name"),
            client_phone=payload.get("client_phone"),
        )

        return await self.token_repository.update_tokens(
            session,
            TokenEntity(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                is_revoke=False,
            ),
            refresh_token,
        )

    async def create_access_token(self, company_id: int) -> str:
        new_access_token = AccessTokenEntity(
            company_id=company_id,
            type=self.jwt_settings.token_type_access,
            exp=int(
                (
                    datetime.now(timezone.utc)
                    + timedelta(minutes=self.jwt_settings.access_token_expire_minutes)
                ).timestamp()
            ),
        )

        encoded_access_jwt = jwt.encode(
            new_access_token.to_dict(),
            self.jwt_settings.secret_key,
            algorithm=self.jwt_settings.algorithm,
        )

        return encoded_access_jwt

    async def create_access_token_client(
        self, client_id: int, client_name: str, client_phone: str
    ) -> str:
        new_access_token = {
            "client_id": client_id,
            "client_name": client_name,
            "client_phone": client_phone,
            "type": self.jwt_settings.token_type_access,
            "exp": int(
                (
                    datetime.now(timezone.utc)
                    + timedelta(minutes=self.jwt_settings.access_token_expire_minutes)
                ).timestamp()
            ),
        }

        encoded_access_jwt = jwt.encode(
            new_access_token,
            self.jwt_settings.secret_key,
            algorithm=self.jwt_settings.algorithm,
        )

        return encoded_access_jwt

    async def create_refresh_token(self, company_id: int) -> str:
        new_refresh_token = RefreshTokenEntity(
            company_id=company_id,
            type=self.jwt_settings.token_type_refresh,
            exp=int(
                (
                    datetime.now(timezone.utc)
                    + timedelta(minutes=self.jwt_settings.refresh_token_expire_minutes)
                ).timestamp()
            ),
        )

        encoded_refresh_jwt = jwt.encode(
            new_refresh_token.to_dict(),
            self.jwt_settings.secret_key,
            algorithm=self.jwt_settings.algorithm,
        )

        return encoded_refresh_jwt

    async def create_refresh_token_client(
        self, client_id: int, client_name: str, client_phone: str
    ) -> str:
        new_refresh_token = {
            "client_id": client_id,
            "client_name": client_name,
            "client_phone": client_phone,
            "type": self.jwt_settings.token_type_refresh,
            "exp": int(
                (
                    datetime.now(timezone.utc)
                    + timedelta(minutes=self.jwt_settings.refresh_token_expire_minutes)
                ).timestamp()
            ),
        }

        encoded_refresh_jwt = jwt.encode(
            new_refresh_token,
            self.jwt_settings.secret_key,
            algorithm=self.jwt_settings.algorithm,
        )

        return encoded_refresh_jwt

    async def revoke_tokens(
        self, session: AsyncSession, refresh_token: str, is_revoke: bool
    ) -> None:
        await self.token_repository.update_revoke(session, refresh_token, is_revoke)

    async def is_revoke(self, session: AsyncSession, access_token: str) -> bool | None:
        tokens = await self.token_repository.get_tokens_by_access_token(
            session, access_token
        )
        if tokens is None:
            return

        return tokens.is_revoke

    async def decode_token(self, token: str) -> dict:
        payload = jwt.decode(
            token,
            self.jwt_settings.secret_key,
            algorithms=[self.jwt_settings.algorithm],
        )
        return payload

    async def is_expired(self, expired: int) -> bool:
        now = int(datetime.now().timestamp())
        return expired > now

    async def is_refresh_token(self, type_token: str) -> bool:
        return type_token == self.jwt_settings.token_type_refresh
