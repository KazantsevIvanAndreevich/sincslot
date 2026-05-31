from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class BookingErrorResponse(BaseModel):
    error: str


class BookingGetById(BaseModel):
    booking_id: int


class BookingServiceInterval(BaseModel):
    start: str
    end: str


class BookingSchedule(BaseModel):
    month: int
    day: int
    day_of_week: int = Field(alias="dayOfWeek")
    is_work: bool = Field(alias="isWork")
    time_to_book: Optional[list[list[BookingServiceInterval]]] = Field(
        default=None, alias="timeToBook"
    )

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class BookingCalendarScheduleResponse(BaseModel):
    id: int
    name: str
    duration: int
    price: int
    description: Optional[str] = Field(default=None)
    # schedule: list[BookingSchedule]
