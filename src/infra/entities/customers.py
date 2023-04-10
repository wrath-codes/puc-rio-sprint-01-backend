from sqlalchemy import Column, ForeignKey, Integer, String

from src.infra.config.database import Base


class Customers(Base):
    """Customers Entity"""

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)

    tab_id = Column(Integer, ForeignKey("tabs.id"))

    def __repr__(self):
        return f"Customer(id={self.id}, name={self.name}, email={self.email})"

    def __eq__(self, other):
        if (
            self.id == other.id
            and self.name == other.name
            and self.email == other.email
            and self.password == other.password
        ):
            return True
        return False
