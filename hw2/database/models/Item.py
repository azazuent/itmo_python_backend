from typing import Optional, Annotated

from pydantic import BaseModel, NonNegativeFloat, ConfigDict


class ItemBase(BaseModel):
    name: str
    price: Annotated[float, NonNegativeFloat]


class ItemCreate(ItemBase):
    deleted: Optional[bool] = False


class Item(ItemCreate):
    id: int


class ItemPatch(ItemBase):
    name: Optional[str] = None
    price: Optional[Annotated[float, NonNegativeFloat]] = None

    model_config = ConfigDict(
        extra='forbid'
    )


class ItemPut(ItemBase):
    ...
