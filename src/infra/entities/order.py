from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.infra.config.database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    date = Column(DateTime(timezone=True), nullable=False)

    dishes = relationship("Dish", secondary="dish_order", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")

    def __repr__(self):
        return f"Order(customer={self.customer})"

    def __eq__(self, other):
        if self.customer == other.customer:
            return True
        return False
