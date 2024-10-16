from fastapi import APIRouter, HTTPException

from http import HTTPStatus

from ..database import DBExceptions
from ..database.crud import Item

router = APIRouter(
    prefix="/item"
)


@router.post("", response_model=Item.ItemWithId, status_code=HTTPStatus.CREATED)
def add_item(item: Item.Item):
    try:
        return Item.create_item(item)
    except DBExceptions.AlreadyExists:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "This name is already in use")


@router.get("", response_model=list[Item.ItemWithId])
def get_items(limit: int = 50, offset: int = 0):
    return Item.read_items(limit, offset)


@router.get("/{item_id}", response_model=Item.ItemWithId)
def get_item(item_id: int):
    try:
        return Item.read_item(item_id)
    except DBExceptions.NotFound:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Item not found")


@router.patch("/{item_id}", response_model=Item.ItemWithId)
def patch_item(item_id: int, item: Item.ItemUpdate):
    try:
        return Item.update_item(item_id, item)
    except DBExceptions.NotFound:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Item not found")
    except DBExceptions.NotModified:
        raise HTTPException(HTTPStatus.NOT_MODIFIED, "Item not modified")


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int):
    try:
        Item.delete_item(item_id)
    except DBExceptions.NotFound:
        raise HTTPException(HTTPStatus.NOT_FOUND, "Item not found")