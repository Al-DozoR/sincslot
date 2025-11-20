from rodi import Container
from passlib.context import CryptContext

from backend.repository.company_repository import ICompanyRepository, CompanyRepository
from backend.repository.token_repository import ITokenRepository, TokenRepository
from backend.use_case.company_use_case import ICompanyUseCase, CompanyUseCase
from backend.use_case.token_use_case import IToken, Token
from backend.core.config import settings


class DIContainer:
    container = Container()

    container.add_transient(ICompanyRepository, CompanyRepository)
    container.add_transient(ITokenRepository, TokenRepository)
    container.add_transient(ICompanyUseCase, CompanyUseCase)
    container.add_transient(IToken, Token)
    container.add_instance(CryptContext(schemes=["bcrypt"], deprecated="auto"))
    container.add_instance(settings.jwt)
    container.add_instance(settings.password)


    def get_company_use_cases(self) -> ICompanyUseCase:
        return self.container.resolve(ICompanyUseCase)

    def get_token_use_case(self) -> IToken:
        return self.container.resolve(IToken)


di_container = DIContainer()
