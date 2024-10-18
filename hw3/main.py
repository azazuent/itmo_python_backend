from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from database import create_schema
from routers import items_router, carts_router

# Почему-то не работает через lifespan
# @asynccontextmanager
# async def lifespan(application: FastAPI):
#     create_schema()
#     yield

create_schema()
app = FastAPI(
    title="Shop API"
)

Instrumentator().instrument(app).expose(app)

app.include_router(items_router)
app.include_router(carts_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
