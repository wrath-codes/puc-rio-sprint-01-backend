# Este arquivo é responsável por popular o banco de dados com dados de teste
# Também pode ser usado para popular o banco de dados com dados caso você não
# queira criar uma lista de receitas manualmente.

from src.config.database import create_db
from src.models import Ingredient, Recipe, Step

# Importa as bibliotecas necessárias
from src.seeder.receitas import receitas
from src.services import ingredient_create, recipe_create, step_create

# Cria uma instância do DBConnectionHandler

# Cria as tabelas no banco de dados
create_db()

# Percorre a lista de receitas
for receita in receitas:
    # Cria uma receita no banco de dados
    recipe = Recipe(
        title=receita["title"],
        description=receita["description"],
    )
    new_recipe = recipe_create(recipe)

    # Percorre a lista de ingredientes da receita
    for ingrediente in receita["ingredients"]:
        # Cria um ingrediente no banco de dados
        ingredient = Ingredient(
            name=ingrediente["name"],
            quantity=ingrediente["quantity"],
            recipe_id=new_recipe.id,
        )
        ingredient_create(ingredient, new_recipe.id)

    # Percorre a lista de passos da receita
    for passo in receita["steps"]:
        # Cria um passo no banco de dados
        step = Step(
            title=passo["title"],
            description=passo["description"],
            recipe_id=new_recipe.id,
        )
        step_create(step, new_recipe.id)
