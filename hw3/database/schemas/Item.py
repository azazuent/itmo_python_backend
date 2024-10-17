from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

from ..db_utils import Base


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)

    name = Column(String)  # , unique=True)
    price = Column(Float)
    deleted = Column(Boolean)

    cart_items = relationship("CartItem", back_populates="item")
