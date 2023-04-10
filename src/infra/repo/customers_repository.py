from typing import List

from sqlalchemy.orm.exc import NoResultFound

from src.domain.models import Customers
from src.infra.config.database import DBConnectionHandler
from src.infra.entities import Customers as CustomersModel


class CustomersRepository:
    """Class to manage the Customers Repository"""

    @classmethod
    def insert_customer(cls, name: str, phone: str) -> Customers:
        """Insert a new customer in the database
        :params - name: str
                - phone: str
        :return - Customers
        """

        with DBConnectionHandler() as db_conn:
            try:
                new_customer = CustomersModel(name=name, phone=phone)
                db_conn.session.add(new_customer)
                db_conn.session.commit()
                return Customers(
                    id=new_customer.id, name=new_customer.name, phone=new_customer.phone
                )
            except:
                db_conn.session.rollback()
                raise
            finally:
                db_conn.session.close()
            return None

    @classmethod
    def select_customer(
        cls,
        customer_id: int = None,
        customer_name: str = None,
        customer_phone: str = None,
    ) -> List[Customers]:
        """Select customers from the database
        :params - customer_id: int
                - customer_name: str
                - customer_phone: str
        :return - List[Customers]
        """

        try:
            query_data = None

            if customer_id and not customer_name and not customer_phone:
                with DBConnectionHandler() as db_conn:
                    data = (
                        db_conn.session.query(CustomersModel)
                        .filter_by(id=customer_id)
                        .one()
                    )
                    query_data = [data]
            elif not customer_id and customer_name and not customer_phone:
                with DBConnectionHandler() as db_conn:
                    data = (
                        db_conn.session.query(CustomersModel)
                        .filter_by(name=customer_name)
                        .one()
                    )
                    query_data = [data]
            elif not customer_id and not customer_name and customer_phone:
                with DBConnectionHandler() as db_conn:
                    data = (
                        db_conn.session.query(CustomersModel)
                        .filter_by(phone=customer_phone)
                        .one()
                    )
                    query_data = [data]
            elif not customer_id and not customer_name and not customer_phone:
                with DBConnectionHandler() as db_conn:
                    data = db_conn.session.query(CustomersModel).all()
                    query_data = data

            return query_data

        except NoResultFound:
            return []
        except:
            db_conn.session.rollback()
            raise
        finally:
            db_conn.session.close()
        return None

    @classmethod
    def update_customer(
        cls, customer_id: int, name: str = None, phone: str = None
    ) -> Customers:
        """Update a customer in the database
        :params - customer_id: int
                - name: str
                - phone: str
        :return - Customers
        """

        with DBConnectionHandler() as db_conn:
            try:
                customer = (
                    db_conn.session.query(CustomersModel)
                    .filter_by(id=customer_id)
                    .one()
                )
                if name:
                    customer.name = name
                if phone:
                    customer.phone = phone
                db_conn.session.commit()
                return Customers(
                    id=customer.id, name=customer.name, phone=customer.phone
                )
            except:
                db_conn.session.rollback()
                raise
            finally:
                db_conn.session.close()
            return None

    @classmethod
    def delete_customer(cls, customer_id: int) -> None:
        """Delete a customer from the database
        :params - customer_id: int
        :return - None
        """

        with DBConnectionHandler() as db_conn:
            try:
                customer = (
                    db_conn.session.query(CustomersModel)
                    .filter_by(id=customer_id)
                    .one()
                )
                db_conn.session.delete(customer)
                db_conn.session.commit()
            except:
                db_conn.session.rollback()
                raise
            finally:
                db_conn.session.close()
            return None
