from src.config.database import DBConnectionHandler
from src.models import Recipe, Step
from src.schemas import StepCreate, StepUpdate

# Funções para manipular os passos


def step_create(step: StepCreate, recipe_id: int):
    """Método para criar um passo"""

    try:
        with DBConnectionHandler() as db_connection:
            # Busca a receita
            recipe = db_connection.session.query(Recipe).filter_by(id=recipe_id).first()

            # Se não existir a receita, retorna None
            if not recipe:
                return None

            steps = recipe.steps

            # Se não existir nenhum passo, cria o primeiro passo
            if not steps:
                new_step = Step(
                    title=step.title,
                    description=step.description,
                    recipe_id=recipe_id,
                )
                db_connection.session.add(new_step)
                db_connection.session.commit()
                db_connection.session.refresh(new_step)
                return new_step

            # Se existir apenas um passo, cria o segundo passo
            elif len(steps) == 1:
                new_step = Step(
                    title=step.title,
                    description=step.description,
                    recipe_id=recipe_id,
                    prev_step=steps[0].id,
                )
                db_connection.session.add(new_step)
                first_step = steps[0]
                db_connection.session.refresh(first_step)
                first_step.next_step = new_step.id
                db_connection.session.commit()
                db_connection.session.refresh(new_step)
                return new_step

            # Se existir mais de um passo, cria o próximo passo
            else:
                last_step = None
                for s in steps:
                    if s.next_step is None:
                        last_step = s
                        break

                new_step = Step(
                    title=step.title,
                    description=step.description,
                    recipe_id=recipe_id,
                    prev_step=last_step.id,
                )

                db_connection.session.add(new_step)
                db_connection.session.refresh(last_step)
                last_step.next_step = new_step.id
                db_connection.session.commit()
                db_connection.session.refresh(new_step)
                return new_step

    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def step_delete(step_id: int, recipe_id: int):
    """Método para deletar um passo"""

    try:
        with DBConnectionHandler() as db_connection:
            # Busca a receita
            recipe = db_connection.session.query(Recipe).filter_by(id=recipe_id).first()

            # Se não existir a receita, retorna None
            if not recipe:
                return None

            steps = recipe.steps

            # Se não existir nenhum passo, retorna None
            if not steps:
                return None

            # Se existir apenas um passo, deleta o passo
            elif len(steps) == 1:
                deleted_step = steps[0]
                db_connection.session.refresh(deleted_step)
                db_connection.session.delete(deleted_step)
                db_connection.session.commit()
                return True

            # Se existir mais de um passo, deleta o passo
            elif len(steps) == 2:
                # Se o passo a ser deletado for o primeiro passo
                if steps[0].id == step_id and steps[0].next_step == steps[1].id:
                    remaining_step = steps[1]
                    db_connection.session.refresh(remaining_step)
                    remaining_step.prev_step = None
                    deleted_step = steps[0]
                    db_connection.session.refresh(deleted_step)
                    db_connection.session.delete(deleted_step)
                    db_connection.session.commit()
                    return True

                # Se o passo a ser deletado for o segundo passo
                elif steps[1].id == step_id and steps[1].prev_step == steps[0].id:
                    remaining_step = steps[0]
                    db_connection.session.refresh(remaining_step)
                    remaining_step.next_step = None
                    deleted_step = steps[1]
                    db_connection.session.refresh(deleted_step)
                    db_connection.session.delete(deleted_step)
                    db_connection.session.commit()
                    return True

                else:
                    return False

            else:
                step_to_delete = None

                for step in range(len(steps)):
                    if steps[step].id == step_id:
                        step_to_delete = steps[step]
                        break

                db_connection.session.refresh(step_to_delete)
                # Se o passo a ser deletado for o primeiro passo
                if step_to_delete.prev_step is None:
                    next_step = None
                    for step in range(len(steps)):
                        if steps[step].id == step_to_delete.next_step:
                            next_step = steps[step]
                            break

                    db_connection.session.refresh(next_step)
                    next_step.prev_step = None
                    db_connection.session.delete(step_to_delete)
                    db_connection.session.commit()
                    db_connection.session.refresh(next_step)
                    return True

                # Se o passo a ser deletado for o último passo
                elif step_to_delete.next_step is None:
                    prev_step = None
                    for step in range(len(steps)):
                        if steps[step].id == step_to_delete.prev_step:
                            prev_step = steps[step]
                            break

                    db_connection.session.refresh(prev_step)
                    prev_step.next_step = None
                    db_connection.session.delete(step_to_delete)
                    db_connection.session.commit()
                    db_connection.session.refresh(prev_step)
                    return True

                # Se o passo a ser deletado for um passo intermediário
                else:
                    prev_step = None
                    for step in range(len(steps)):
                        if steps[step].id == step_to_delete.prev_step:
                            prev_step = steps[step]
                            break

                    next_step = None
                    for step in range(len(steps)):
                        if steps[step].id == step_to_delete.next_step:
                            next_step = steps[step]
                            break

                    db_connection.session.refresh(prev_step)
                    db_connection.session.refresh(next_step)
                    prev_step.next_step = next_step.id
                    next_step.prev_step = prev_step.id
                    db_connection.session.delete(step_to_delete)
                    db_connection.session.commit()
                    db_connection.session.refresh(prev_step)
                    db_connection.session.refresh(next_step)
                    return True

    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def step_update(step: StepUpdate, step_id: int, recipe_id: int):
    """Método para atualizar um passo"""

    try:
        with DBConnectionHandler() as db_connection:
            # Busca a receita
            updated_step = (
                db_connection.session.query(Step)
                .filter_by(id=step_id, recipe_id=recipe_id)
                .first()
            )

            # Se não existir a receita, retorna None
            if not updated_step:
                return None

            # Atualiza os dados do passo
            updated_step.title = step.title
            updated_step.description = step.description

            db_connection.session.commit()
            db_connection.session.refresh(updated_step)

            return updated_step

    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def step_get_by_id(step_id: int, recipe_id: int):
    """Método para buscar um passo"""

    try:
        with DBConnectionHandler() as db_connection:
            # Busca a receita
            step = (
                db_connection.session.query(Step)
                .filter_by(id=step_id, recipe_id=recipe_id)
                .first()
            )

            # Se não existir a receita, retorna None
            if not step:
                return None

            return step

    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def step_get_all_ordered(recipe_id: int):
    """Método para buscar todos os passos de uma receita"""

    try:
        with DBConnectionHandler() as db_connection:
            # Busca a receita
            recipe = db_connection.session.query(Recipe).filter_by(id=recipe_id).first()

            # Se não existir a receita, retorna None
            if not recipe:
                return None

            steps = recipe.steps

            # Se não existir nenhum passo, retorna None
            if not steps:
                return None

            if len(steps) == 1:
                return steps

            first_step = None
            for step in steps:
                if step.prev_step is None:
                    first_step = step
                    break

            last_step = None
            for step in steps:
                if step.next_step is None:
                    last_step = step
                    break

            db_connection.session.refresh(first_step)
            db_connection.session.refresh(last_step)

            if len(steps) == 2:
                return [first_step, last_step]

            else:
                ordered_steps = []
                ordered_steps.append(first_step)

                current_step = first_step
                next_step = None

                while True:
                    for step in steps:
                        if step.id == current_step.next_step:
                            next_step = step
                            break

                    db_connection.session.refresh(next_step)

                    ordered_steps.append(next_step)

                    if next_step.next_step is None:
                        break

                    current_step = next_step

                return ordered_steps

    except Exception as e:
        db_connection.session.rollback()
        raise e
    finally:
        db_connection.session.close()


