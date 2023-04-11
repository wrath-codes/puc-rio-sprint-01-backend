from pydantic import BaseModel


class StepSchema(BaseModel):
    """Define como um novo passo inserido deve ser representado"""

    recipe_id: int = 1
    title: str = "Misture tudo"
    description: str = "Misture todos os ingredientes"


class StepUpdateSchema(BaseModel):
    """Define como um passo atualizado deve ser representado"""

    title: str = "Misture tudo"
    description: str = "Misture todos os ingredientes"


class StepDeleteSchema(BaseModel):
    """Define como um passo deletado deve ser representado"""

    message: str
    title: str
