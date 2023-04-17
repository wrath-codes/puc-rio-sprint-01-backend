from src.config.database import DBConnectionHandler
from src.models import Ingredient, Recipe
from src.schemas import IngredientCreate, IngredientUpdate


# Funções para manipular os ingredientes
def ingredient_get_by_id(ingredient_id: int, recipe_id: int):
    """Método para buscar um ingrediente pelo id"""

    try:
        with DBConnectionHandler() as db_connection:
            ingredient = (
                db_connection.session.query(Ingredient)
                .filter_by(id=ingredient_id, recipe_id=recipe_id)
                .first()
            )

            return ingredient
    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def ingredient_get_by_recipe(recipe_id: int):
    """Método para buscar todos os ingredientes de uma receita"""

    try:
        with DBConnectionHandler() as db_connection:
            ingredients = (
                db_connection.session.query(Ingredient)
                .filter_by(recipe_id=recipe_id)
                .all()
            )
            return ingredients
    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def ingredient_create(ingredient: IngredientCreate, recipe_id: int):
    """Método para criar um ingrediente"""

    new_ingredient = Ingredient(
        name=ingredient.name, quantity=ingredient.quantity, recipe_id=recipe_id
    )
    try:
        with DBConnectionHandler() as db_connection:
            db_connection.session.add(new_ingredient)
            db_connection.session.commit()
            db_connection.session.refresh(new_ingredient)
            return new_ingredient

    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def ingredient_update(ingredient: IngredientUpdate, ingredient_id: int, recipe_id: int):
    """Método para atualizar um ingrediente"""

    try:
        with DBConnectionHandler() as db_connection:
            updated_ingredient = (
                db_connection.session.query(Ingredient)
                .filter_by(id=ingredient_id, recipe_id=recipe_id)
                .first()
            )
            updated_ingredient.name = ingredient.name
            updated_ingredient.quantity = ingredient.quantity
            db_connection.session.commit()
            db_connection.session.refresh(updated_ingredient)
            return ingredient
    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def ingredient_delete(ingredient_id: int, recipe_id: int):
    """Método para deletar um ingrediente"""

    try:
        with DBConnectionHandler() as db_connection:
            deleted_ingredient = (
                db_connection.session.query(Ingredient)
                .filter_by(id=ingredient_id)
                .first()
            )
            recipe = db_connection.session.query(Recipe).filter_by(id=recipe_id).first()
            db_connection.session.delete(deleted_ingredient)
            db_connection.session.commit()
            db_connection.session.refresh(recipe)
            return recipe
    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()
