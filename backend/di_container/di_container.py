from rodi import Container

from backend.repository.company_repository import ICompanyRepository, CompanyRepository
from backend.use_case.company_use_case import ICompanyUseCase, CompanyUseCase


class DIContainer:
    container = Container()

    container.add_transient(ICompanyRepository, CompanyRepository)
    container.add_transient(ICompanyUseCase, CompanyUseCase)

    def get_company_use_cases(self) -> ICompanyRepository:
        return self.container.resolve(ICompanyRepository)


di_container = DIContainer()
