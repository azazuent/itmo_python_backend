from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from http import HTTPStatus
from typing import Optional

from ..database import ItemCRUD, ItemModels, get_db


router = APIRouter(
    prefix="/item",
    tags=["Items"]
)


@router.post("", response_model=ItemModels.Item, status_code=HTTPStatus.CREATED)
def add_item(item: ItemModels.ItemCreate, db: Session = Depends(get_db)):
    db_item = ItemCRUD.read_item_by_name(db, item.name)
    if db_item is not None:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "This name is already in use")

    db_item = ItemCRUD.create_item(db, item)
    return db_item


@router.get("", response_model=list[ItemModels.Item], status_code=HTTPStatus.OK)
def get_items(
        offset: int = Query(0, ge=0),
        limit: int = Query(10, ge=1),
        min_price: Optional[float] = Query(None, ge=0),
        max_price: Optional[float] = Query(None, ge=0),
        show_deleted: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    return ItemCRUD.read_items(db, limit, offset, min_price, max_price, show_deleted)


@router.get("/{item_id}", response_model=ItemModels.Item, status_code=HTTPStatus.OK)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = ItemCRUD.read_item(db, item_id)
    if db_item is None or db_item.deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND)
    return db_item


@router.patch("/{item_id}", response_model=ItemModels.Item)
def patch_item(item_id: int, item: ItemModels.ItemPatch, db: Session = Depends(get_db)):
    db_item = ItemCRUD.read_item(db, item_id)
    if db_item is None or db_item.deleted:
        raise HTTPException(HTTPStatus.NOT_MODIFIED)

    # for key, value in item.model_dump(exclude_unset=True).items():
    #     if getattr(db_item, key) != value:
    return ItemCRUD.update_item(db, db_item, item)

    # raise HTTPException(HTTPStatus.NOT_MODIFIED)


@router.put("/{item_id}", response_model=ItemModels.Item)
def put_item(item_id: int, item: ItemModels.ItemPut, db: Session = Depends(get_db)):
    db_item = ItemCRUD.read_item(db, item_id)
    if not db_item:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    return ItemCRUD.update_item(db, db_item, item)


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = ItemCRUD.read_item(db, item_id)
    if not db_item:
        raise HTTPException(HTTPStatus.NOT_FOUND)

    ItemCRUD.delete_item(db, db_item)
