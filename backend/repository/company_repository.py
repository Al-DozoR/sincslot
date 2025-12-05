from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from backend.entity.company import CompanyEntity
from backend.repository.models.company import Company
from backend.repository.unit_of_work.unit_of_work import UnitOfWork


class ICompanyRepository(ABC):

    @abstractmethod
    async def save_company(
            self,
            session: AsyncSession,
            name: str,
            email: str,
            phone: str,
            address: str,
            password: str,
            booking_url: str,
    ) -> int:
        raise NotImplemented

    @abstractmethod
    async def get_company_by_id(self, session: AsyncSession, company_id: int) -> CompanyEntity:
        raise NotImplemented

    @abstractmethod
    async def get_company_by_email(self, session: AsyncSession, email: str) -> CompanyEntity:
        raise NotImplemented

    @abstractmethod
    async def get_company_by_phone(self, session: AsyncSession, phone: str) -> CompanyEntity:
        raise NotImplemented

    @abstractmethod
    async def get_company_by_name(self, session: AsyncSession, name: str) -> CompanyEntity | None:
        raise NotImplemented

    @abstractmethod
    async def get_company_by_booking_url(self, session: AsyncSession, booking_url: str) -> CompanyEntity | None:
        raise NotImplemented

    @abstractmethod
    async def update_company_by_id(
            self,
            session: AsyncSession,
            company_id: int,
            data_to_update: dict
    ) -> CompanyEntity | None:
        raise NotImplemented

    @abstractmethod
    async def get_work_schedule_by_company_id(self, session: AsyncSession, company_id) -> list | None:
        raise NotImplemented

    @abstractmethod
    async def deactivate_company(self, session: AsyncSession, company_id: int) -> None:
        raise NotImplemented

class CompanyRepository(ICompanyRepository):

    async def save_company(
            self,
            session: AsyncSession,
            name: str,
            email: str,
            phone: str,
            address: str,
            password: str,
            booking_url: str,
    ) -> int:

        new_company = Company(
            name=name,
            email=email,
            phone=phone,
            address=address,
            password=password,
            booking_url=booking_url,
            is_active=True,
        )

        async with UnitOfWork(session) as uow:
            await uow.add(new_company)

        return new_company.id

    async def get_company_by_id(self, session: AsyncSession, company_id: int) -> CompanyEntity | None:

        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.id == company_id)
            company = await uow.execute_query(query)
            company_scalar = company.scalar()
            if company_scalar is None:
                return

        return company_scalar.to_company_entity()

    async def get_company_by_email(self, session: AsyncSession, email: str) -> CompanyEntity | None:

        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.email == email)
            company = await uow.execute_query(query)
            company_scalar = company.scalar()
            if company_scalar is None:
                return

        return company_scalar.to_company_entity()

    async def get_company_by_phone(self, session: AsyncSession, phone: str) -> CompanyEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.phone == phone)
            company = await uow.execute_query(query)
            company_scalar: Company | None = company.scalar()
            if company_scalar is None:
                return

        return company_scalar.to_company_entity()

    async def get_company_by_name(self, session: AsyncSession, name: str) -> CompanyEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.name == name)
            company = await uow.execute_query(query)
            company_scalar: Company | None = company.scalar()
            if company_scalar is None:
                return

        return company_scalar.to_company_entity()

    async def get_company_by_booking_url(self, session: AsyncSession, booking_url: str) -> CompanyEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.booking_url == booking_url)
            company = await uow.execute_query(query)
            company_scalar: Company | None = company.scalar()
            if company_scalar is None:
                return

        return company_scalar.to_company_entity()

    async def update_company_by_id(
            self,
            session: AsyncSession,
            company_id: int,
            data_to_update: dict
    ) -> CompanyEntity | None:
        async with UnitOfWork(session) as uow:
            query = update(Company).where(Company.id == company_id).values(
                **data_to_update
            ).returning(Company)
            company_updated = await uow.execute_query(query)
            company_updated_scalar: Company | None = company_updated.scalar()
            if company_updated_scalar is None:
                return

        return company_updated_scalar.to_company_entity()

    async def get_work_schedule_by_company_id(self, session: AsyncSession, company_id) -> list | None:
        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.id == company_id)
            company = await uow.execute_query(query)
            company_scalar: Company | None = company.scalar()
            if company_scalar is None:
                return None

            return company_scalar.work_schedule if company_scalar.work_schedule else []

    async def deactivate_company(self, session: AsyncSession, company_id: int) -> None:
        async with UnitOfWork(session) as uow:
            query = update(Company).where(Company.id == company_id).values(is_active=False)
            await uow.execute_query(query)
            return None