from datetime import datetime
from typing import Union

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from src.config.database import Base


class Ingredient(Base):
    """Ingredient model"""

    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    quantity = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre Ingredient e Recipe
    recipe_id = Column(Integer, ForeignKey("recipes.pk_recipe"), nullable=False)

    def __init__(
        self, name: str, quantity: str, created_at: Union[datetime, None] = None
    ):
        """
        Criar um Ingrediente

        Args:
            name (str): Nome do ingrediente
            created_at (Union[datetime, None], optional): Data de criação do ingrediente. Defaults to None.
        """
        self.name = name
        self.quantity = quantity

        if created_at:
            self.created_at = created_at
