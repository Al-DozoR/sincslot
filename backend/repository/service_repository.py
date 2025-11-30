from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from backend.entity.service import ServiceEntity
from backend.repository.models.service import Service
from backend.repository.unit_of_work.unit_of_work import UnitOfWork


class IServiceRepository(ABC):

    @abstractmethod
    async def save_service(self, session: AsyncSession, service: ServiceEntity) -> ServiceEntity:
        raise NotImplemented

    @abstractmethod
    async def get_service_by_id(self, session: AsyncSession, service_id: int) -> ServiceEntity | None:
        raise NotImplemented

    @abstractmethod
    async def update_service(
            self,
            session: AsyncSession,
            service_id: int,
            data_to_update: dict) -> ServiceEntity | None:
        raise NotImplemented

    @abstractmethod
    async def get_services_by_company_id(self, session: AsyncSession, company_id: int) -> list[ServiceEntity] | None:
        raise NotImplemented


class ServiceRepository(IServiceRepository):

    async def save_service(self, session: AsyncSession, service: ServiceEntity) -> ServiceEntity:

        new_service = Service(**service.to_dict())

        async with UnitOfWork(session) as uow:
            await uow.add(new_service)

        return new_service.to_service_entity()

    async def get_service_by_id(self, session: AsyncSession, service_id: int) -> ServiceEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Service).where(Service.id == service_id)
            service = await uow.execute_query(query)
            service_scalar: Service | None = service.scalar()
            if service_scalar is None:
                return

        return service_scalar.to_service_entity()

    async def update_service(
            self,
            session: AsyncSession,
            service_id: int,
            data_to_update: dict) -> ServiceEntity | None:

        async with UnitOfWork(session) as uow:
            query = update(Service).where(Service.id == service_id).values(
                **data_to_update
            ).returning(Service)
            service_updated = await uow.execute_query(query)
            service_updated_scalar: Service | None = service_updated.scalar()
            if service_updated_scalar is None:
                return

        return service_updated_scalar.to_service_entity()

    async def get_services_by_company_id(self, session: AsyncSession, company_id: int) -> list[ServiceEntity] | None:
        async with UnitOfWork(session) as uow:
            query = select(Service).where(Service.company_id == company_id)
            services = await uow.execute_query(query)
            services_scalars: list[Service] | None = services.scalars()
            if services_scalars is None:
                return

        result: list[ServiceEntity] = []

        for service in services_scalars:
            result.append(service.to_service_entity())

        return result
