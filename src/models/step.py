from datetime import datetime
from typing import Union

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from src.config.database import Base


class Step(Base):
    """Step model"""

    __tablename__ = "steps"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre Step e Recipe
    recipe_id = Column(Integer, ForeignKey("recipes.pk_recipe"), nullable=False)

    def __init__(
        self, title: str, description: str, created_at: Union[datetime, None] = None
    ):
        """
        Criar um Passo

        Args:
            description (str): Descrição do passo
            created_at (Union[datetime, None], optional): Data de criação do passo. Defaults to None.
        """
        self.title = title
        self.description = description

        if created_at:
            self.created_at = created_at
