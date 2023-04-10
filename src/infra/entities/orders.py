from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.infra.config.database import Base


class Orders(Base):
    """Orders Entity"""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))

    tab_id = Column(Integer, ForeignKey("tabs.id"))
    tab = relationship("Tabs", back_populates="orders")

    def __repr__(self):
        return f"Order(id={self.id}, customer_id={self.customer_id})"

    def __eq__(self, other):
        if (
            self.id == other.id
            and self.customer_id == other.customer_id
            and self.dishes == other.dishes
        ):
            return True
        return False
