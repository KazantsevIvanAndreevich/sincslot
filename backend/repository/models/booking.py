from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy import true, TIMESTAMP
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from backend.entity.booking import BookingEntity, BookingStatus
from backend.repository.models.base import Base
from backend.repository.models.service import Service
from backend.repository.models.client import Client
from backend.repository.models.mixins import CreatedAtMixin, UpdatedAtMixin


if TYPE_CHECKING:
    from .service import Service


class Booking(CreatedAtMixin, UpdatedAtMixin, Base):
    _booking_back_populates = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))
    service: Mapped["Service"] = relationship(back_populates="bookings")
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"))
    client: Mapped["Client"] = relationship(back_populates="bookings")
    time_start: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    time_end: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    status: Mapped[str] = mapped_column(
        default=BookingStatus.pending.value, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default=true(),
        nullable=False,
    )

    def to_booking_entity(self) -> BookingEntity:
        return BookingEntity(
            id=self.id,
            service_id=self.service_id,
            client_id=self.client_id,
            time_start=self.time_start,
            time_end=self.time_end,
            is_active=self.is_active,
            status=BookingStatus(self.status),
        )
