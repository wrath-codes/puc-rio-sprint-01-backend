# flake8: noqa: E501
from faker import Faker
from sqlalchemy import text

from src.infra.config.database import DBConnectionHandler
from src.infra.entities import Dishes as DishesModel
from src.infra.repo import DishesRepository

fake = Faker()
dishes_repository = DishesRepository()
db_conn_handler = DBConnectionHandler()


def test_insert_dish():
    """Should test Insert Dish"""

    name = fake.name()
    description = fake.text()
    price = fake.random_number(digits=2)

    engine = db_conn_handler.get_engine()

    # SQL Commands
    new_dish = dishes_repository.insert_dish(name, description, price)

    with engine.connect() as conn:
        query_dish = conn.execute(
            text("SELECT * FROM dishes WHERE id = {}".format(new_dish.id))
        ).fetchone()

    # Testing
    assert new_dish.id == query_dish.id
    assert new_dish.name == query_dish.name
    assert new_dish.description == query_dish.description
    assert new_dish.price == query_dish.price

    # Cleaning
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM dishes WHERE id = {}".format(new_dish.id)))
        conn.commit()


def test_select_dish():
    """Should test Select Dish"""

    dish_id = fake.random_number(digits=2)
    name = fake.name()
    description = fake.text()
    price = fake.random_number(digits=2)

    data = DishesModel(
        id=dish_id,
        name=name,
        description=description,
        price=price,
    )

    engine = db_conn_handler.get_engine()

    # SQL Commands
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO dishes (id, name, description, price) VALUES ({}, '{}', '{}', {})".format(
                    dish_id, name, description, price
                )
            )
        )
        conn.commit()

    # Testing
    dish_01 = dishes_repository.select_dish(dish_id=dish_id)
    dish_02 = dishes_repository.select_dish(dish_name=name)
    dish_03 = dishes_repository.select_dish(dish_id=dish_id, dish_name=name)
    dish_04 = dishes_repository.select_dish()

    assert data in dish_01
    assert data in dish_02
    assert data in dish_03
    assert data in dish_04

    # Cleaning
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM dishes WHERE id = {}".format(dish_id)))
        conn.commit()


def test_update_dish():
    """Should test Update Dish"""

    dish_id = fake.random_number(digits=2)
    name = fake.name()
    description = fake.text()
    price = fake.random_number(digits=2)

    name2 = fake.name()
    description2 = fake.text()
    price2 = fake.random_number(digits=2)

    engine = db_conn_handler.get_engine()

    # SQL Commands
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO dishes (id, name, description, price) VALUES ({}, '{}', '{}', {})".format(
                    dish_id, name, description, price
                )
            )
        )
        conn.commit()

    # Testing
    dishes_repository.update_dish(
        dish_id=dish_id,
        dish_name=name2,
        dish_description=description2,
        dish_price=price2,
    )

    with engine.connect() as conn:
        query_dish = conn.execute(
            text("SELECT * FROM dishes WHERE id = {}".format(dish_id))
        ).fetchone()

    assert dish_id == query_dish.id
    assert name2 == query_dish.name
    assert description2 == query_dish.description
    assert price2 == query_dish.price

    # Cleaning
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM dishes WHERE id = {}".format(dish_id)))
        conn.commit()


def test_delete_dish():
    """Should test Delete Dish"""

    dish_id = fake.random_number(digits=2)
    name = fake.name()
    description = fake.text()
    price = fake.random_number(digits=2)

    engine = db_conn_handler.get_engine()

    # SQL Commands
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO dishes (id, name, description, price) VALUES ({}, '{}', '{}', {})".format(
                    dish_id, name, description, price
                )
            )
        )
        conn.commit()

    # Testing
    dishes_repository.delete_dish(dish_id=dish_id)

    with engine.connect() as conn:
        query_dish = conn.execute(
            text("SELECT * FROM dishes WHERE id = {}".format(dish_id))
        ).fetchone()

    assert query_dish is None

    # Cleaning
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM dishes WHERE id = {}".format(dish_id)))
        conn.commit()
