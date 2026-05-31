from fastapi import APIRouter

from backend.core.config import settings
from backend.api.controllers.health import router_health

from backend.api.controllers.company.get_company_by_slug import (
    router as router_get_company_by_slug,
)
from backend.api.controllers.company.list_companies import (
    router as router_list_companies,
)
from backend.api.controllers.company.image import router as router_image
from backend.api.controllers.company.work_schedule import router as router_work_schedule
from backend.api.controllers.company.auth.login import router as router_login
from backend.api.controllers.company.auth.logout import router as router_logout
from backend.api.controllers.company.auth.recover_password import (
    router as router_recover_password,
)
from backend.api.controllers.company.auth.refresh_token import (
    router as router_refresh_token,
)
from backend.api.controllers.company.settings_company import (
    router as router_settings_company,
)

from backend.api.controllers.company.service.create_service import (
    router as router_create_service,
)
from backend.api.controllers.company.service.get_service_by_id import (
    router as router_get_service_by_id,
)
from backend.api.controllers.company.service.get_services_by_company_id import (
    router as router_get_services_by_company_id,
)
from backend.api.controllers.company.service.update_service_by_id import (
    router as router_update_service_by_id,
)
from backend.api.controllers.company.service.remove_service_by_id import (
    router as router_remove_service_by_id,
)
from backend.api.controllers.company.auth.register import (
    router as router_register_company,
)
from backend.api.controllers.company.deactivate_company import (
    router as router_deactivate_company,
)
from backend.api.controllers.company.service.get_services_by_company_alias import (
    router as router_get_services_by_company_alias,
)

from backend.api.controllers.booking.get_booking_by_id import (
    router as router_get_booking_by_id,
)
from backend.api.controllers.booking.create_booking import (
    router as router_create_booking,
)

from backend.api.controllers.company.booking_schedule.booking_schedule import (
    router as router_booking_schedule,
)
from backend.api.controllers.company.booking_schedule.booking_schedule_status import (
    router as router_booking_schedule_status,
)

from backend.api.controllers.client.auth.login import router_client_auth_login
from backend.api.controllers.client.auth.register import (
    router as router_register_client,
)
from backend.api.controllers.client.auth.refresh_token import (
    router as router_refresh_token_client,
)
from backend.api.controllers.client.get_client_bookings import (
    router as router_get_client_bookings,
)
from backend.api.controllers.client.deactivate_client_booking import (
    router as router_deactivate_client_booking,
)
from backend.api.controllers.client.auth.logout import router as router_logout_client


routes = APIRouter()

routes.include_router(router=router_health)

################### Company ###################

routes.include_router(
    router=router_image,
    prefix=settings.api_v1.prefix_company_logo_image,
    tags=[settings.tags.tag_company_logo_image],
)

routes.include_router(
    router=router_work_schedule,
    prefix=settings.api_v1.prefix_company_work_schedule,
    tags=[settings.tags.tag_company_work_schedule],
)

routes.include_router(
    router=router_settings_company,
    prefix=settings.api_v1.prefix_company_settings,
    tags=[settings.tags.tag_company_settings],
)

routes.include_router(
    router=router_login,
    prefix=settings.api_v1.prefix_company_auth,
    tags=[settings.tags.tag_company_auth],
)

routes.include_router(
    router=router_logout,
    prefix=settings.api_v1.prefix_company_auth,
    tags=[settings.tags.tag_company_auth],
)

routes.include_router(
    router=router_recover_password,
    prefix=settings.api_v1.prefix_company_auth,
    tags=[settings.tags.tag_company_auth],
)

routes.include_router(
    router=router_refresh_token,
    prefix=settings.api_v1.prefix_company_auth,
    tags=[settings.tags.tag_company_auth],
)

routes.include_router(
    router=router_register_company,
    prefix=settings.api_v1.prefix_company_auth,
    tags=[settings.tags.tag_company_auth],
)

routes.include_router(
    router=router_deactivate_company,
    prefix=settings.api_v1.prefix_company_settings,
    tags=[settings.tags.tag_company_settings],
)

routes.include_router(
    router=router_list_companies,
    prefix=settings.api_v1.prefix_list_companies,
    tags=[settings.tags.tag_company],
)

routes.include_router(
    router=router_get_company_by_slug,
    prefix=settings.api_v1.prefix_company_by_slug,
    tags=[settings.tags.tag_company],
)
################### Company Service ###################

routes.include_router(
    router=router_create_service,
    prefix=settings.api_v1.prefix_company_service,
    tags=[settings.tags.tag_company_service],
)

routes.include_router(
    router=router_get_service_by_id,
    prefix=settings.api_v1.prefix_company_service,
    tags=[settings.tags.tag_company_service],
)

routes.include_router(
    router=router_get_services_by_company_id,
    prefix=settings.api_v1.prefix_company_service,
    tags=[settings.tags.tag_company_service],
)

routes.include_router(
    router=router_update_service_by_id,
    prefix=settings.api_v1.prefix_company_service,
    tags=[settings.tags.tag_company_service],
)

routes.include_router(
    router=router_remove_service_by_id,
    prefix=settings.api_v1.prefix_company_service,
    tags=[settings.tags.tag_company_service],
)

routes.include_router(
    router=router_get_services_by_company_alias,
    prefix=settings.api_v1.prefix_company_service_public,
    tags=[settings.tags.tag_company_service_public],
)

################### Company booking schedule ###################

routes.include_router(
    router=router_booking_schedule,
    prefix=settings.api_v1.prefix_company_booking_schedule,
    tags=[settings.tags.tag_company_booking_schedule],
)

routes.include_router(
    router=router_booking_schedule_status,
    prefix=settings.api_v1.prefix_company_booking_schedule,
    tags=[settings.tags.tag_company_booking_schedule],
)

################### Booking ###################

routes.include_router(
    router=router_get_booking_by_id,
    prefix=settings.api_v1.prefix_booking,
    tags=[settings.tags.tag_booking],
)

routes.include_router(
    router=router_create_booking,
    prefix=settings.api_v1.prefix_booking,
    tags=[settings.tags.tag_booking],
)

routes.include_router(
    router=router_get_client_bookings,
    prefix=settings.api_v1.prefix_client_booking,
    tags=[settings.tags.tag_client_booking],
)

################### Client ###################

routes.include_router(
    router=router_client_auth_login,
    prefix=settings.api_v1.prefix_client_auth,
    tags=[settings.tags.tag_client_auth],
)

routes.include_router(
    router=router_refresh_token_client,
    prefix=settings.api_v1.prefix_client_auth,
    tags=[settings.tags.tag_client_auth],
)

routes.include_router(
    router=router_register_client,
    prefix=settings.api_v1.prefix_client_auth,
    tags=[settings.tags.tag_client_auth],
)

routes.include_router(
    router=router_deactivate_client_booking,
    prefix=settings.api_v1.prefix_client_booking,
    tags=[settings.tags.tag_client_booking],
)

routes.include_router(
    router=router_logout_client,
    prefix=settings.api_v1.prefix_client_auth,
    tags=[settings.tags.tag_client_auth],
)
