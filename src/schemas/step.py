from typing import Optional

from pydantic import BaseModel


class StepBase(BaseModel):
    title: str
    description: Optional[str] = None


class StepCreate(StepBase):
    pass


class StepUpdate(StepBase):
    pass


class Step(StepBase):
    id: int
    recipe_id: int

    prev_step: Optional[int] = None
    next_step: Optional[int] = None

    class Config:
        orm_mode = True
