from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from passlib.context import CryptContext

from backend.core.config import JWT, Password
from backend.repository.token_repository import ITokenRepository, TokenRepository
from backend.entity.token import TokenEntity


class IToken(ABC):

    @abstractmethod
    async def save_tokens(
            self,
            session: AsyncSession,
            access_token: str,
            refresh_token: str,
    ) -> TokenEntity:
        raise NotImplemented

    @abstractmethod
    async def update_tokens(self, session: AsyncSession, refresh_token: str) -> TokenEntity:
        raise NotImplemented

    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create_access_token(self, to_encode: dict) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_refresh_token(self, to_encode: dict) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> dict:
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
    ) -> TokenEntity:
        return await self.token_repository.save_tokens(session, access_token, refresh_token)

    async def update_tokens(self, session: AsyncSession, refresh_token: str) -> TokenEntity:
        tokens = await self.token_repository.get_tokens_by_refresh_token(session, refresh_token)

        access_token = tokens.access_token

        payload = self.decode_token(access_token)

        new_access_token = self.create_access_token(to_encode={
            "company_id": payload.get("company_id"),
            "name": payload.get("name"),
            "email": payload.get("email")
        })

        new_refresh_token = self.create_refresh_token(
            to_encode={
                "company_id": payload.get("company_id"),
                "name": payload.get("name"),
                "email": payload.get("email")
            }
        )

        return await self.token_repository.update_tokens(
            session,
            TokenEntity(
                access_token=new_access_token,
                refresh_token=new_refresh_token
            ),
            refresh_token
        )

    def hash_password(self, password: str) -> str:
        return self.crypt_hasher.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.crypt_hasher.verify(plain_password, hashed_password)

    def create_access_token(self, to_encode: dict) -> str:
        expire = datetime.now() + timedelta(minutes=self.jwt_settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.jwt_settings.secret_key, algorithm=self.jwt_settings.algorithm)

        return encoded_jwt

    def create_refresh_token(self, to_encode: dict) -> str:
        expire = datetime.now() + timedelta(minutes=self.jwt_settings.refresh_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.jwt_settings.secret_key, algorithm=self.jwt_settings.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        payload = jwt.decode(token, self.jwt_settings.secret_key, algorithms=[self.jwt_settings.algorithm])
        return payload
