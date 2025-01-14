# main.py

import logging
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.db import close_db, init_db
from app.modules.event.router import router as event_router
from app.modules.user.router import router as user_router

# -----------------------
# LIFESPAN EVENT:
# -----------------------


@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_db()

    yield

    await close_db()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/api")
app.include_router(event_router, prefix="/api")


# Configuración básica de logging
logging.basicConfig(
    level=logging.ERROR,  # Cambia a DEBUG/INFO para ver más detalles
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


# # Handler genérico para cualquier otra excepción -> Devuelve 500
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error at {request.url}: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
