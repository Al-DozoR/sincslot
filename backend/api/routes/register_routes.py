from fastapi import APIRouter
from backend.core.config import settings
from backend.api.conrollers.health import router_health
from backend.api.conrollers.company.get_company_by_id import router as router_get_company_by_id
from backend.api.conrollers.company.upload_image import router as router_upload_image
from backend.api.conrollers.company.download_image import router as router_download_image
from backend.api.conrollers.company.work_schedule import router as router_work_schedule
from backend.api.conrollers.company.auth.login import router as router_login
from backend.api.conrollers.company.auth.logout import router as router_logout
from backend.api.conrollers.company.auth.recover_password import router as router_recover_password
from backend.api.conrollers.company.auth.refresh_token import router as router_refresh_token
from backend.api.conrollers.company.auth.register import router as router_register
from backend.api.conrollers.company.settings_company import router as router_company_settings
from backend.api.conrollers.service.create_service import router as router_create_service


routes = APIRouter()

routes.include_router(router=router_health, prefix=settings.api_v1.prefix_company)
routes.include_router(router=router_get_company_by_id, prefix=settings.api_v1.prefix_company)
routes.include_router(router=router_upload_image, prefix=settings.api_v1.prefix_company)
routes.include_router(router=router_download_image, prefix=settings.api_v1.prefix_company)
routes.include_router(router=router_work_schedule, prefix=settings.api_v1.prefix_company)
routes.include_router(router=router_company_settings, prefix=settings.api_v1.prefix_company)

routes.include_router(router=router_login, prefix=settings.api_v1.prefix_company)
routes.include_router(router=router_logout, prefix=settings.api_v1.prefix_company)
routes.include_router(router=router_recover_password, prefix=settings.api_v1.prefix_company)
routes.include_router(router=router_refresh_token, prefix=settings.api_v1.prefix_company)
routes.include_router(router=router_register, prefix=settings.api_v1.prefix_company)

routes.include_router(router=router_create_service, prefix=settings.api_v1.prefix_service)
