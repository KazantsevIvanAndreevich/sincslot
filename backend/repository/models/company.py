from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy import true
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from backend.entity.company import CompanyEntity, WorkSchedule
from backend.repository.models.base import Base
from backend.repository.models.mixins import CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from .service import Service


class Company(CreatedAtMixin, UpdatedAtMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
        nullable=True,
    )
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    filename: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(
        default=True,
        server_default=true(),
        nullable=False,
    )
    work_schedule = mapped_column(JSONB, nullable=True)
    booking_url: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    services: Mapped[list["Service"]] = relationship(back_populates="company")

    def to_company_entity(self) -> CompanyEntity:
        if self.work_schedule:
            result = []
            for ws in self.work_schedule:
                result.append(WorkSchedule.to_model(ws))

            self.work_schedule = result

        return CompanyEntity(
            id=self.id,
            name=self.name,
            email=self.email,
            password=self.password,
            phone=self.phone,
            work_schedule=self.work_schedule,
            filename=self.filename,
            updated_at=int(self.updated_at.timestamp()),
            created_at=int(self.created_at.timestamp()),
            description=self.description,
            address=self.address,
            booking_url=self.booking_url,
            is_active=self.is_active,
        )

    def __str__(self):
        return self.name
