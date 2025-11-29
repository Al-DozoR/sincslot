import secrets
import string
from abc import ABC, abstractmethod
from slugify import slugify

from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from backend.logger.logger import init_logger
from backend.use_case.file_use_case import IFileStorage
from backend.use_case.token_use_case import IToken
from backend.entity.company import CompanyEntity, WorkSchedule, DaysOfWeek
from backend.entity.token import TokenEntity
from backend.repository.company_repository import ICompanyRepository
from backend.core.config import Password, BookingUrl

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

    async def update_company_by_id(
            self,
            session: AsyncSession,
            company_id: int,
            name: str | None = None,
            email: str | None = None,
            password: str | None = None,
            phone: str | None = None,
            slug_booking_url: str | None = None,
            description: str | None = None,
            address: str | None = None,
    ) -> CompanyEntity | None:
        raise NotImplemented

    @abstractmethod
    async def update_work_schedule(
            self,
            session: AsyncSession,
            company_id: int,
            work_schedule: dict
    ) -> list[WorkSchedule] | None:
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

    @abstractmethod
    async def generate_booking_url(self, s: str) -> str:
        raise NotImplemented


class CompanyUseCase(ICompanyUseCase):

    def __init__(
            self,
            company_repository: ICompanyRepository,
            token: IToken,
            file_storage: IFileStorage,
            password_settings: Password,
            crypt_hasher: CryptContext,
            booking_url_settings: BookingUrl,
    ):
        self.company_repository = company_repository
        self.token = token
        self.file_storage = file_storage
        self.password_settings = password_settings
        self.crypt_hasher = crypt_hasher
        self.booking_url_settings = booking_url_settings

    async def save_company(
            self,
            session: AsyncSession,
            name: str,
            email: str,
            phone: str,
            address: str,
            password: str,
    ) -> TokenEntity | None:

        password_salt = password + self.password_settings.salt

        hash_password = await self.hash_password(password_salt)

        booking_url: str = await self.generate_booking_url(name)

        company_id = await self.company_repository.save_company(
            session,
            name,
            email,
            phone,
            address,
            hash_password,
            booking_url,
        )

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

    async def update_company_by_id(
            self,
            session: AsyncSession,
            company_id: int,
            name: str | None = None,
            email: str | None = None,
            password: str | None = None,
            phone: str | None = None,
            slug_booking_url: str | None = None,
            description: str | None = None,
            address: str | None = None,
    ) -> CompanyEntity | None:

        data_to_update = {}

        if name is not None:
            data_to_update["name"] = name
        if email is not None:
            data_to_update["email"] = email
        if password is not None:
            data_to_update["password"] = await self.hash_password(password)
        if phone is not None:
            data_to_update["phone"] = phone
        if slug_booking_url is not None:
            data_to_update["booking_url"] = await self.generate_booking_url(slug_booking_url)
        if description is not None:
            data_to_update["booking_url"] = await self.generate_booking_url(description)
        if address is not None:
            data_to_update["address"] = address

        return await self.company_repository.update_company_by_id(session, company_id, data_to_update)

    async def update_work_schedule(
            self,
            session: AsyncSession,
            company_id: int,
            work_schedule: dict
    ) -> list[WorkSchedule] | None:

        data_to_update = []

        for ws in work_schedule["work_schedule"]:
            day_of_week: DaysOfWeek = ws.get("day_of_week")
            ws["day_of_week"] = day_of_week.value
            data_to_update.append(ws)

        work_schedule["work_schedule"] = data_to_update

        updated_data: CompanyEntity | None = await self.company_repository.update_company_by_id(
            session=session,
            company_id=company_id,
            data_to_update=work_schedule
        )

        if updated_data is None:
            return

        return [w.to_dict() for w in updated_data.work_schedule]

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

    async def generate_booking_url(self, s: str) -> str:
        return self.booking_url_settings.base_url + "/" + slugify(s, separator='-')
