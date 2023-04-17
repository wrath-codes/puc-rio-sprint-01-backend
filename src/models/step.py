from sqlalchemy import Column, ForeignKey, Integer, String

from src.config.database import Base


class Step(Base):
    """Step model"""

    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)

    # Definição do relacionamento entre Step e Step
    prev_step = Column(Integer, ForeignKey("steps.id"), nullable=True)
    next_step = Column(Integer, ForeignKey("steps.id"), nullable=True)

    # Definição do relacionamento entre Step e Recipe
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
