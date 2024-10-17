from fastapi import APIRouter, Depends, HTTPException, Response, Query
from pydantic import NonNegativeInt
from sqlalchemy.orm import Session

from http import HTTPStatus
from typing import Annotated, Optional

from ..database import CartCRUD, ItemCRUD, CartModels, get_db

router = APIRouter(
    prefix="/cart",
    tags=["Carts"]
)


@router.post("", response_model=CartModels.Cart, status_code=HTTPStatus.CREATED)
def initialize_cart(response: Response, db: Session = Depends(get_db)):
    db_cart = CartCRUD.create_cart(db)
    response.headers["location"] = f"/carts/{db_cart.id}"
    return db_cart


@router.get("/{cart_id}", response_model=CartModels.Cart)
def get_cart(cart_id: Annotated[int, NonNegativeInt],
             db: Session = Depends(get_db)):
    db_cart = CartCRUD.read_cart(db, cart_id)
    if db_cart is None:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    return CartModels.Cart.from_db_cart(db_cart)


@router.get("", response_model=list[CartModels.Cart])
def get_carts(
        offset: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        min_price: Optional[float] = Query(None, ge=0),
        max_price: Optional[float] = Query(None, ge=0),
        min_quantity: Optional[int] = Query(None, ge=0),
        max_quantity: Optional[int] = Query(None, ge=0),
        db: Session = Depends(get_db)):
    db_carts = CartCRUD.read_carts(db,
                                   offset, limit,
                                   min_price, max_price,
                                   min_quantity, max_quantity)

    return [CartModels.Cart.from_db_cart(db_cart) for db_cart in db_carts]


@router.post("/{cart_id}/add/{item_id}", response_model=CartModels.Cart)
def add_item_to_cart(cart_id: Annotated[int, NonNegativeInt],
                     item_id: Annotated[int, NonNegativeInt],
                     db: Session = Depends(get_db)):
    db_cart = CartCRUD.read_cart(db, cart_id)
    if db_cart is None:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    db_item = ItemCRUD.read_item(db, item_id)
    if db_item is None:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    CartCRUD.add_item(db, db_cart, db_item)
    return CartModels.Cart.from_db_cart(db_cart)
