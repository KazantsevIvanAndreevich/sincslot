from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy import true
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy import CheckConstraint

from backend.entity.service import ServiceEntity
from backend.repository.models.base import Base
from backend.repository.models.mixins import CreatedAtMixin, UpdatedAtMixin


if TYPE_CHECKING:
    from .booking import Booking
    from .company import Company


class Service(CreatedAtMixin, UpdatedAtMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("price > 0", name="check_price_positive"),
        nullable=False,
    )
    duration: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("duration > 0", name="check_price_positive"),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(255),
        default="",
        server_default="",
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default=true(),
        nullable=False,
    )
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"), nullable=False)
    company: Mapped["Company"] = relationship(back_populates="services")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="service")

    def to_service_entity(self) -> ServiceEntity:
        return ServiceEntity(
            id=self.id,
            name=self.name,
            price=self.price,
            duration=self.duration,
            description=self.description,
            company_id=self.company_id,
            is_active=self.is_active,
            created_at=int(self.created_at.timestamp()),
            updated_at=int(self.updated_at.timestamp()),
        )
