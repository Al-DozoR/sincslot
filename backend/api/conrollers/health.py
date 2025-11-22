from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import JSONResponse

router_health = APIRouter(tags=["health"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


@router_health.get("/health")
async def health():
    return JSONResponse(status_code=status.HTTP_200_OK, content="ok")


@router_health.get("/health_auth")
async def health(token: str = Depends(oauth2_scheme)):
    return JSONResponse(status_code=status.HTTP_200_OK, content="ok")
