from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.infra.config.database import Base


class Customers(Base):
    """Customers Entity"""

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)

    tabs = relationship("Tabs")

    def __repr__(self):
        return f"Customer(name={self.name}"

    def __eq__(self, other):
        if (
            self.id == other.id
            and self.name == other.name
            and self.phone == other.phone
        ):
            return True
        return False
