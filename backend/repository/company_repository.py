from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, Select, asc, desc
from sqlalchemy.orm import joinedload

from backend.entity.company import CompanyEntity
from backend.repository.models.booking import Booking
from backend.repository.models.client import Client
from backend.repository.models.company import Company
from backend.repository.models.service import Service
from backend.repository.unit_of_work.unit_of_work import UnitOfWork


class ICompanyRepository(ABC):
    @abstractmethod
    async def save_company(
        self,
        session: AsyncSession,
        name: str,
        email: str,
        phone: str,
        address: str,
        password: str,
        booking_url: str,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_company_by_id(
        self, session: AsyncSession, company_id: int
    ) -> CompanyEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_company_by_email(
        self, session: AsyncSession, email: str
    ) -> CompanyEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_company_by_phone(
        self, session: AsyncSession, phone: str
    ) -> CompanyEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_company_by_name(
        self, session: AsyncSession, name: str
    ) -> CompanyEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def get_company_by_booking_url(
        self, session: AsyncSession, booking_url: str
    ) -> CompanyEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update_company_by_id(
        self, session: AsyncSession, company_id: int, data_to_update: dict
    ) -> CompanyEntity | None:
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
        self, session: AsyncSession, limit: int, offset: int
    ) -> list[CompanyEntity] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_company_by_slug(
        self, session: AsyncSession, slug: str
    ) -> CompanyEntity | None:
        raise NotImplementedError


class CompanyRepository(ICompanyRepository):
    async def save_company(
        self,
        session: AsyncSession,
        name: str,
        email: str,
        phone: str,
        address: str,
        password: str,
        booking_url: str,
    ) -> int:
        new_company = Company(
            name=name,
            email=email,
            phone=phone,
            address=address,
            password=password,
            booking_url=booking_url,
            is_active=True,
        )

        async with UnitOfWork(session) as uow:
            await uow.add(new_company)

        return new_company.id

    async def get_company_by_id(
        self, session: AsyncSession, company_id: int
    ) -> CompanyEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.id == company_id)
            company = await uow.execute_query(query)
            company_scalar = company.scalar()
            if company_scalar is None:
                return

        return company_scalar.to_company_entity()

    async def get_company_by_email(
        self, session: AsyncSession, email: str
    ) -> CompanyEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.email == email)
            company = await uow.execute_query(query)
            company_scalar = company.scalar()
            if company_scalar is None:
                return

        return company_scalar.to_company_entity()

    async def get_company_by_phone(
        self, session: AsyncSession, phone: str
    ) -> CompanyEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.phone == phone)
            company = await uow.execute_query(query)
            company_scalar: Company | None = company.scalar()
            if company_scalar is None:
                return

        return company_scalar.to_company_entity()

    async def get_company_by_name(
        self, session: AsyncSession, name: str
    ) -> CompanyEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.name == name)
            company = await uow.execute_query(query)
            company_scalar: Company | None = company.scalar()
            if company_scalar is None:
                return

        return company_scalar.to_company_entity()

    async def get_company_by_booking_url(
        self, session: AsyncSession, booking_url: str
    ) -> CompanyEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.booking_url == booking_url)
            company = await uow.execute_query(query)
            company_scalar: Company | None = company.scalar()
            if company_scalar is None:
                return

        return company_scalar.to_company_entity()

    async def update_company_by_id(
        self, session: AsyncSession, company_id: int, data_to_update: dict
    ) -> CompanyEntity | None:
        async with UnitOfWork(session) as uow:
            query = (
                update(Company)
                .where(Company.id == company_id)
                .values(**data_to_update)
                .returning(Company)
            )
            company_updated = await uow.execute_query(query)
            company_updated_scalar: Company | None = company_updated.scalar()
            if company_updated_scalar is None:
                return

        return company_updated_scalar.to_company_entity()

    async def get_work_schedule_by_company_id(
        self, session: AsyncSession, company_id
    ) -> list | None:
        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.id == company_id)
            company = await uow.execute_query(query)
            company_scalar: Company | None = company.scalar()
            if company_scalar is None:
                return None

            return company_scalar.work_schedule if company_scalar.work_schedule else []

    async def deactivate_company(self, session: AsyncSession, company_id: int) -> None:
        async with UnitOfWork(session) as uow:
            query = (
                update(Company).where(Company.id == company_id).values(is_active=False)
            )
            await uow.execute_query(query)
            return None

    async def get_company_booking_schedule(
        self,
        session: AsyncSession,
        company_id: int,
        sort_by: str,
        sort_order: str,
    ):
        sort_by_mapping = {
            "clientName": Client.name,
            "serviceName": Service.name,
            "date": "booking_date",
            "time": "booking_time",
        }

        async with UnitOfWork(session) as uow:
            query = (
                Select(Booking)
                .join(Booking.service)
                .join(Booking.client)
                .options(joinedload(Booking.client), joinedload(Booking.service))
                .where(Service.company_id == company_id)
            )

            sort_by_column = sort_by_mapping.get(sort_by)

            if sort_by_column is not None and sort_by_column in (
                Service.name,
                Client.name,
            ):
                if sort_order == "asc":
                    query = query.order_by(asc(sort_by_column))
                elif sort_order == "desc":
                    query = query.order_by(desc(sort_by_column))
                else:
                    query = query.order_by(sort_by_column)

            bookings_by_client = await uow.execute_query(query)
            bookings_by_client_scalars: list[Booking] | None = (
                bookings_by_client.scalars()
            )
            if bookings_by_client_scalars is None:
                return

            result = []

            for booking in bookings_by_client_scalars:
                result.append(
                    {
                        "booking_id": booking.id,
                        "client_name": booking.client.name,
                        "phone": booking.client.phone,
                        "service": booking.service.name,
                        "status": booking.status,
                        "date": booking.time_start.date().strftime("%Y-%m-%d"),
                        "time": booking.time_start.time().strftime("%H:%M:%S"),
                    }
                )

            if sort_by_column is not None and sort_by_column == "booking_date":
                if sort_order == "desc":
                    result = sorted(result, key=lambda x: x["date"], reverse=True)
                else:
                    result = sorted(result, key=lambda x: x["date"])

            if sort_by_column is not None and sort_by_column == "booking_time":
                if sort_order == "desc":
                    result = sorted(result, key=lambda x: x["time"], reverse=True)
                else:
                    result = sorted(result, key=lambda x: x["time"])

            return result

    async def list_companies(
        self, session: AsyncSession, limit: int, offset: int
    ) -> list[CompanyEntity] | None:
        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.is_active == True)
            if limit is not None:
                query = query.limit(limit)
            if offset is not None:
                query = query.offset(offset)

            company = await uow.execute_query(query)
            companies_scalar = company.scalars()
            if companies_scalar is None:
                return

        result = []

        for company in companies_scalar:
            result.append(company.to_company_entity())

        return result

    async def get_company_by_slug(
        self, session: AsyncSession, slug: str
    ) -> CompanyEntity | None:
        pattern: str = f"%{slug}"

        async with UnitOfWork(session) as uow:
            query = (
                select(Company)
                .where(Company.is_active == True)
                .filter(Company.booking_url.like(pattern))
            )
            company = await uow.execute_query(query)
            company_scalar: Company | None = company.scalar()
            if company_scalar is None:
                return

        return company_scalar.to_company_entity()
