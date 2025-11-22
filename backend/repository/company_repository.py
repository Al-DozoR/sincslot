from abc import ABC, abstractmethod

from backend.entity.company import CompanyEntity
from backend.repository.models.company import Company
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete
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
    async def get_companies(self, session: AsyncSession) -> list[CompanyEntity]:
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
    ) -> int:

        new_company = Company(
            name=name,
            email=email,
            phone=phone,
            address=address,
            hash_password=password,
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

        return CompanyEntity(
            id=company_scalar.id,
            name=company_scalar.name,
            description=company_scalar.description,
            email=company_scalar.email,
            phone=company_scalar.phone,
            password=company_scalar.hash_password,
            address=company_scalar.address,
        )

    async def get_company_by_email(self, session: AsyncSession, email: str) -> CompanyEntity | None:

        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.email == email)
            company = await uow.execute_query(query)
            company_scalar = company.scalar()
            if company_scalar is None:
                return

        return CompanyEntity(
            id=company_scalar.id,
            name=company_scalar.name,
            description=company_scalar.description,
            email=company_scalar.email,
            phone=company_scalar.phone,
            password=company_scalar.hash_password,
            address=company_scalar.address)

    async def get_company_by_phone(self, session: AsyncSession, phone: str) -> CompanyEntity | None:
        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.phone == phone)
            company = await uow.execute_query(query)
            company_scalar = company.scalar()
            if company_scalar is None:
                return

        return CompanyEntity(
            id=company_scalar.id,
            name=company_scalar.name,
            description=company_scalar.description,
            email=company_scalar.email,
            phone=company_scalar.phone,
            password=company_scalar.hash_password,
            address=company_scalar.address)

    async def get_companies(self, session: AsyncSession) -> list[CompanyEntity]:
        async with UnitOfWork(session) as uow:
            query = select(Company)
            companies = await uow.execute_query(query)

        result = []

        for company in companies.scalars():
            result.append(
                CompanyEntity(
                    id=company.id,
                    name=company.name,
                    description=company.description,
                    email=company.email,
                    phone=company.phone,
                    password=company.hash_password,
                    address=company.address)
            )

        return result
