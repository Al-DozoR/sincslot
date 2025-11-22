from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from passlib.context import CryptContext

from backend.core.config import JWT, Password
from backend.repository.token_repository import ITokenRepository
from backend.entity.token import TokenEntity, AccessTokenEntity, RefreshTokenEntity


class IToken(ABC):

    @abstractmethod
    async def save_tokens(
            self,
            session: AsyncSession,
            access_token: str,
            refresh_token: str,
            is_revoke: bool,
    ) -> TokenEntity:
        raise NotImplemented

    @abstractmethod
    async def update_tokens(self, session: AsyncSession, refresh_token: str) -> TokenEntity:
        raise NotImplemented

    @abstractmethod
    async def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def create_access_token(self, company_id: int) -> str:
        raise NotImplementedError

    @abstractmethod
    async def create_refresh_token(self, company_id: int) -> str:
        raise NotImplementedError

    @abstractmethod
    async def decode_token(self, token: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def is_expired(self, expired: int) -> bool:
        raise NotImplementedError


class Token(IToken):

    def __init__(
            self,
            token_repository: ITokenRepository,
            crypt_hasher: CryptContext,
            jwt_settings: JWT,
            password_settings: Password
    ):
        self.token_repository: ITokenRepository = token_repository
        self.crypt_hasher = crypt_hasher
        self.jwt_settings = jwt_settings
        self.password_settings = password_settings

    async def save_tokens(
            self,
            session: AsyncSession,
            access_token: str,
            refresh_token: str,
            is_revoke: bool,
    ) -> TokenEntity:
        return await self.token_repository.save_tokens(session, access_token, refresh_token, is_revoke)

    async def update_tokens(self, session: AsyncSession, refresh_token: str) -> TokenEntity:
        tokens = await self.token_repository.get_tokens_by_refresh_token(session, refresh_token)

        access_token = tokens.access_token

        payload = self.decode_token(access_token)

        new_access_token = await self.create_access_token(company_id=payload.get("company_id"))

        new_refresh_token = await self.create_refresh_token(company_id=payload.get("company_id"))

        return await self.token_repository.update_tokens(
            session,
            TokenEntity(
                access_token=new_access_token,
                refresh_token=new_refresh_token,
                is_revoke=True,
            ),
            refresh_token
        )

    async def hash_password(self, password: str) -> str:
        return self.crypt_hasher.hash(password)

    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.crypt_hasher.verify(plain_password, hashed_password)

    async def create_access_token(self, company_id: int) -> str:

        new_access_token = AccessTokenEntity(
            company_id=company_id,
            type=self.jwt_settings.token_type_access,
            exp=int(
                (datetime.now() + timedelta(minutes=self.jwt_settings.access_token_expire_minutes)).timestamp()
            )

        )

        encoded_access_jwt = jwt.encode(
            new_access_token.to_dict(),
            self.jwt_settings.secret_key,
            algorithm=self.jwt_settings.algorithm
        )

        return encoded_access_jwt

    async def create_refresh_token(self, company_id: int) -> str:
        new_refresh_token = RefreshTokenEntity(
            company_id=company_id,
            type=self.jwt_settings.token_type_refresh,
            exp=int(
                (datetime.now() + timedelta(minutes=self.jwt_settings.refresh_token_expire_minutes)).timestamp()
            )

        )

        encoded_refresh_jwt = jwt.encode(
            new_refresh_token.to_dict(),
            self.jwt_settings.secret_key,
            algorithm=self.jwt_settings.algorithm
        )

        return encoded_refresh_jwt

    async def decode_token(self, token: str) -> dict:
        payload = jwt.decode(token, self.jwt_settings.secret_key, algorithms=[self.jwt_settings.algorithm])
        return payload

    async def is_expired(self, expired: int) -> bool:
        now = int(datetime.now().timestamp())
        return expired > now
