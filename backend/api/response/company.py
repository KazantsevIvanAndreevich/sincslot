from typing import Annotated, Union, Optional

import phonenumbers
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic.alias_generators import to_camel

from backend.entity.company import DaysOfWeek

E164NumberType = Annotated[
    Union[str, phonenumbers.PhoneNumber], PhoneNumberValidator(number_format="E164")
]


class CompanyTokensResponse(BaseModel):
    access_token: str = Field(alias="accessToken")
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class CompanyByIdResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    description: Optional[str]
    address: Optional[str]


class CompanyBySlugResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    description: Optional[str]
    address: Optional[str]


class CompanySuccessResponse(BaseModel):
    message: str


class CompanyErrorResponse(BaseModel):
    error: str


class CompanyRecoverPasswordResponse(BaseModel):
    pass


class CompanyWorkDayResponse(BaseModel):
    day_of_week: int = Field(default=DaysOfWeek.Monday)
    work_start: str = Field(examples=["9:00"], alias="workStart")
    work_end: str = Field(examples=["18:00"], alias="workEnd")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class CompanyWorkScheduleResponse(BaseModel):
    work_schedule: list[CompanyWorkDayResponse] = Field(alias="workSchedule")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class CompanyEntityResponse(BaseModel):
    id: int
    name: str
    email: str
    password: Optional[str] = None
    phone: str
    booking_url: str = Field(alias="bookingUrl")
    work_schedule: Optional[list[CompanyWorkScheduleResponse]] = Field(
        default=None, alias="workSchedule"
    )
    filename: Optional[str] = None
    updated_at: Optional[int] = Field(default=None, alias="updatedAt")
    created_at: Optional[int] = Field(default=None, alias="createdAt")
    description: Optional[str] = None
    address: Optional[str] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class ListCompanyElemResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    description: Optional[str] = None
    address: Optional[str] = None
    slug: str


class ListCompanyEntityResponse(BaseModel):
    companies: list[ListCompanyElemResponse]


class CompanySettingsResponse(BaseModel):
    name: str
    address: Optional[str | None] = None
    email: EmailStr
    phone: E164NumberType
    description: Optional[str | None] = None
    slug_booking_url: str = Field(
        examples=["company name slug"], alias="slugBookingUrl"
    )

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class CompanyBookingStatusResponse(BaseModel):
    status: str


class CompanyBookingResponse(BaseModel):
    booking_id: int = Field(alias="bookingID")
    client_name: str = Field(alias="clientName")
    phone: str
    service: str
    status: str
    date: str = Field(examples=["2025-12-14"])
    time: str = Field(examples=["14:04:08"])

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class CompanyBookingScheduleResponse(BaseModel):
    bookings: list[CompanyBookingResponse]
