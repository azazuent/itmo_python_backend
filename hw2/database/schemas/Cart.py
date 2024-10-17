from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from ..db_utils import Base


class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True)
    cart_items = relationship("CartItem", back_populates="cart")

    @property
    def price(self) -> float:
        return sum(cart_item.item.price * cart_item.quantity
                   for cart_item in self.cart_items)

    @property
    def size(self) -> float:
        return sum(cart_item.quantity for cart_item in self.cart_items)
