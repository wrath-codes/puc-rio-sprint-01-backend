from typing import Optional

from pydantic import BaseModel


class StepBase(BaseModel):
    name: str
    description: Optional[str] = None

    prev_step: Optional[int] = None
    next_step: Optional[int] = None


class StepCreate(StepBase):
    pass


class Step(StepBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True
