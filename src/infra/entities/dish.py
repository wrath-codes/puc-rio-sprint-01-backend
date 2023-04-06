from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.infra.config.database import Base


class Dish(Base):
    __tablename__ = "dish"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

    menu_id = Column(Integer, ForeignKey("menu.id"))
    menu = relationship("Menu", back_populates="dishes")

    def __repr__(self):
        return f"Dish(name={self.name})"

    def __eq__(self, other):
        if (
            self.name == other.name
            and self.description == other.description
            and self.price == other.price
        ):
            return True
        return False
