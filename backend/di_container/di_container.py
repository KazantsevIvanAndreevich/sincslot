from rodi import Container
from passlib.context import CryptContext

from backend.repository.booking_repository import IBookingRepository, BookingRepository
from backend.repository.client_repository import IClientRepository, ClientRepository
from backend.repository.company_repository import ICompanyRepository, CompanyRepository
from backend.repository.token_repository import ITokenRepository, TokenRepository
from backend.repository.service_repository import IServiceRepository, ServiceRepository
from backend.use_case.company_use_case import ICompanyUseCase, CompanyUseCase
from backend.use_case.token_use_case import IToken, Token
from backend.use_case.file_use_case import IFileStorage, FileCompanyLogoStorage
from backend.use_case.service_use_case import IServiceUseCase, ServiceUseCase
from backend.use_case.booking_use_case import IBookingUseCase, BookingUseCase
from backend.use_case.client_use_case import IClientUseCase, ClientUseCase
from backend.core.config import settings


class DIContainer:
    container = Container()

    container.add_transient(ICompanyRepository, CompanyRepository)
    container.add_transient(ITokenRepository, TokenRepository)
    container.add_transient(IServiceRepository, ServiceRepository)
    container.add_transient(IBookingRepository, BookingRepository)
    container.add_transient(ICompanyUseCase, CompanyUseCase)
    container.add_transient(IClientRepository, ClientRepository)
    container.add_transient(IToken, Token)
    container.add_transient(IFileStorage, FileCompanyLogoStorage)
    container.add_transient(IServiceUseCase, ServiceUseCase)
    container.add_transient(IBookingUseCase, BookingUseCase)
    container.add_transient(IClientUseCase, ClientUseCase)
    container.add_instance(CryptContext(schemes=["bcrypt"], deprecated="auto"))
    container.add_instance(settings.jwt)
    container.add_instance(settings.password)
    container.add_instance(settings.file_company_logo_settings)
    container.add_instance(settings.booking_url)
    container.add_instance(settings.calendar_schedule)

    def get_company_use_cases(self) -> ICompanyUseCase:
        return self.container.resolve(ICompanyUseCase)

    def get_token_use_case(self) -> IToken:
        return self.container.resolve(IToken)

    def get_file_storage_use_case(self) -> IFileStorage:
        return self.container.resolve(IFileStorage)

    def get_service_use_case(self) -> IServiceUseCase:
        return self.container.resolve(IServiceUseCase)

    def get_booking_use_case(self) -> IBookingUseCase:
        return self.container.resolve(IBookingUseCase)

    def get_client_use_case(self) -> IClientUseCase:
        return self.container.resolve(IClientUseCase)


di_container = DIContainer()
