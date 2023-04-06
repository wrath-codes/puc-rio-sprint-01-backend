from sqlalchemy import Column, ForeignKey, Integer

from src.infra.config.database import Base


class DishOrder(Base):
    """Class to define the association between Dish and Order"""

    __tablename__ = "dish_order"
    dish_id = Column(Integer, ForeignKey("dish.id"), primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"), primary_key=True)
