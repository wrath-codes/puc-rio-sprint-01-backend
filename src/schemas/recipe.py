from typing import List

from pydantic import BaseModel

from src.models import Recipe
from src.schemas import IngredientSchema, StepSchema


class RecipeSchema(BaseModel):
    """Define como uma nova receita inserida deve ser representada"""

    title: str = "Bolo de cenoura"
    description: str = "Receita de bolo de cenoura da Ana Maria Braga"


class RecipeSearchSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca de receitas.
    Será utilizado o id para buscar a receita, ou o título para buscar uma lista de receitas.
    """

    recipes = List[RecipeSchema]


class RecipeListSchema(BaseModel):
    """Define como deve ser a estrutura que representa uma lista de receitas."""

    recipes = List[RecipeSchema]


class RecipeViewSchema(BaseModel):
    """Define como deve ser a estrutura que representa uma receita + passos + ingredientes."""

    name: str
    description: str
    total_steps: int = 1
    total_ingredients: int = 1
    ingredients: List[IngredientSchema]
    steps: List[StepSchema]


class RecipeUpdateSchema(BaseModel):
    """Define como deve ser a estrutura que representa uma receita atualizada."""

    name: str = "Bolo de cenoura"
    description: str = "Receita de bolo de cenoura da Ana Maria Braga"


class RecipeDeleteSchema(BaseModel):
    """Define como deve ser a estrutura de dado retarnada após ma requisição de
    remoção de uma receita.
    """

    message: str
    nome: str


def present_recipe(recipe: Recipe) -> RecipeViewSchema:
    """Retorna uma representação de uma receita seguindo o schema RecipeViewSchema"""
    return {
        "name": recipe.title,
        "description": recipe.description,
        "total_steps": len(recipe.steps),
        "total_ingredients": len(recipe.ingredients),
        "ingredients": [
            {"name": ingredient.name, "quantity": ingredient.quantity}
            for ingredient in recipe.ingredients
        ],
        "steps": [
            {"title": step.title, "description": step.description}
            for step in recipe.steps
        ],
    }


def present_recipes(recipes: List[Recipe]) -> RecipeListSchema:
    """Retorna uma representação de receitas seguindo o schema RecipeViewSchema"""
    result = []
    for recipe in recipes:
        result.append(
            {
                "name": recipe.title,
                "description": recipe.description,
            }
        )

    return {"recipes": result}
