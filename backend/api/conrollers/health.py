from fastapi import APIRouter, status
from starlette.responses import JSONResponse

router_health = APIRouter(tags=["health"])


@router_health.get("/")
async def health():
    return JSONResponse(status_code=status.HTTP_200_OK, content="ok")


@router_health.get("/")
async def health_auth():
    pass
