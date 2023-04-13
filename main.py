from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src import schemas, services
from src.config.database import create_db

tags_metadata = [
    {
        "name": "docs",
        "description": "Redirect to docs.",
    },
    {
        "name": "recipes",
        "description": "Operations with recipes.",
    },
    {
        "name": "ingredients",
        "description": "Operations with ingredients.",
    },
    {
        "name": "steps",
        "description": "Operations with steps.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["docs"])
def index():
    """Redirect to docs"""
    docs = RedirectResponse(url="/docs")
    return docs


@app.post("/recipes/", tags=["recipes"], response_model=schemas.Recipe, status_code=201)
def create_recipe(recipe: schemas.RecipeCreate):
    """Create a new recipe"""
    return services.recipe_create(recipe)


@app.get("/recipes/", tags=["recipes"], response_model=List[schemas.Recipe])
def get_recipes():
    """Get all recipes"""
    return services.recipe_get_all()


@app.get("/recipes/{recipe_id}", tags=["recipes"], response_model=schemas.Recipe)
def get_recipe(recipe_id: int):
    """Get a recipe by id"""
    recipe = services.recipe_get_one(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.put("/recipes/{recipe_id}", tags=["recipes"], response_model=schemas.Recipe)
def update_recipe(recipe_id: int, recipe: schemas.RecipeUpdate):
    """Update a recipe by id"""
    return services.recipe_update(recipe, recipe_id)


@app.delete("/recipes/{recipe_id}", tags=["recipes"], status_code=204)
def delete_recipe(recipe_id: int):
    """Delete a recipe by id"""
    services.recipe_delete(recipe_id)


@app.get(
    "/recipes/search/{title}", tags=["recipes"], response_model=List[schemas.Recipe]
)
def search_recipe(title: str):
    """Search a recipe by title or contains in title"""
    return services.recipe_search(title)


@app.post(
    "/recipes/{recipe_id}/ingredients/",
    tags=["ingredients"],
    response_model=schemas.Recipe,
    status_code=201,
)
def add_ingredient(ingredient: schemas.IngredientCreate, recipe_id: int):
    """Add an ingredient to a recipe"""
    return services.ingredient_create(ingredient, recipe_id)


@app.get(
    "/recipes/{recipe_id}/ingredients/",
    tags=["ingredients"],
    response_model=List[schemas.Ingredient],
)
def get_ingredients(recipe_id: int):
    """Get all ingredients from a recipe"""
    return services.ingredient_get_all(recipe_id)


@app.get(
    "/recipes/{recipe_id}/ingredients/{ingredient_id}",
    tags=["ingredients"],
    response_model=schemas.Ingredient,
)
def get_ingredient(ingredient_id: int):
    """Get an ingredient from a recipe"""
    ingredient = services.ingredient_get_by_id(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@app.put(
    "/recipes/{recipe_id}/ingredients/{ingredient_id}",
    tags=["ingredients"],
    response_model=schemas.Ingredient,
)
def update_ingredient(ingredient_id: int, ingredient: schemas.IngredientUpdate):
    """Update an ingredient from a recipe"""
    return services.ingredient_update(ingredient, ingredient_id)


@app.delete(
    "/recipes/{recipe_id}/ingredients/{ingredient_id}",
    tags=["ingredients"],
    status_code=200,
    response_model=schemas.Recipe,
)
def delete_ingredient(ingredient_id: int):
    """Delete an ingredient from a recipe"""
    services.ingredient_delete(ingredient_id)


if __name__ == "__main__":
    create_db()

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
