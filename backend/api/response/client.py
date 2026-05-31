from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class ClientSuccessResponse(BaseModel):
    message: str


class ClientErrorResponse(BaseModel):
    error: str


class ClientTokensResponse(BaseModel):
    access_token: str = Field(alias="accessToken")
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class CompanyInfo(BaseModel):
    company_id: int = Field(alias="companyID")
    name: str
    booking_url: str = Field(alias="bookingUrl")
    phone: str
    email: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class ServiceInfo(BaseModel):
    id: int
    name: str
    duration: int
    price: int
    company: CompanyInfo

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class Booking(BaseModel):
    id: int
    client_id: int = Field(alias="clientID")
    time_start: datetime = Field(alias="timeStart")
    time_end: datetime = Field(alias="timeEnd")
    status: str
    service: ServiceInfo

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class ClientBookingsResponse(BaseModel):
    client_bookings: list[Booking]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
