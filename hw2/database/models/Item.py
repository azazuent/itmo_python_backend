from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    deleted: Optional[bool] = False


class ItemWithId(Item):
    id: int


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None


class ItemCart(ItemWithId):
    quantity: int
