from sqlalchemy import Column, ForeignKey, Integer

from src.infra.config.database import Base


class DishOrders(Base):
    """Association Table to Dish and Orders"""

    __tablename__ = "dish_orders"

    dish_id = Column(Integer, ForeignKey("dishes.id"), primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
