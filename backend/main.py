import logging

import uvicorn
from fastapi import FastAPI
from backend.conrollers.user.handlers import router_user



app = FastAPI()

app.include_router(router_user)

if __name__ == "__main__":
    logging.info(f'Start server: 3000')
    uvicorn.run("main:app",
                port=3000)