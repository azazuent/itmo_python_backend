from typing import Optional

from sqlalchemy.orm import Session

from ..models.Item import ItemCreate, ItemPut, ItemPatch
from ..schemas.Item import Item as DBItem


def create_item(db: Session, item: ItemCreate) -> DBItem:
    db_item = DBItem(
        name=item.name,
        price=item.price,
        deleted=item.deleted
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def read_item(db: Session, item_id: int) -> DBItem:
    return db.get(DBItem, item_id)


def read_item_by_name(db: Session, item_name: str) -> DBItem:
    return db.query(DBItem).filter(DBItem.name == item_name).first()


def read_items(db: Session,
               limit: int, offset: int,
               min_price: Optional[float], max_price: Optional[float],
               show_deleted: Optional[bool]
               ) -> list[DBItem]:
    items = db.query(DBItem)

    if min_price is not None:
        items = items.filter(DBItem.price >= min_price)
    if max_price is not None:
        items = items.filter(DBItem.price <= max_price)

    if show_deleted is not None and show_deleted is False:
        items = items.filter(DBItem.deleted is False)

    return items.limit(limit).offset(offset).all()


def update_item(db: Session, db_item: DBItem, item_update: ItemPut | ItemPatch) -> DBItem:
    update_data = item_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def delete_item(db: Session, db_item: DBItem) -> None:
    db_item.deleted = True
    db.commit()
