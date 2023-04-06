from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.infra.config.database import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    phone = Column(String)

    orders = relationship("Order", back_populates="customer")

    def __repr__(self):
        return f"Customer(name={self.name})"

    def __eq__(self, other):
        if (
            self.name == other.name
            and self.address == other.address
            and self.phone == other.phone
        ):
            return True
        return False
