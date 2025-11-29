from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from backend.logger.logger import init_logger


logger = init_logger('company_use_case', 'INFO')


class IClientUseCase(ABC):

    @abstractmethod
    async def save_client(
            self,
            session: AsyncSession,
            phone: str,
    ):
        raise NotImplemented

    @abstractmethod
    async def get_client_by_id(self, session: AsyncSession, client_id: int):
        raise NotImplemented

    @abstractmethod
    async def get_client_by_phone(self, session: AsyncSession, phone: str):
        raise NotImplemented
