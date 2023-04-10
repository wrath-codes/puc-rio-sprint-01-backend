import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from src.infra.config.database import Base


class StatusTab(enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class Tabs(Base):
    """Tabs Entity"""

    __tablename__ = "tabs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(StatusTab))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    orders = relationship("Orders")

    def __repr__(self):
        return f"Tab(customer_id={self.customer_id}, status={self.status})"

    def __eq__(self, other):
        if (
            self.id == other.id
            and self.status == other.status
            and self.customer_id == other.customer_id
        ):
            return True
        return False
