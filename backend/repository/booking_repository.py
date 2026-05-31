from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, Select, update
from sqlalchemy.orm import joinedload

from backend.entity.booking import BookingEntity, BookingStatus
from backend.repository.models.booking import Booking
from backend.repository.models.service import Service
from backend.repository.unit_of_work.unit_of_work import UnitOfWork


class IBookingRepository(ABC):
    @abstractmethod
    async def save_booking(
        self,
        session: AsyncSession,
        service_id: int,
        client_id: int,
        time_start: datetime,
        time_end: datetime,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_booking_by_client(
        self, session: AsyncSession, client_id
    ) -> list[dict] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_booking_by_service_id(
        self, session: AsyncSession, service_id
    ) -> list[BookingEntity] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_booking_by_service_id_and_client_id(
        self, session: AsyncSession, service_id: int, client_id: int
    ) -> BookingEntity | None:
        raise NotImplementedError

    @abstractmethod
    async def update_booking_by_id(
        self, session: AsyncSession, booking_id: int, data_to_update: dict
    ) -> BookingEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_booking_by_id(self, session: AsyncSession, booking_id: int):
        raise NotImplementedError


class BookingRepository(IBookingRepository):
    async def save_booking(
        self,
        session: AsyncSession,
        service_id: int,
        client_id: int,
        time_start: datetime,
        time_end: datetime,
    ) -> int:
        new_booking = Booking(
            service_id=service_id,
            client_id=client_id,
            time_start=time_start,
            time_end=time_end,
            is_active=True,
            status=BookingStatus.pending.value,
        )

        async with UnitOfWork(session) as uow:
            await uow.add(new_booking)

        return new_booking.id

    async def get_booking_by_client(
        self, session: AsyncSession, client_id
    ) -> list[dict] | None:
        async with UnitOfWork(session) as uow:
            query = (
                Select(Booking)
                .join(Booking.service)
                .options(joinedload(Booking.service).selectinload(Service.company))
                .where(Booking.client_id == client_id)
            )
            bookings_by_client = await uow.execute_query(query)
            bookings_by_client_scalars: list[Booking] | None = (
                bookings_by_client.scalars()
            )
            if bookings_by_client_scalars is None:
                return

        result: list[dict] = []

        for booking in bookings_by_client_scalars:
            result.append(
                {
                    "id": booking.id,
                    "client_id": booking.client_id,
                    "time_start": booking.time_start,
                    "time_end": booking.time_end,
                    "status": booking.status,
                    "service": {
                        "id": booking.service.id,
                        "name": booking.service.name,
                        "duration": booking.service.duration,
                        "price": booking.service.price,
                        "company": {
                            "company_id": booking.service.company.id,
                            "name": booking.service.company.name,
                            "booking_url": booking.service.company.booking_url,
                            "phone": booking.service.company.phone,
                            "email": booking.service.company.email,
                        },
                    },
                }
            )

        return result

    async def get_booking_by_service_id(
        self, session: AsyncSession, service_id
    ) -> list[BookingEntity] | None:
        async with UnitOfWork(session) as uow:
            query = Select(Booking).where(Booking.service_id == service_id)
            booking = await uow.execute_query(query)
            booking_scalars: list[Booking] | None = booking.scalars()
            if booking_scalars is None:
                return

        return [b.to_booking_entity() for b in booking_scalars]

    async def get_booking_by_service_id_and_client_id(
        self, session: AsyncSession, service_id: int, client_id: int
    ) -> BookingEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Booking).where(
                and_(Booking.client_id == client_id, Booking.service_id == service_id)
            )
            booking = await uow.execute_query(query)
            booking_scalars: Booking | None = booking.scalar()
            if booking_scalars is None:
                return

        return booking_scalars.to_booking_entity()

    async def update_booking_by_id(
        self, session: AsyncSession, booking_id: int, data_to_update: dict
    ) -> BookingEntity | None:
        async with UnitOfWork(session) as uow:
            query = (
                update(Booking)
                .where(Booking.id == booking_id)
                .values(**data_to_update)
                .returning(Booking)
            )
            booking_updated = await uow.execute_query(query)
            booking_updated_scalar: Booking | None = booking_updated.scalar()
            if booking_updated_scalar is None:
                return

        return booking_updated_scalar.to_booking_entity()

    async def get_booking_by_id(self, session: AsyncSession, booking_id: int):
        async with UnitOfWork(session) as uow:
            query = select(Booking).where(Booking.id == booking_id)
            booking = await uow.execute_query(query)
            booking_scalar = booking.scalar()
            if booking_scalar is None:
                return

        return booking_scalar.to_booking_entity()
