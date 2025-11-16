from abc import ABC, abstractmethod

from backend.entity.company import CompanyEntity
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repository.company_repository import ICompanyRepository


class ICompanyUseCase(ABC):

    @abstractmethod
    async def save_company(self, session: AsyncSession, company: CompanyEntity) -> int:
        raise NotImplemented

    @abstractmethod
    async def get_company_by_id(self, session: AsyncSession, company_id: int) -> CompanyEntity | None:
        raise NotImplemented


class CompanyUseCase(ICompanyUseCase):

    def __init__(self, company_repository: ICompanyRepository):
        self.company_repository = company_repository

    async def save_company(self, session: AsyncSession, company: CompanyEntity) -> int:
        return await self.company_repository.save_company(session, company)

    async def get_company_by_id(self, session: AsyncSession, company_id: int) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_id(session, company_id)