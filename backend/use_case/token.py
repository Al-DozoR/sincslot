from typing import Optional
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from jose import jwt
from jose.exceptions import JWSError
from passlib.context import CryptContext
from backend.core.config import JWT, Password


class IToken(ABC):

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
    def verify_token(self, token: str):
        raise NotImplementedError


class Token(IToken):

    def __init__(self, crypt_hasher: CryptContext, jwt_settings: JWT, password_settings: Password):
        self.crypt_hasher = crypt_hasher
        self.jwt_settings = jwt_settings
        self.password_settings = password_settings

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

    def verify_token(self, token: str):
        payload = jwt.decode(token, self.jwt_settings.secret_key, algorithms=[self.jwt_settings.algorithm])
        return payload