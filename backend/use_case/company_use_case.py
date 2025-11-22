import secrets
import string

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
    async def get_company_by_phone(self, session: AsyncSession, phone: str) -> CompanyEntity | None:
        raise NotImplemented

    @abstractmethod
    async def login(self, session: AsyncSession, email: str, input_password: str) -> dict | None:
        raise NotImplemented

    @abstractmethod
    async def recover_company_by_email(self, session: AsyncSession, email: str) -> str | None:
        raise NotImplemented

    @abstractmethod
    async def get_companies(self, session: AsyncSession) -> list[CompanyEntity]:
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

        hash_password = await self.token.hash_password(password)

        company_id = await self.company_repository.save_company(
            session,
            name,
            email,
            phone,
            address,
            hash_password,
        )

        access_token = await self.token.create_access_token(company_id=company_id)
        refresh_token = await self.token.create_refresh_token(company_id=company_id)

        tokens = await self.token.save_tokens(session, access_token, refresh_token, is_revoke=True)

        return tokens

    async def get_company_by_id(self, session: AsyncSession, company_id: int) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_id(session, company_id)

    async def get_company_by_email(self, session: AsyncSession, email: str) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_email(session, email)

    async def get_company_by_phone(self, session: AsyncSession, phone: str) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_phone(session, phone)

    async def login(self, session: AsyncSession, email_or_phone: str, input_password: str) -> dict | None:
        company_by_email = await self.company_repository.get_company_by_email(session, email_or_phone)

        company_by_phone = await self.company_repository.get_company_by_phone(session, email_or_phone)

        company: CompanyEntity | None = company_by_email if company_by_email else company_by_phone
        if company is None:
            return

        if not await self.token.verify_password(input_password, company.password):
            return

        access_token = await self.token.create_access_token(company_id=company.id)
        refresh_token = await self.token.create_refresh_token(company_id=company.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def get_companies(self, session: AsyncSession) -> list[CompanyEntity]:
        return await self.company_repository.get_companies(session)

    async def recover_company_by_email(self, session: AsyncSession, email: str, length: int = 10) -> str | None:
        company_by_email = await self.company_repository.get_company_by_email(session, email)
        if company_by_email is None:
            return

        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        random_pass = ''.join(secrets.choice(chars) for _ in range(length))
        return random_pass

