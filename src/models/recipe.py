from datetime import datetime
from typing import Union

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.config.database import Base
from src.models import Ingredient, Step


class Recipe(Base):
    """Recipe model"""

    __tablename__ = "recipes"

    id = Column("pk_recipe", Integer, primary_key=True)
    title = Column(String(250), unique=True, nullable=False)
    description = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre Recipe e Ingredient
    ingredients = relationship("Ingredient")

    # Definição do relacionamento entre Recipe e Step
    steps = relationship("Step")

    def __init__(
        self, title: str, description: str, created_at: Union[datetime, None] = None
    ):
        """
        Criar uma Receita

        Args:
            title (str): Título da receita
            description (str): Descrição da receita
            created_at (Union[datetime, None], optional): Data de criação da receita. Defaults to None.
        """
        self.title = title
        self.description = description

        if created_at:
            self.created_at = created_at

    def add_ingredient(self, ingredient: "Ingredient"):
        """Adicionar um ingrediente a uma receita"""
        self.ingredients.append(ingredient)

    def add_step(self, step: "Step"):
        """Adicionar um passo a uma receita"""
        self.steps.append(step)
