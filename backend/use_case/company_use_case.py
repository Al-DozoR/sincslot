from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from backend.use_case.token_use_case import IToken
from backend.entity.company import CompanyEntity
from backend.entity.token import TokenEntity
from backend.repository.company_repository import ICompanyRepository


class ICompanyUseCase(ABC):

    @abstractmethod
    async def save_company(
            self,
            session: AsyncSession,
            name: str,
            email: str,
            phone: str,
            address: str,
            password: str
    ) -> TokenEntity:
        raise NotImplemented

    @abstractmethod
    async def get_company_by_id(self, session: AsyncSession, company_id: int) -> CompanyEntity | None:
        raise NotImplemented

    @abstractmethod
    async def get_company_by_email(self, session: AsyncSession, email: str) -> CompanyEntity | None:
        raise NotImplemented

    @abstractmethod
    async def login(self, session: AsyncSession, email: str, input_password: str) -> dict:
        raise NotImplemented


class CompanyUseCase(ICompanyUseCase):

    def __init__(self, company_repository: ICompanyRepository, token: IToken):
        self.company_repository = company_repository
        self.token = token

    async def save_company(
            self,
            session: AsyncSession,
            name: str,
            email: str,
            phone: str,
            address: str,
            password: str
    ) -> TokenEntity:

        hash_password = self.token.hash_password(password)

        company_id = await self.company_repository.save_company(
            session,
            name,
            email,
            phone,
            address,
            hash_password,
        )

        access_token = self.token.create_access_token(to_encode={
            "company_id": company_id,
            "name": name,
            "email": email
        })
        refresh_token = self.token.create_refresh_token(to_encode={"email": email})

        tokens = await self.token.save_tokens(session, access_token, refresh_token)

        return tokens

    async def get_company_by_id(self, session: AsyncSession, company_id: int) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_id(session, company_id)

    async def get_company_by_email(self, session: AsyncSession, email: str) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_email(session, email)

    async def login(self, session: AsyncSession, email: str, input_password: str) -> dict | None:
        company = await self.company_repository.get_company_by_email(session, email)
        if company is None:
            return

        if not self.token.verify_password(input_password, company.password):
            return

        access_token = self.token.create_access_token(to_encode={"company_id": company.id})
        refresh_token = self.token.create_refresh_token(to_encode={"company_id": company.id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
