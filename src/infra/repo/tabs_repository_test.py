# flake8: noqa: E501
from faker import Faker
from sqlalchemy import text

from src.infra.config.database import DBConnectionHandler
from src.infra.entities import Tabs as TabsModel
from src.infra.entities.tabs import StatusTab
from src.infra.repo import TabsRepository

fake = Faker()
tabs_repository = TabsRepository()
db_conn_handler = DBConnectionHandler()


def test_insert_tab():
    """Should test Insert Tab"""

    status = "OPEN"
    customer_id = fake.random_number(digits=2)

    engine = db_conn_handler.get_engine()

    # SQL Commands
    new_tab = tabs_repository.insert_tab(status, customer_id)

    with engine.connect() as conn:
        query_tab = conn.execute(
            text("SELECT * FROM tabs WHERE id = {}".format(new_tab.id))
        ).fetchone()

    # Testing
    assert new_tab.id == query_tab.id
    assert new_tab.status.value == query_tab.status
    assert new_tab.customer_id == query_tab.customer_id

    # Cleaning
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM tabs WHERE id = {}".format(new_tab.id)))
        conn.commit()


def test_select_tab():
    """Should test Select Tab"""

    tab_id = fake.random_number(digits=2)
    status = "OPEN"
    customer_id = fake.random_number(digits=2)

    status_mock = StatusTab(status)

    data = TabsModel(
        id=tab_id,
        status=status_mock,
        customer_id=customer_id,
    )

    engine = db_conn_handler.get_engine()

    # SQL Commands
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO tabs (id, status, customer_id) VALUES ({}, '{}', {})".format(
                    tab_id, status, customer_id
                )
            )
        )
        conn.commit()

    # Testing
    tab_01 = tabs_repository.select_tab(tab_id=tab_id)
    tab_02 = tabs_repository.select_tab(tab_status=status)
    tab_03 = tabs_repository.select_tab(tab_customer_id=customer_id)
    tab_04 = tabs_repository.select_tab(tab_status=status, tab_customer_id=customer_id)

    assert data in tab_01
    assert data in tab_02
    assert data in tab_03
    assert data in tab_04

    # Cleaning
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM tabs WHERE id = {}".format(tab_id)))
        conn.commit()


def test_update_tab():
    """Should test Update Tab"""

    tab_id = fake.random_number(digits=2)
    status = "OPEN"
    customer_id = fake.random_number(digits=2)

    status2 = "CLOSED"
    customer_id2 = fake.random_number(digits=2)

    engine = db_conn_handler.get_engine()

    # SQL Commands
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO tabs (id, status, customer_id) VALUES ({}, '{}', {})".format(
                    tab_id, status, customer_id
                )
            )
        )
        conn.commit()

    # Testing
    tabs_repository.update_tab(tab_id=tab_id, status=status2, customer_id=customer_id2)

    with engine.connect() as conn:
        query_tab = conn.execute(
            text("SELECT * FROM tabs WHERE id = {}".format(tab_id))
        ).fetchone()

    assert tab_id == query_tab.id
    assert status2 == query_tab.status
    assert customer_id2 == query_tab.customer_id

    # Cleaning
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM tabs WHERE id = {}".format(tab_id)))
        conn.commit()


def test_delete_tab():
    """Should test Delete Tab"""

    tab_id = fake.random_number(digits=2)
    status = "OPEN"
    customer_id = fake.random_number(digits=2)

    engine = db_conn_handler.get_engine()

    # SQL Commands
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO tabs (id, status, customer_id) VALUES ({}, '{}', {})".format(
                    tab_id, status, customer_id
                )
            )
        )
        conn.commit()

    # Testing
    tabs_repository.delete_tab(tab_id=tab_id)

    with engine.connect() as conn:
        query_tab = conn.execute(
            text("SELECT * FROM tabs WHERE id = {}".format(tab_id))
        ).fetchone()

    assert query_tab is None

    # Cleaning
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM tabs WHERE id = {}".format(tab_id)))
        conn.commit()
