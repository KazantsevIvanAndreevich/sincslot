import re
from datetime import datetime
from typing import Annotated, Union, Optional, Self

import phonenumbers
from pydantic_extra_types.phone_numbers import PhoneNumberValidator
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict,
    field_validator,
    model_validator,
)
from pydantic.alias_generators import to_camel

from backend.entity.company import DaysOfWeek
from backend.entity.booking import BookingStatus

E164NumberType = Annotated[
    Union[str, phonenumbers.PhoneNumber], PhoneNumberValidator(number_format="E164")
]


class CompanyCreateRequest(BaseModel):
    name: str = Field(examples=["Apple"])
    address: Optional[str] = None
    email: EmailStr = Field(examples=["SteveJobs123@example.com"])
    phone: E164NumberType = Field(examples=["+79126329303"])
    password: str = Field(examples=["Pass123!"])
    repeat_password: str = Field(examples=["Pass123!"], alias="repeatPassword")

    @classmethod
    @field_validator("password")
    def validate_password_complexity(cls, password):
        if not re.search(r"[A-Z]", password):
            raise ValueError(
                "Пароль должен содержать хотя бы одну заглавную букву (A–Z)"
            )
        if not re.search(r"[a-z]", password):
            raise ValueError(
                "Пароль должен содержать хотя бы одну строчную букву (a–z)"
            )
        if not re.search(r"\d", password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру (0–9)")
        if not re.search(r"[!@#$%^&*()_+\-=]", password):
            raise ValueError(
                "Пароль должен содержать хотя бы один спецсимвол: !@#$%^&*()_+-="
            )

        return password


class CompanyLoginRequest(BaseModel):
    email: EmailStr
    password: str


class CompanyRecoverPasswordRequest(BaseModel):
    email: str


class CompanyWorkDay(BaseModel):
    day_of_week: DaysOfWeek = Field(examples=[DaysOfWeek.Monday], alias="dayOfWeek")
    work_start: str = Field(examples=["9:00"], alias="workStart")
    work_end: str = Field(examples=["18:00"], alias="workEnd")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

    @classmethod
    @field_validator("work_start", "work_end")
    def validate_time_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%H:%M")
        except:
            raise ValueError(
                "Время должно быть в формате HH:MM (например, 9:00 или 18:30)"
            )
        return value

    @model_validator(mode="after")
    def validate_work_hours(self) -> Self:
        start_hours, start_minutes = map(int, self.work_start.split(":"))
        end_hours, end_minutes = map(int, self.work_end.split(":"))

        if start_hours * 60 + start_minutes >= end_hours * 60 + end_minutes:
            raise ValueError("work_start должно быть раньше work_end")
        return self


class CompanyWorkScheduleRequest(BaseModel):
    work_schedule: list[CompanyWorkDay] = Field(alias="workSchedule")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class CompanyUpdateSettingsRequest(BaseModel):
    name: Optional[str] = Field(default="", examples=["Tesla"])
    address: Optional[str] = Field(default="", examples=["Baker Street 221"])
    email: Optional[EmailStr] = Field(default="", examples=["ElonMask@example.ru"])
    phone: Optional[E164NumberType] = Field(default="", examples=["+79125483496"])
    current_password: Optional[str] = Field(
        default="", examples=["currentPass123"], alias="currentPassword"
    )
    new_password: Optional[str] = Field(
        default="", examples=["newPass123!"], alias="newPassword"
    )
    new_repeat_password: Optional[str] = Field(
        default="", examples=["user@example.ru"], alias="newRepeatPassword"
    )
    slug_booking_url: Optional[str] = Field(
        default="", examples=["company name slug"], alias="slugBookingUrl"
    )
    description: Optional[str] = Field(default="", examples=["company description"])

    @model_validator(mode="after")
    def validate_password_complexity(self) -> Self:
        # Не передали поле
        if self.new_password == "":
            return self

        # Передали null
        if self.new_password is None:
            raise ValueError(
                "Пароль должен содержать хотя бы одну заглавную букву (A–Z)"
            )

        if not re.search(r"[A-Z]", self.new_password):
            raise ValueError(
                "Пароль должен содержать хотя бы одну заглавную букву (A–Z)"
            )
        if not re.search(r"[a-z]", self.new_password):
            raise ValueError(
                "Пароль должен содержать хотя бы одну строчную букву (a–z)"
            )
        if not re.search(r"\d", self.new_password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру (0–9)")
        if not re.search(r"[!@#$%^&*()_+\-=]", self.new_password):
            raise ValueError(
                "Пароль должен содержать хотя бы один спецсимвол: !@#$%^&*()_+-="
            )

        return self

    @model_validator(mode="after")
    def is_email(self):
        if self.email is None:
            raise ValueError("email cannot be null")
        return self

    @model_validator(mode="after")
    def is_name(self):
        if self.name is None:
            raise ValueError("name cannot be null")
        return self

    @model_validator(mode="after")
    def is_phone(self):
        if self.phone is None:
            raise ValueError("phone cannot be null")
        return self

    @model_validator(mode="after")
    def is_slug_booking_url(self):
        # передали null. Поле не может быть null
        if self.slug_booking_url is None:
            raise ValueError("slug booking url cannot be null")

        # поле slug_booking_url не передали
        if self.slug_booking_url == "":
            return self

        if not re.fullmatch(r"^[a-zA-Z-0-9-]+$", self.slug_booking_url):
            raise ValueError(
                "slug_booking_url must contain only Latin letters, hyphens (-) and numbers"
            )

        return self

    @model_validator(mode="after")
    def check_password_match(self) -> Self:
        # Не передали поля
        if self.new_password == "" and self.new_repeat_password == "":
            return self

        # Не передали поле new_password, но передали new_repeat_password
        if self.new_password == "" and self.new_repeat_password != "":
            raise ValueError("new_password and new_repeat_password do not match")

        # Не передали поле new_repeat_password, но передали new_password
        if self.new_password != "" and self.new_repeat_password == "":
            raise ValueError("new_password and new_repeat_password do not match")

        # Передали null
        if self.new_password is None or self.new_repeat_password is None:
            raise ValueError("new_password and new_repeat_password do not match")

        # Поля передали и они не null
        if self.new_password is not None and self.new_repeat_password is not None:
            # Текущий передали как null. Он не может быть null
            if self.current_password is None:
                raise ValueError("current_password is needed to update new password")

            # Текущий пароль не передали
            if self.current_password == "":
                raise ValueError("current_password is needed to update new password")

            if self.new_password != self.new_repeat_password:
                raise ValueError("new_password and new_repeat_password do not match")

        return self


class CompanyBookingScheduleOrder(BaseModel):
    client_name: str | None = Field(default=None)
    service_name: str | None = Field(default=None)
    date: str | None = Field(default=None)
    time: str | None = Field(default=None)


class CompanyBookingScheduleStatus(BaseModel):
    status: BookingStatus
