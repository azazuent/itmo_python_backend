from pydantic import BaseModel

from collections import Counter

from .Item import Item
from ..schemas.Cart import Cart as DBCart


class CartItem(Item):
    quantity: int = 1


class Cart(BaseModel):
    id: int
    items: list[CartItem] = list()
    price: float = 0

    @classmethod
    def from_db_cart(cls, db_cart: DBCart):
        items = []
        for cart_item in db_cart.cart_items:
            items.append(
                CartItem.model_validate(
                    cart_item.item.__dict__ | {"quantity": cart_item.quantity}
                )
            )

        return cls.model_validate({
            "id": db_cart.id,
            "items": items,
            "price": sum([cart_item.item.price * cart_item.quantity
                          for cart_item in db_cart.cart_items])
        })
