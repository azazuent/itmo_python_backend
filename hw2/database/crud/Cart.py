from typing import Optional

from sqlalchemy.orm import Session

from ..schemas.Cart import Cart as DBCart
from ..schemas.Item import Item as DBItem
from ..schemas.CartItem import CartItem as DBCartItem


def create_cart(db: Session) -> DBCart:
    db_cart = DBCart()
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)

    return db_cart


def read_cart(db: Session, cart_id: int):
    return db.get(DBCart, cart_id)


def read_carts(
        db: Session,
        offset: int, limit: int,
        min_price: Optional[float], max_price: Optional[float],
        min_quantity: Optional[int], max_quantity: Optional[int]
) -> list[DBCart]:
    db_carts = db.query(DBCart).all()

    filtered_db_carts = []
    for db_cart in db_carts:
        if min_price is not None:
            if db_cart.price < min_price:
                continue
        if max_price is not None:
            if db_cart.price > max_price:
                continue

        if min_quantity is not None:
            if db_cart.size < min_quantity:
                continue
        if max_quantity is not None:
            if db_cart.size > max_quantity:
                continue

        filtered_db_carts.append(db_cart)

    if offset > len(filtered_db_carts):
        return []

    start = offset
    end = min(limit + offset, len(filtered_db_carts))

    return filtered_db_carts[start:end]


def add_item(db: Session, db_cart: DBCart, db_item: DBItem) -> DBCart:
    db_cart_item = db.query(DBCartItem)\
        .filter(DBCartItem.item_id == db_item.id) \
        .filter(DBCartItem.cart_id == db_cart.id)\
        .first()

    if db_cart_item is not None:
        db_cart_item.quantity += 1

    else:
        db_cart_item = DBCartItem(
            cart_id=db_cart.id,
            item_id=db_item.id,
            quantity=1
        )
        db.add(db_cart_item)

    db.commit()
    db.refresh(db_cart)

    return db_cart
