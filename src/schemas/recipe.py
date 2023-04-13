from typing import List, Optional

from pydantic import BaseModel

from .ingredient import Ingredient
from .step import Step


class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = None


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int

    ingredients: List[Ingredient] = None
    steps: List[Step] = None

    class Config:
        orm_mode = True
