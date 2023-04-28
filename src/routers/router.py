from typing import List

from fastapi import APIRouter, HTTPException

from src.schemas import (
    Ingredient,
    IngredientCreate,
    IngredientUpdate,
    Recipe,
    RecipeCreate,
    RecipeUpdate,
    Step,
    StepCreate,
    StepUpdate,
)
from src.services import (
    ingredient_create,
    ingredient_delete,
    ingredient_get_by_id,
    ingredient_get_by_recipe,
    ingredient_update,
    recipe_create,
    recipe_delete,
    recipe_get_all,
    recipe_get_one,
    recipe_search,
    recipe_update,
    step_create,
    step_delete,
    step_get_all_ordered,
    step_get_by_id,
    step_swap,
    step_update,
)

main_router = APIRouter(
    prefix="/recipes",
    responses={404: {"description": "Not found"}},
)


@main_router.post("/", response_model=Recipe, status_code=201, tags=["Recipes"])
def create_recipe(recipe: RecipeCreate):
    """Create a new recipe"""
    return recipe_create(recipe)


@main_router.get("/", response_model=List[Recipe], tags=["Recipes"])
def get_recipes():
    """Get all recipes"""
    recipes = recipe_get_all()
    if not recipes:
        return []
    return recipes


@main_router.get("/{recipe_id}", response_model=Recipe, tags=["Recipes"])
def get_recipe(recipe_id: int):
    """Get a recipe by id"""
    recipe = recipe_get_one(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@main_router.put("/{recipe_id}", response_model=Recipe, tags=["Recipes"])
def update_recipe(recipe_id: int, recipe: RecipeUpdate):
    """Update a recipe by id"""
    return recipe_update(recipe, recipe_id)


@main_router.delete("/{recipe_id}", status_code=200, tags=["Recipes"])
def delete_recipe(recipe_id: int):
    """Delete a recipe by id"""
    if recipe_delete(recipe_id):
        return {"message": "Recipe deleted successfully"}
    raise HTTPException(status_code=404, detail="Recipe not found")


@main_router.get("/search/{title}", response_model=List[Recipe], tags=["Recipes"])
def search_recipe(title: str):
    """Search a recipe by title or contains in title"""
    search_result = recipe_search(title)
    if not search_result:
        return []
    return search_result


@main_router.post(
    "/{recipe_id}/ingredients",
    response_model=Ingredient,
    status_code=201,
    tags=["Ingredients"],
)
def add_ingredient(ingredient: IngredientCreate, recipe_id: int):
    """Add an ingredient to a recipe"""
    return ingredient_create(ingredient, recipe_id)


@main_router.get(
    "/{recipe_id}/ingredients", response_model=List[Ingredient], tags=["Ingredients"]
)
def get_ingredients(recipe_id: int):
    """Get all ingredients from a recipe"""
    ingredients = ingredient_get_by_recipe(recipe_id)
    if not ingredients:
        return []
    return ingredients


@main_router.get(
    "/{recipe_id}/ingredients/{ingredient_id}",
    response_model=Ingredient,
    tags=["Ingredients"],
)
def get_ingredient(ingredient_id: int, recipe_id: int):
    """Get an ingredient from a recipe"""
    ingredient = ingredient_get_by_id(ingredient_id, recipe_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@main_router.put(
    "/{recipe_id}/ingredients/{ingredient_id}",
    response_model=Ingredient,
    tags=["Ingredients"],
)
def update_ingredient(ingredient_id: int, ingredient: IngredientUpdate, recipe_id: int):
    """Update an ingredient from a recipe"""
    ingredient_update(ingredient, ingredient_id, recipe_id)
    updated_ingredient = ingredient_get_by_id(ingredient_id, recipe_id)
    return updated_ingredient


@main_router.delete(
    "/{recipe_id}/ingredients/{ingredient_id}", status_code=200, tags=["Ingredients"]
)
def delete_ingredient(ingredient_id: int, recipe_id: int):
    """Delete an ingredient from a recipe"""
    if ingredient_delete(ingredient_id, recipe_id):
        return {"message": "Ingredient deleted successfully"}
    raise HTTPException(status_code=404, detail="Ingredient not found")


@main_router.post(
    "/{recipe_id}/steps", response_model=Step, status_code=201, tags=["Steps"]
)
def add_step(step: StepCreate, recipe_id: int):
    """Add a step to a recipe"""
    new_step = step_create(step, recipe_id)
    return new_step


@main_router.delete("/{recipe_id}/steps/{step_id}", status_code=200, tags=["Steps"])
def delete_step(step_id: int, recipe_id: int):
    """Delete a step from a recipe"""
    if step_delete(step_id, recipe_id):
        return {"message": "Step deleted successfully"}
    raise HTTPException(status_code=404, detail="Step not found")


@main_router.put("/{recipe_id}/steps/{step_id}", response_model=Step, tags=["Steps"])
def update_step(step_id: int, step: StepUpdate, recipe_id: int):
    """Update a step from a recipe"""
    step_update(step, step_id, recipe_id)
    updated_step = step_get_by_id(step_id, recipe_id)
    return updated_step


@main_router.get("/{recipe_id}/steps/{step_id}", response_model=Step, tags=["Steps"])
def get_step(step_id: int, recipe_id: int):
    """Get a step from a recipe"""
    step = step_get_by_id(step_id, recipe_id)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    return step


@main_router.get("/{recipe_id}/steps", response_model=List[Step], tags=["Steps"])
def get_steps(recipe_id: int):
    """Get all steps from a recipe in order"""
    steps = step_get_all_ordered(recipe_id)
    if not steps:
        return []
    return steps


@main_router.put(
    "/{recipe_id}/steps/{step_01_id}/swap/{step_02_id}", status_code=200, tags=["Steps"]
)
def swap_steps(step_01_id: int, step_02_id: int, recipe_id: int):
    """Swap two steps from a recipe"""
    return step_swap(recipe_id=recipe_id, step_01_id=step_01_id, step_02_id=step_02_id)
