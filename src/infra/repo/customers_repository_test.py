# flake8: noqa: E501
from faker import Faker
from sqlalchemy import text

from src.infra.config.database import DBConnectionHandler
from src.infra.entities import Customers as CustomersModel
from src.infra.repo import CustomersRepository

fake = Faker()
customers_repository = CustomersRepository()
db_conn_handler = DBConnectionHandler()


def test_insert_customer():
    """Should test Insert Customer"""

    name = fake.name()
    phone = fake.phone_number()

    engine = db_conn_handler.get_engine()

    # SQL Commands
    new_customer = customers_repository.insert_customer(name, phone)

    with engine.connect() as conn:
        query_customer = conn.execute(
            text("SELECT * FROM customers WHERE id = {}".format(new_customer.id))
        ).fetchone()

    # Testing
    assert new_customer.id == query_customer.id
    assert new_customer.name == query_customer.name
    assert new_customer.phone == query_customer.phone

    # Cleaning
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM customers WHERE id = {}".format(new_customer.id))
        )
        conn.commit()


def test_select_customer():
    """Should test Select Customer"""

    customer_id = fake.random_number(digits=2)
    name = fake.name()
    phone = fake.phone_number()

    data = CustomersModel(
        id=customer_id,
        name=name,
        phone=phone,
    )

    engine = db_conn_handler.get_engine()

    # SQL Commands
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO customers (id, name, phone) VALUES ({}, '{}', '{}')".format(
                    customer_id, name, phone
                )
            )
        )
        conn.commit()

    # Testing
    customer_01 = customers_repository.select_customer(customer_id=customer_id)
    customer_02 = customers_repository.select_customer(customer_name=name)
    customer_03 = customers_repository.select_customer(customer_phone=phone)
    customer_04 = customers_repository.select_customer()

    assert data in customer_01
    assert data in customer_02
    assert data in customer_03
    assert data in customer_04

    # Cleaning
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM customers WHERE id = {}".format(data.id)))
        conn.commit()


def test_update_customer():
    """Should test Update Customer"""

    customer_id = fake.random_number(digits=2)
    name = fake.name()
    phone = fake.phone_number()

    name_02 = fake.name()
    phone_02 = fake.phone_number()

    engine = db_conn_handler.get_engine()

    # SQL Commands
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO customers (id, name, phone) VALUES ({}, '{}', '{}')".format(
                    customer_id, name, phone
                )
            )
        )
        conn.commit()

    # Testing
    customers_repository.update_customer(
        customer_id=customer_id, name=name_02, phone=phone_02
    )

    with engine.connect() as conn:
        query_customer = conn.execute(
            text("SELECT * FROM customers WHERE id = {}".format(customer_id))
        ).fetchone()

    assert customer_id == query_customer.id
    assert name_02 == query_customer.name
    assert phone_02 == query_customer.phone

    # Cleaning
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM customers WHERE id = {}".format(customer_id)))
        conn.commit()


def test_delete_customer():
    """Should test Delete Customer"""

    customer_id = fake.random_number(digits=2)
    name = fake.name()
    phone = fake.phone_number()

    engine = db_conn_handler.get_engine()

    # SQL Commands
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO customers (id, name, phone) VALUES ({}, '{}', '{}')".format(
                    customer_id, name, phone
                )
            )
        )
        conn.commit()

    # Testing
    customers_repository.delete_customer(customer_id=customer_id)

    with engine.connect() as conn:
        query_customer = conn.execute(
            text("SELECT * FROM customers WHERE id = {}".format(customer_id))
        ).fetchone()

    assert query_customer is None

    # Cleaning
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM customers WHERE id = {}".format(customer_id)))
        conn.commit()
