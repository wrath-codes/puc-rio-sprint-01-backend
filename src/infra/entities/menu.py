from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import relationship

from src.infra.config.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), nullable=False)

    dishes = relationship("Dish", back_populates="menu")

    def __repr__(self):
        return f"Menu(date={self.date})"

    def __eq__(self, other):
        if self.name == other.name and self.description == other.description:
            return True
        return False
