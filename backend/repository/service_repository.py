from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from backend.entity.company import CompanyEntity
from backend.repository.models.service import Service
from backend.entity.service import ServiceEntity
from backend.repository.models.service import Service
from backend.repository.unit_of_work.unit_of_work import UnitOfWork


class IServiceRepository(ABC):

    @abstractmethod
    async def save_service(self, session: AsyncSession, service: ServiceEntity) -> ServiceEntity:
        raise NotImplemented

    @abstractmethod
    async def get_service_by_id(self, session: AsyncSession, service_id: int):
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

    async def save_service(self, session: AsyncSession, service: ServiceEntity) -> ServiceEntity:

        new_service = Service(**service.to_dict())

        async with UnitOfWork(session) as uow:
            await uow.add(new_service)

        return new_service.to_service_entity()

    async def get_service_by_id(self, session: AsyncSession, service_id: int):
        async with UnitOfWork(session) as uow:
            query = select(Service).where(Service.id == service_id)
            service = await uow.execute_query(query)
            service_scalar = service.scalar()
            if service_scalar is None:
                return

        return service_scalar

    async def update_service(self) -> ServiceEntity | None:
        raise NotImplemented

    async def get_services_by_company_id(self, company_id: int) -> list[ServiceEntity]:
        raise NotImplemented

    async def get_services_by_company_booking_url(self, booking_url: str) -> list[ServiceEntity]:
        raise NotImplemented