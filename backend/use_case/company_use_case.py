import secrets
import string
from typing import BinaryIO
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from backend.logger.logger import init_logger
from backend.use_case.file_use_case import IFileStorage
from backend.use_case.token_use_case import IToken
from backend.entity.company import CompanyEntity
from backend.entity.token import TokenEntity
from backend.repository.company_repository import ICompanyRepository
from backend.core.config import Password

logger = init_logger('company_use_case', 'INFO')


class ICompanyUseCase(ABC):

    @abstractmethod
    async def save_company(
            self,
            session: AsyncSession,
            name: str,
            email: str,
            phone: str,
            address: str,
            password: str,
            filename: str,
            file: BinaryIO,
    ) -> TokenEntity | None:
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
    async def get_company_by_name(self, session: AsyncSession, name: str) -> CompanyEntity | None:
        raise NotImplemented

    @abstractmethod
    async def login(self, session: AsyncSession, company: CompanyEntity) -> TokenEntity:
        raise NotImplemented

    @abstractmethod
    async def recover_company_by_email(self, session: AsyncSession, email: str) -> str | None:
        raise NotImplemented

    @abstractmethod
    async def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError


class CompanyUseCase(ICompanyUseCase):

    def __init__(
            self,
            company_repository: ICompanyRepository,
            token: IToken,
            file_storage: IFileStorage,
            password_settings: Password,
            crypt_hasher: CryptContext,
    ):
        self.company_repository = company_repository
        self.token = token
        self.file_storage = file_storage
        self.password_settings = password_settings
        self.crypt_hasher = crypt_hasher

    async def save_company(
            self,
            session: AsyncSession,
            name: str,
            email: str,
            phone: str,
            address: str,
            password: str,
            filename: str,
            file: BinaryIO,
    ) -> TokenEntity | None:

        password_salt = password + self.password_settings.salt

        hash_password = await self.hash_password(password_salt)

        filename = f"{name}_{filename}"

        try:
            await self.file_storage.save_file(filename, file)

            company_id = await self.company_repository.save_company(
                session,
                name,
                email,
                phone,
                address,
                hash_password,
                filename,
            )
        except Exception as ex:
            logger.error("Failed to create company %s Error: %s", name, str(ex), exc_info=True)
            await self.file_storage.remove_file(filename)
        else:

            access_token = await self.token.create_access_token(company_id=company_id)
            refresh_token = await self.token.create_refresh_token(company_id=company_id)

            tokens = await self.token.save_tokens(session, access_token, refresh_token, is_revoke=False)

            return tokens

    async def get_company_by_id(self, session: AsyncSession, company_id: int) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_id(session, company_id)

    async def get_company_by_email(self, session: AsyncSession, email: str) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_email(session, email)

    async def get_company_by_phone(self, session: AsyncSession, phone: str) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_phone(session, phone)

    async def get_company_by_name(self, session: AsyncSession, name: str) -> CompanyEntity | None:
        return await self.company_repository.get_company_by_name(session, name)

    async def login(self, session: AsyncSession, company: CompanyEntity) -> TokenEntity:

        access_token = await self.token.create_access_token(company_id=company.id)
        refresh_token = await self.token.create_refresh_token(company_id=company.id)

        tokens = await self.token.save_tokens(session, access_token, refresh_token, is_revoke=False)

        return tokens

    async def recover_company_by_email(self, session: AsyncSession, email: str, length: int = 10) -> str | None:
        company_by_email = await self.company_repository.get_company_by_email(session, email)
        if company_by_email is None:
            logger.warning("Failed to ger company by email %s to recover password", email)
            return

        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        random_pass = ''.join(secrets.choice(chars) for _ in range(length))
        return random_pass

    async def hash_password(self, password: str) -> str:
        return self.crypt_hasher.hash(password)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.crypt_hasher.verify(plain_password + self.password_settings.salt, hashed_password)
