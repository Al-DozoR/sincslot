from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from backend.entity.company import CompanyEntity
from backend.repository.models.company import Company
from backend.entity.service import ServiceEntity
from backend.repository.unit_of_work.unit_of_work import UnitOfWork
#
# name: str
# duration: int
# price: int
# company_id: int
# client_id: Optional[int] = field(default=None)
# updated_at: Optional[int] = field(default=None)
# created_at: Optional[int] = field(default=None)
# description: Optional[str] = field(default=None)
# id: Optional[int] = field(default=None)

class IServiceRepository(ABC):

    @abstractmethod
    async def save_service(self, service: ServiceEntity) -> int:
        raise NotImplemented

    @abstractmethod
    async def update_service(self) -> ServiceEntity | None:
        raise NotImplemented

    @abstractmethod
    async def get_services_by_company_id(self, company_id: int) -> list[ServiceEntity]:
        raise NotImplemented

    @abstractmethod
    async def get_services_by_company_booking_url(self, booking_url: str) -> list[ServiceEntity]:
        raise NotImplemented


class ServiceRepository(IServiceRepository):

    async def save_service(self, service: ServiceEntity) -> int:
        pass

    async def update_service(self) -> ServiceEntity | None:
        raise NotImplemented

    async def get_services_by_company_id(self, company_id: int) -> list[ServiceEntity]:
        raise NotImplemented

    async def get_services_by_company_booking_url(self, booking_url: str) -> list[ServiceEntity]:
        raise NotImplemented