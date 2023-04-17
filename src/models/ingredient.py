from sqlalchemy import Column, ForeignKey, Integer, String

from src.config.database import Base


class Ingredient(Base):
    """Ingredient model"""

    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    quantity = Column(String(50), nullable=False)

    # Definição do relacionamento entre Ingredient e Recipe
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
