from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.responses import JSONResponse

from backend.use_case.token_use_case import IToken
from backend.use_case.company_use_case import ICompanyUseCase
from backend.core.db_helper import db_helper


class AuthCompanyMiddleware(BaseHTTPMiddleware):

    def __init__(
            self,
            *args,
            token_use_case: IToken,
            company_use_case: ICompanyUseCase,
            exclude_path: list[str],
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.token_use_case: IToken = token_use_case
        self.company_use_case: ICompanyUseCase = company_use_case
        self.exclude_path = exclude_path

    def is_skip(self, url: str, exclude_path):

        for p in exclude_path:
            if p in url:
                return True

        return False

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

        print(request.url.path)

        self.exclude_path = ["docs", "openapi", "health", "login", "register"]

        if self.is_skip(request.url.path, self.exclude_path):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "No authorization header"}
            )

            # Проверяем формат: "Bearer <token>"
        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header must start with 'Bearer '"}
            )

        token = auth_header[len("Bearer "):].strip()
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token is empty"}
            )

        try:
            payload = self.token_use_case.decode_token(token)
        except Exception as ex:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Failed to parse auth token"}
            )

        email = payload.get("email")
        if email is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Failed to get email from auth token"}
            )

        company = self.company_use_case.get_company_by_email(db_helper.session_getter(), email)
        if company is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Failed to get company by email"}
            )

        response = await call_next(request)
        return response