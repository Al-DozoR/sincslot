from abc import ABC, abstractmethod

from backend.entity.token import TokenEntity
from backend.repository.models.company import Company
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete
from backend.repository.unit_of_work.unit_of_work import UnitOfWork


class ITokenRepository(ABC):

    @abstractmethod
    async def save_tokens(
            self,
            session: AsyncSession,
            access_token: str,
            refresh_token: str,
    ) -> TokenEntity:
        raise NotImplemented

    @abstractmethod
    async def get_tokens_by_refresh_token(self, session: AsyncSession, refresh_token: str) -> TokenEntity:
        raise NotImplemented

    @abstractmethod
    async def update_tokens(self, tokens: TokenEntity) -> TokenEntity:
        raise NotImplemented


class TokenRepository(ITokenRepository):

    async def save_tokens(
            self,
            session: AsyncSession,
            access_token: str,
            refresh_token: str,
    ) -> TokenEntity:
        pass

    async def get_tokens_by_refresh_token(self, session: AsyncSession, refresh_token: str) -> TokenEntity:
        pass