from sqlalchemy import Column, Integer, String

from src.infra.config.database import Base


class Dishes(Base):
    """Dishes Entity"""

    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

    def __repr__(self):
        return f"Dish(id={self.id}, name={self.name}, price={self.price}, menu_id={self.menu_id})"

    def __eq__(self, other):
        if (
            self.id == other.id
            and self.name == other.name
            and self.description == other.description
            and self.price == other.price
        ):
            return True
        return False
