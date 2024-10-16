from fastapi import FastAPI

from .routers import items_router


app = FastAPI(
    title="Shop API"
)

app.include_router(items_router)