def step_swap(recipe_id: int, step_01_id: int, step_02_id: int):
    """Método para trocar a ordem de dois passos"""

    try:
        with DBConnectionHandler() as db_connection:
            # Busca a receita
            recipe = db_connection.session.query(Recipe).filter_by(id=recipe_id).first()

            # Se não existir a receita, retorna None
            if not recipe:
                return None

            steps = recipe.steps

            # Se não existir nenhum passo, retorna None
            if not steps:
                return None

            # Se existir apenas um passo, retorna True
            if len(steps) == 1:
                return True

            step_01 = None
            for step in steps:
                if step.id == step_01_id:
                    step_01 = step
                    break

            step_02 = None
            for step in steps:
                if step.id == step_02_id:
                    step_02 = step
                    break

            db_connection.session.refresh(step_01)
            db_connection.session.refresh(step_02)

            step_01_next_step = step_01.next_step
            step_01_prev_step = step_01.prev_step
            step_02_next_step = step_02.next_step
            step_02_prev_step = step_02.prev_step

            # Se os passos forem vizinhos
            if step_01_next_step == step_02_id or step_01_prev_step == step_02_id:
                # Se o passo 01 for o primeiro passo
                if step_01_prev_step is None:
                    step_01.next_step = step_02_next_step
                    step_02.prev_step = None
                    step_02.next_step = step_01_id
                    step_01.prev_step = step_02_id

                    next_step = None
                    for step in steps:
                        if step.id == step_01.next_step:
                            next_step = step
                            break

                    db_connection.session.refresh(next_step)
                    next_step.prev_step = step_01_id

                # Se o passo 02 for o primeiro passo
                elif step_02_prev_step is None:
                    step_02.next_step = step_01_next_step
                    step_01.prev_step = None
                    step_01.next_step = step_02_id
                    step_02.prev_step = step_01_id

                    next_step = None
                    for step in steps:
                        if step.id == step_02.next_step:
                            next_step = step
                            break

                    db_connection.session.refresh(next_step)
                    next_step.prev_step = step_02_id

                # Se o passo 01 for o último passo
                elif step_01_next_step is None:
                    step_01.prev_step = step_02_prev_step
                    step_02.next_step = None
                    step_02.prev_step = step_01_id
                    step_01.next_step = step_02_id

                    prev_step = None
                    for step in steps:
                        if step.id == step_01.prev_step:
                            prev_step = step
                            break

                    db_connection.session.refresh(prev_step)
                    prev_step.next_step = step_01_id

                # Se o passo 02 for o último passo
                elif step_02_next_step is None:
                    step_02.prev_step = step_01_prev_step
                    step_01.next_step = None
                    step_01.prev_step = step_02_id
                    step_02.next_step = step_01_id

                    prev_step = None
                    for step in steps:
                        if step.id == step_02.prev_step:
                            prev_step = step
                            break

                    db_connection.session.refresh(prev_step)
                    prev_step.next_step = step_02_id

                # Se os passos forem vizinhos e não forem o primeiro ou o último passo
                elif step_01_next_step == step_02_id:
                    step_01.next_step = step_02_next_step
                    step_01.prev_step = step_02_id
                    step_02.prev_step = step_01_prev_step
                    step_02.next_step = step_01_id

                    next_step = None
                    for step in steps:
                        if step.id == step_01.next_step:
                            next_step = step
                            break

                    db_connection.session.refresh(next_step)
                    next_step.prev_step = step_01_id

                    prev_step = None
                    for step in steps:
                        if step.id == step_02.prev_step:
                            prev_step = step
                            break

                    db_connection.session.refresh(prev_step)
                    prev_step.next_step = step_02_id

                else:
                    step_01.prev_step = step_02_prev_step
                    step_01.next_step = step_02_id
                    step_02.prev_step = step_01_id
                    step_02.next_step = step_01_next_step

                    next_step = None
                    for step in steps:
                        if step.id == step_02.next_step:
                            next_step = step
                            break

                    db_connection.session.refresh(next_step)
                    next_step.prev_step = step_02_id

                    prev_step = None
                    for step in steps:
                        if step.id == step_01.prev_step:
                            prev_step = step
                            break

                    db_connection.session.refresh(prev_step)
                    prev_step.next_step = step_01_id

            # Se os passos não forem vizinhos
            else:
                # Se o passo 01 for o primeiro passo e o passo 02 for intermediário
                if (
                    step_01_prev_step is None
                    and step_02_next_step is not None
                    and step_02_prev_step is not None
                ):
                    step_01.next_step = step_02_next_step
                    step_01.prev_step = step_02_prev_step
                    step_02.prev_step = None
                    step_02.next_step = step_01_next_step

                    step_01_next_step_real = None
                    for step in steps:
                        if step.id == step_01.next_step:
                            step_01_next_step_real = step
                            break

                    db_connection.session.refresh(step_01_next_step_real)
                    step_01_next_step_real.prev_step = step_01_id

                    step_01_prev_step_real = None
                    for step in steps:
                        if step.id == step_01.prev_step:
                            step_01_prev_step_real = step
                            break

                    db_connection.session.refresh(step_01_prev_step_real)
                    step_01_prev_step_real.next_step = step_01_id

                    step_02_next_step_real = None
                    for step in steps:
                        if step.id == step_02.next_step:
                            step_02_next_step_real = step
                            break

                    db_connection.session.refresh(step_02_next_step_real)
                    step_02_next_step_real.prev_step = step_02_id

                # Se o passo 02 for o primeiro passo e o passo 01 for intermediário
                elif (
                    step_02_prev_step is None
                    and step_01_next_step is not None
                    and step_01_prev_step is not None
                ):
                    step_02.next_step = step_01_next_step
                    step_02.prev_step = step_01_prev_step
                    step_01.prev_step = None
                    step_01.next_step = step_02_next_step

                    step_02_next_step_real = None
                    for step in steps:
                        if step.id == step_02.next_step:
                            step_02_next_step_real = step
                            break

                    db_connection.session.refresh(step_02_next_step_real)
                    step_02_next_step_real.prev_step = step_02_id

                    step_02_prev_step_real = None
                    for step in steps:
                        if step.id == step_02.prev_step:
                            step_02_prev_step_real = step
                            break

                    db_connection.session.refresh(step_02_prev_step_real)
                    step_02_prev_step_real.next_step = step_02_id

                    step_01_next_step_real = None
                    for step in steps:
                        if step.id == step_01.next_step:
                            step_01_next_step_real = step
                            break

                    db_connection.session.refresh(step_01_next_step_real)
                    step_01_next_step_real.prev_step = step_01_id

                # Se o passo 01 for o último passo e o passo 02 for intermediário
                elif (
                    step_01_next_step is None
                    and step_02_next_step is not None
                    and step_02_prev_step is not None
                ):
                    step_01.prev_step = step_02_prev_step
                    step_01.next_step = step_02.next_step
                    step_02.prev_step = step_01_prev_step
                    step_02.next_step = None

                    step_01_prev_step_real = None
                    for step in steps:
                        if step.id == step_01.prev_step:
                            step_01_prev_step_real = step
                            break

                    db_connection.session.refresh(step_01_prev_step_real)
                    step_01_prev_step_real.next_step = step_01_id

                    step_01_next_step_real = None
                    for step in steps:
                        if step.id == step_01.next_step:
                            step_01_next_step_real = step
                            break

                    db_connection.session.refresh(step_01_next_step_real)
                    step_01_next_step_real.prev_step = step_01_id

                    step_02_prev_step_real = None
                    for step in steps:
                        if step.id == step_02.prev_step:
                            step_02_prev_step_real = step
                            break

                    db_connection.session.refresh(step_02_prev_step_real)
                    step_02_prev_step_real.next_step = step_02_id

                # Se o passo 02 for o último passo e o passo 01 for intermediário
                elif (
                    step_02_next_step is None
                    and step_01_next_step is not None
                    and step_01_prev_step is not None
                ):
                    step_02.prev_step = step_01_prev_step
                    step_02.next_step = step_01.next_step
                    step_01.prev_step = step_02_prev_step
                    step_01.next_step = None

                    step_02_prev_step_real = None
                    for step in steps:
                        if step.id == step_02.prev_step:
                            step_02_prev_step_real = step
                            break

                    db_connection.session.refresh(step_02_prev_step_real)
                    step_02_prev_step_real.next_step = step_02_id

                    step_02_next_step_real = None
                    for step in steps:
                        if step.id == step_02.next_step:
                            step_02_next_step_real = step
                            break

                    db_connection.session.refresh(step_02_next_step_real)
                    step_02_next_step_real.prev_step = step_02_id

                    step_01_prev_step_real = None
                    for step in steps:
                        if step.id == step_01.prev_step:
                            step_01_prev_step_real = step
                            break

                    db_connection.session.refresh(step_01_prev_step_real)
                    step_01_prev_step_real.next_step = step_01_id

                # Se o passo 01 for o primeiro passo e o passo 02 for o último passo
                elif step_01_prev_step is None and step_02_next_step is None:
                    step_01.next_step = None
                    step_02.prev_step = None
                    step_01.prev_step = step_02_prev_step
                    step_02.next_step = step_01_next_step

                    step_01_prev_step_real = None
                    for step in steps:
                        if step.id == step_01.prev_step:
                            step_01_prev_step_real = step
                            break

                    db_connection.session.refresh(step_01_prev_step_real)
                    step_01_prev_step_real.next_step = step_01_id

                    step_02_next_step_real = None
                    for step in steps:
                        if step.id == step_02.next_step:
                            step_02_next_step_real = step
                            break

                    db_connection.session.refresh(step_02_next_step_real)
                    step_02_next_step_real.prev_step = step_02_id

                # Se o passo 02 for o primeiro passo e o passo 01 for o último passo
                elif step_02_prev_step is None and step_01_next_step is None:
                    step_02.next_step = None
                    step_01.prev_step = None
                    step_02.prev_step = step_01_prev_step
                    step_01.next_step = step_02_next_step

                    step_02_prev_step_real = None
                    for step in steps:
                        if step.id == step_02.prev_step:
                            step_02_prev_step_real = step
                            break

                    db_connection.session.refresh(step_02_prev_step_real)
                    step_02_prev_step_real.next_step = step_02_id

                    step_01_next_step_real = None
                    for step in steps:
                        if step.id == step_01.next_step:
                            step_01_next_step_real = step
                            break

                    db_connection.session.refresh(step_01_next_step_real)
                    step_01_next_step_real.prev_step = step_01_id

                # Se o passo 01 for o primeiro passo e o passo 02 for intermediário
                else:
                    step_01.next_step = step_02_next_step
                    step_01.prev_step = step_02_prev_step
                    step_02.prev_step = step_01_prev_step
                    step_02.next_step = step_01_next_step

                    step_01_prev_step_real = None
                    for step in steps:
                        if step.id == step_01.prev_step:
                            step_01_prev_step_real = step
                            break

                    db_connection.session.refresh(step_01_prev_step_real)
                    step_01_prev_step_real.next_step = step_01_id

                    step_01_next_step_real = None
                    for step in steps:
                        if step.id == step_01.next_step:
                            step_01_next_step_real = step
                            break

                    db_connection.session.refresh(step_01_next_step_real)
                    step_01_next_step_real.prev_step = step_01_id

                    step_02_prev_step_real = None
                    for step in steps:
                        if step.id == step_02.prev_step:
                            step_02_prev_step_real = step
                            break

                    db_connection.session.refresh(step_02_prev_step_real)
                    step_02_prev_step_real.next_step = step_02_id

                    step_02_next_step_real = None
                    for step in steps:
                        if step.id == step_02.next_step:
                            step_02_next_step_real = step
                            break

                    db_connection.session.refresh(step_02_next_step_real)
                    step_02_next_step_real.prev_step = step_02_id

                db_connection.session.commit()

                return True

    except Exception as e:
        db_connection.session.rollback()
        raise e

    finally:
        db_connection.session.close()
