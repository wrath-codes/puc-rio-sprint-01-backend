from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str
    quantity: str


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(IngredientBase):
    pass


class Ingredient(IngredientBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True
