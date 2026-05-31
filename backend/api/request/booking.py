from typing import Self
from datetime import datetime
from pydantic import BaseModel, model_validator, Field


class BookingCreateRequest(BaseModel):
    start_booking: datetime = Field(
        examples=["2025-12-07T12:09:33.497Z"], alias="startBooking"
    )
    end_booking: datetime = Field(
        examples=["2025-12-07T12:09:33.497Z"], alias="endBooking"
    )

    @model_validator(mode="after")
    def validate_time_format(self) -> Self:
        if int(self.start_booking.timestamp()) >= int(self.end_booking.timestamp()):
            raise ValueError(
                "Дата начала не может быть больше, чем дата окончания услуги"
            )
        return self
