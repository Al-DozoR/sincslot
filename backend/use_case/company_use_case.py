from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


from backend.use_case.token import IToken
from backend.entity.company import CompanyEntity
from backend.repository.company_repository import ICompanyRepository


class ICompanyUseCase(ABC):

    @abstractmethod
    async def save_company(self, session: AsyncSession, company: CompanyEntity) -> dict:
        raise NotImplemented

    @abstractmethod
    async def get_company_by_id(self, session: AsyncSession, company_id: int) -> CompanyEntity | None:
        raise NotImplemented


class CompanyUseCase(ICompanyUseCase):


    def __init__(self, company_repository: ICompanyRepository, token: IToken):
        self.company_repository = company_repository
        self.token = token

    async def save_company(self, session: AsyncSession, company: CompanyEntity) -> dict:

        hash_password = self.token.hash_password(company.password)
        company.password = hash_password

        company_id = await self.company_repository.save_company(session, company)

        access_token = self.token.create_access_token(to_encode={"company_id": company_id})
        refresh_token = self.token.create_refresh_token(to_encode={"company_id": company_id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def get_company_by_id(self, session: AsyncSession, company_id: int) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_id(session, company_id)


