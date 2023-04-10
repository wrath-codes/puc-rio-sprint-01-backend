from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.infra.config.database import Base


class Tabs(Base):
    """Tabs Entity"""

    __tablename__ = "tabs"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    orders = relationship("Orders")

    def __repr__(self):
        return f"Tab(id={self.id}, customer_id={self.customer_id})"

    def __eq__(self, other):
        if (
            self.id == other.id
            and self.customer_id == other.customer_id
            and self.dishes == other.dishes
        ):
            return True
        return False
