from src.config.database import DBConnectionHandler
from src.models import Recipe
from src.schemas import RecipeCreate, RecipeUpdate


# Funções para manipular as receitas
def recipe_get_one(recipe_id: int):
    """Método para buscar uma receita pelo id"""

    try:
        with DBConnectionHandler() as db_connection:
            recipe = db_connection.session.query(Recipe).filter_by(id=recipe_id).first()
            return recipe
    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def recipe_get_all():
    """Método para buscar todas as receitas"""

    try:
        with DBConnectionHandler() as db_connection:
            recipes = db_connection.session.query(Recipe).order_by(Recipe.title).all()
            return recipes
    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def recipe_create(recipe: RecipeCreate):
    """Método para criar uma receita"""

    new_recipe = Recipe(title=recipe.title, description=recipe.description)
    try:
        with DBConnectionHandler() as db_connection:
            db_connection.session.add(new_recipe)
            db_connection.session.commit()
            db_connection.session.refresh(new_recipe)
            return new_recipe

    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def recipe_update(recipe: RecipeUpdate, recipe_id: int):
    """Método para atualizar uma receita"""

    try:
        with DBConnectionHandler() as db_connection:
            updated_recipe = (
                db_connection.session.query(Recipe).filter_by(id=recipe_id).first()
            )
            updated_recipe.title = recipe.title
            updated_recipe.description = recipe.description

            db_connection.session.commit()
            db_connection.session.refresh(updated_recipe)
            return updated_recipe

    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def recipe_delete(recipe_id: int):
    """Método para deletar uma receita"""

    try:
        with DBConnectionHandler() as db_connection:
            recipe = db_connection.session.query(Recipe).filter_by(id=recipe_id).first()

            ingredients = recipe.ingredients
            steps = recipe.steps

            if ingredients:
                for ingredient in ingredients:
                    db_connection.session.delete(ingredient)

            if steps:
                for step in steps:
                    db_connection.session.delete(step)

            db_connection.session.delete(recipe)
            db_connection.session.commit()
            return True

    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def recipe_search(search: str):
    """Método para buscar receitas por título"""

    try:
        with DBConnectionHandler() as db_connection:
            recipes = (
                db_connection.session.query(Recipe)
                .filter(Recipe.title.ilike(f"%{search}%"))
                .order_by(Recipe.title)
                .all()
            )
            return recipes
    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()
