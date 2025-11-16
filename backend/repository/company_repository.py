from abc import ABC, abstractmethod

from backend.entity.company import CompanyEntity
from backend.repository.models.company import Company
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete
from backend.repository.unit_of_work.unit_of_work import UnitOfWork


class ICompanyRepository(ABC):

    @abstractmethod
    async def save_company(self, session: AsyncSession, company: CompanyEntity) -> int:
        raise NotImplemented

    @abstractmethod
    async def get_company_by_id(self, session: AsyncSession, company_id: int) -> CompanyEntity:
        raise NotImplemented


class CompanyRepository(ICompanyRepository):

    async def save_company(self, session: AsyncSession, company: CompanyEntity) -> int:

        new_company = Company.to_company_model(company)

        async with UnitOfWork(session) as uow:
            await uow.add(new_company)

        return new_company.id

    async def get_company_by_id(self, session: AsyncSession, company_id: int) -> CompanyEntity | None:

        async with UnitOfWork(session) as uow:
            query = select(Company).where(Company.id == company_id)
            company = await uow.execute_query(query)
            if company is None:
                return

        company_scalar = company.scalar()

        return CompanyEntity(
            id=company_scalar.id,
            name=company_scalar.name,
            description=company_scalar.description,
            email=company_scalar.email,
            phone=company_scalar.phone,
            password=company_scalar.hash_password,
            address=company_scalar.address,

        )
