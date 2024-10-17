from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ..db_utils import Base


class CartItem(Base):
    __tablename__ = "cart_item",

    id = Column(Integer, primary_key=True)

    cart_id = Column(Integer, ForeignKey("cart.id"))
    item_id = Column(Integer, ForeignKey("item.id"))

    cart = relationship("Cart", back_populates="cart_items")
    item = relationship("Item", back_populates="cart_items")

    quantity = Column(Integer)
