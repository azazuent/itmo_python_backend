from pydantic import BaseModel


class CartItem(BaseModel):
    item_id: int
    quantity: int = 1


class Cart(BaseModel):
    id: int
    items: list[CartItem] = list()
    price: float = 0
