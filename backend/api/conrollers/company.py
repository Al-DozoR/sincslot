from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from backend.api.requests.company import CreateCompany

router_user = APIRouter()


@router_user.post("/", tags=["user"])
async def register_company(company: CreateCompany) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content="ok")
