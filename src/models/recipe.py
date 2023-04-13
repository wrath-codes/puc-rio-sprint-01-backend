from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.config.database import Base


class Recipe(Base):
    """Recipe model"""

    __tablename__ = "recipes"

    id = Column("pk_recipe", Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False)
    description = Column(String(255), nullable=True)

    # Definição do relacionamento entre Recipe e Ingredient
    ingredients = relationship("Ingredient", lazy="joined")

    # Definição do relacionamento entre Recipe e Step
    steps = relationship("Step", lazy="joined")
