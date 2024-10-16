from ..models.Item import Item, ItemWithId, ItemUpdate

from ..DBExceptions import NotFound, AlreadyExists, NotModified

items: dict[int, ItemWithId] = {}
next_id: int = 0


def create_item(item: Item) -> ItemWithId:
    global items, next_id

    if item.name in [value.name for value in items.values()]:
        raise AlreadyExists

    item_with_id = item.model_dump()
    item_with_id["id"] = next_id
    item_with_id = ItemWithId.parse_obj(item_with_id)

    items[next_id] = item_with_id
    next_id += 1

    return item_with_id


def read_item(item_id: int) -> ItemWithId:
    if item_id not in items:
        raise NotFound

    return items[item_id]


def read_items(limit: int = 50, offset: int = 0) -> list[ItemWithId]:
    item_list = list(items.values())
    item_list_size = len(item_list)

    start = offset
    end = min(item_list_size, offset + limit)

    if offset > item_list_size:
        return []

    return item_list[start:end]


def put_item(item_id: int, item: Item):
    global items

    if item.name in [value.name for value in items.values() if value.id != item_id]:
        raise AlreadyExists

    item["id"] = item_id
    items[item_id] = ItemWithId.parse_obj(item)

    return items[item_id]


def update_item(item_id: int, item: ItemUpdate) -> ItemWithId:
    global items

    if item_id not in items:
        raise NotFound

    item = item.model_dump(exclude_unset=True)
    if not item:
        raise NotModified

    updated_item = items[item_id].model_dump()
    updated_item.update(item)

    items[item_id] = ItemWithId.parse_obj(updated_item)

    return items[item_id]


def delete_item(item_id: int) -> None:
    global items

    if item_id not in items:
        raise NotFound

    del items[item_id]
