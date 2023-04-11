from pydantic import BaseModel


class IngredientSchema(BaseModel):
    """Define como um novo ingrediente inserido deve ser representado"""

    recipe_id: int = 1
    name: str = "Farinha"
    quantity: str = "1kg"


class IngredientUpdateSchema(BaseModel):
    """Define como um ingrediente atualizado deve ser representado"""

    name: str = "Farinha"
    quantity: str = "1kg"


class IngredientDeleteSchema(BaseModel):
    """Define como um ingrediente deletado deve ser representado"""

    message: str
    name: str
