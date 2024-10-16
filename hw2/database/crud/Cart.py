from typing import Optional

from ..models.Cart import Cart
from ..DBExceptions import NotFound, AlreadyExists, NotModified
from .Item import items


carts: dict[int, Cart] = {}
next_id = 0


def create_cart():
    global carts, next_id

    cart = Cart.parse_obj({"id": next_id})

    carts[next_id] = cart
    next_id += 1

    return cart


def read_cart(cart_id: int):
    if cart_id not in carts:
        raise NotFound

    return carts[cart_id]


def read_carts(
        offset: int, limit: int,
        min_price: Optional[float], max_price: Optional[float],
        min_quantity: Optional[int], max_quantity: Optional[int]
) -> list[Cart]:
    cart_list = list(carts.values())

    if min_price is not None:
        cart_list = [cart for cart in cart_list if min_price <= cart.price]
    if max_price is not None:
        cart_list = [cart for cart in cart_list if cart.price <= max_price]

    if min_quantity is not None:
        cart_list = [cart for cart in cart_list if min_quantity <= cart.item_quantity()]
    if max_quantity is not None:
        cart_list = [cart for cart in cart_list if cart.item_quantity() <= max_quantity]

    cart_list_size = len(cart_list)

    start = offset
    end = min(cart_list_size, offset + limit)

    if offset > cart_list_size:
        return []

    return cart_list[start:end]


def add_item_to_cart(cart_id, item_id):
    if cart_id not in carts:
        raise NotFound
    if item_id not in items:
        raise NotFound

    cart = carts[cart_id]
    item = items[item_id]

    if item_id in cart.items