import secrets
import string
from abc import ABC, abstractmethod

from slugify import slugify

from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from backend.logger.logger import init_logger
from backend.use_case.file_use_case import IFileStorage
from backend.use_case.token_use_case import IToken
from backend.entity.company import CompanyEntity, WorkSchedule, DaysOfWeek
from backend.entity.token import TokenEntity
from backend.repository.company_repository import ICompanyRepository
from backend.core.config import Password, BookingUrl

logger = init_logger("company_use_case", "INFO")


class ICompanyUseCase(ABC):
    @abstractmethod
    async def save_company(
        self,
        session: AsyncSession,
        name: str,
        email: str,
        phone: str,
        address: str,
        password: str,
    ) -> TokenEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_company_by_id(
        self, session: AsyncSession, company_id: int
    ) -> CompanyEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_company_by_email(
        self, session: AsyncSession, email: str
    ) -> CompanyEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_company_by_phone(
        self, session: AsyncSession, phone: str
    ) -> CompanyEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_company_by_name(
        self, session: AsyncSession, name: str
    ) -> CompanyEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_company_by_booking_url_slug(
        self, session: AsyncSession, slug_booking_url: str
    ) -> CompanyEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def login(self, session: AsyncSession, company: CompanyEntity) -> TokenEntity:
        raise NotImplementedError

    async def update_company_by_id(
        self,
        session: AsyncSession,
        company_id: int,
        name: str,
        email: str,
        password: str,
        phone: str,
        slug_booking_url: str,
        description: str,
        address: str,
    ) -> CompanyEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update_work_schedule(
        self, session: AsyncSession, company_id: int, work_schedule: dict
    ) -> list[WorkSchedule] | None:
        raise NotImplementedError

    @abstractmethod
    async def recover_company_by_email(
        self, session: AsyncSession, email: str
    ) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get_work_schedule_by_company_id(
        self, session: AsyncSession, company_id
    ) -> list | None:
        raise NotImplementedError

    @abstractmethod
    async def deactivate_company(self, session: AsyncSession, company_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_company_booking_schedule(
        self,
        session: AsyncSession,
        company_id: int,
        sort_by: str,
        sort_order: str,
    ):
        raise NotImplementedError

    @abstractmethod
    async def list_companies(
        self,
        session: AsyncSession,
        limit: int | None,
        offset: int | None,
    ) -> list[CompanyEntity] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_company_by_slug(
        self, session: AsyncSession, slug: str
    ) -> CompanyEntity | None:
        raise NotImplementedError


class CompanyUseCase(ICompanyUseCase):
    def __init__(
        self,
        company_repository: ICompanyRepository,
        token: IToken,
        file_storage: IFileStorage,
        password_settings: Password,
        crypt_hasher: CryptContext,
        booking_url_settings: BookingUrl,
    ):
        self.company_repository = company_repository
        self.token = token
        self.file_storage = file_storage
        self.password_settings = password_settings
        self.crypt_hasher = crypt_hasher
        self.booking_url_settings = booking_url_settings

    async def save_company(
        self,
        session: AsyncSession,
        name: str,
        email: str,
        phone: str,
        address: str,
        password: str,
    ) -> TokenEntity | None:
        hash_password = await self.hash_password(password)

        booking_url: str = await self.generate_booking_url(name)

        company_id = await self.company_repository.save_company(
            session,
            name,
            email,
            phone,
            address,
            hash_password,
            booking_url,
        )

        access_token = await self.token.create_access_token(company_id=company_id)
        refresh_token = await self.token.create_refresh_token(company_id=company_id)

        tokens = await self.token.save_tokens(
            session, access_token, refresh_token, is_revoke=False
        )

        return tokens

    async def get_company_by_id(
        self, session: AsyncSession, company_id: int
    ) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_id(session, company_id)

    async def get_company_by_email(
        self, session: AsyncSession, email: str
    ) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_email(session, email)

    async def get_company_by_phone(
        self, session: AsyncSession, phone: str
    ) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_phone(session, phone)

    async def get_company_by_name(
        self, session: AsyncSession, name: str
    ) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_name(session, name)

    async def get_company_by_booking_url_slug(
        self, session: AsyncSession, slug_booking_url: str
    ) -> CompanyEntity | None:
        booking_url = await self.generate_booking_url(slug_booking_url)
        return await self.company_repository.get_company_by_booking_url(
            session, booking_url
        )

    async def login(self, session: AsyncSession, company: CompanyEntity) -> TokenEntity:
        if not company.is_active:
            raise Exception("Inactive company cannot log in")

        access_token = await self.token.create_access_token(company_id=company.id)
        refresh_token = await self.token.create_refresh_token(company_id=company.id)

        tokens = await self.token.save_tokens(
            session, access_token, refresh_token, is_revoke=False
        )

        return tokens

    async def update_company_by_id(
        self,
        session: AsyncSession,
        company_id: int,
        name: str,
        email: str,
        password: str,
        phone: str,
        slug_booking_url: str,
        description: str,
        address: str,
    ) -> CompanyEntity | None:
        data_to_update = {}

        # Поле передано и не равно null
        if name != "" and name is not None:
            data_to_update["name"] = name
        # Поле передано и не равно null
        if email != "" and email is not None:
            data_to_update["email"] = email
        # Поле передано и не равно null
        if password != "" and password is not None:
            data_to_update["password"] = await self.hash_password(password)
        # Поле передано и не равно null
        if phone != "" and phone is not None:
            data_to_update["phone"] = phone
        # Поле передано и не равно null
        if slug_booking_url != "" and slug_booking_url is not None:
            data_to_update["booking_url"] = await self.generate_booking_url(
                slug_booking_url
            )
        if description != "":
            data_to_update["description"] = description
        if address != "":
            data_to_update["address"] = address

        return await self.company_repository.update_company_by_id(
            session, company_id, data_to_update
        )

    async def update_work_schedule(
        self, session: AsyncSession, company_id: int, work_schedule: dict
    ) -> list[WorkSchedule] | None:
        data_to_update = []

        for ws in work_schedule["work_schedule"]:
            day_of_week: DaysOfWeek = ws.get("day_of_week")
            ws["day_of_week"] = day_of_week.value
            data_to_update.append(ws)

        work_schedule["work_schedule"] = data_to_update

        updated_data: (
            CompanyEntity | None
        ) = await self.company_repository.update_company_by_id(
            session=session, company_id=company_id, data_to_update=work_schedule
        )

        if updated_data is None:
            return

        return [w.to_dict() for w in updated_data.work_schedule]

    async def recover_company_by_email(
        self, session: AsyncSession, email: str, length: int = 10
    ) -> str | None:
        company_by_email = await self.company_repository.get_company_by_email(
            session, email
        )
        if company_by_email is None:
            logger.warning(
                "Failed to ger company by email %s to recover password", email
            )
            return

        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        random_pass = "".join(secrets.choice(chars) for _ in range(length))
        return random_pass

    async def hash_password(self, password: str) -> str:
        return self.crypt_hasher.hash(password + self.password_settings.salt)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.crypt_hasher.verify(
            plain_password + self.password_settings.salt, hashed_password
        )

    @staticmethod
    async def generate_company_slug(s: str) -> str:
        return slugify(s, separator="-")

    async def generate_booking_url(self, s: str) -> str:
        return self.booking_url_settings.base_url + "/" + slugify(s, separator="-")

    async def get_work_schedule_by_company_id(
        self, session: AsyncSession, company_id
    ) -> list | None:
        return await self.company_repository.get_work_schedule_by_company_id(
            session, company_id
        )

    async def deactivate_company(self, session: AsyncSession, company_id: int) -> None:
        await self.company_repository.deactivate_company(session, company_id)

    async def get_company_booking_schedule(
        self,
        session: AsyncSession,
        company_id: int,
        sort_by: str,
        sort_order: str,
    ):
        return await self.company_repository.get_company_booking_schedule(
            session, company_id, sort_by, sort_order
        )

    async def list_companies(
        self, session: AsyncSession, limit: int | None, offset: int | None
    ) -> list[CompanyEntity] | None:
        if limit is not None:
            if limit > 100:
                limit = 100

        if limit is None:
            limit = 100

        return await self.company_repository.list_companies(session, limit, offset)

    async def get_company_by_slug(
        self, session: AsyncSession, slug: str
    ) -> CompanyEntity | None:
        slug = await self.generate_company_slug(slug)
        return await self.company_repository.get_company_by_slug(session, slug)
