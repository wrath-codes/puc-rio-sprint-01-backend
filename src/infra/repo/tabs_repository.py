from typing import List

from sqlalchemy.orm.exc import NoResultFound

from src.domain.models import Tabs
from src.infra.config.database import DBConnectionHandler
from src.infra.entities import Tabs as TabsModel


class TabsRepository:
    """Class to manage the Tabs Repository"""

    @classmethod
    def insert_tab(cls, status: str, customer_id: int) -> Tabs:
        """Insert a new tab in the database
        :params - status: str
                - customer_id: int
        :return - Tabs
        """

        with DBConnectionHandler() as db_conn:
            try:
                new_tab = TabsModel(status=status, customer_id=customer_id)
                db_conn.session.add(new_tab)
                db_conn.session.commit()
                return Tabs(
                    id=new_tab.id,
                    status=new_tab.status,
                    customer_id=new_tab.customer_id,
                )
            except:
                db_conn.session.rollback()
                raise
            finally:
                db_conn.session.close()
            return None

    @classmethod
    def select_tab(
        cls,
        tab_id: int = None,
        tab_status: str = None,
        tab_customer_id: int = None,
    ) -> List[Tabs]:
        """Select tabs from the database
        :params - tab_id: int
                - tab_status: str
                - tab_customer_id: int
        :return - List[Tabs]
        """

        try:
            query_data = None

            if tab_id and not tab_status and not tab_customer_id:
                with DBConnectionHandler() as db_conn:
                    data = db_conn.session.query(TabsModel).filter_by(id=tab_id).one()
                    query_data = [data]

            elif not tab_id and tab_status and not tab_customer_id:
                with DBConnectionHandler() as db_conn:
                    data = (
                        db_conn.session.query(TabsModel)
                        .filter_by(status=tab_status)
                        .all()
                    )
                    query_data = data

            elif not tab_id and not tab_status and tab_customer_id:
                with DBConnectionHandler() as db_conn:
                    data = (
                        db_conn.session.query(TabsModel)
                        .filter_by(customer_id=tab_customer_id)
                        .all()
                    )
                    query_data = data

            elif not tab_id and tab_status and tab_customer_id:
                with DBConnectionHandler() as db_conn:
                    data = (
                        db_conn.session.query(TabsModel)
                        .filter_by(status=tab_status)
                        .filter_by(customer_id=tab_customer_id)
                        .all()
                    )
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
    def update_tab(
        cls, tab_id: int, status: str = None, customer_id: int = None
    ) -> Tabs:
        """Update a tab in the database
        :params - tab_id: int
                - status: str
                - customer_id: int
        :return - Tabs
        """

        with DBConnectionHandler() as db_conn:
            try:
                tab = db_conn.session.query(TabsModel).filter_by(id=tab_id).one()
                if status:
                    tab.status = status
                if customer_id:
                    tab.customer_id = customer_id
                db_conn.session.commit()
                return Tabs(id=tab.id, status=tab.status, customer_id=tab.customer_id)
            except:
                db_conn.session.rollback()
                raise
            finally:
                db_conn.session.close()
            return None

    @classmethod
    def delete_tab(cls, tab_id: int) -> None:
        """Delete a tab in the database
        :params - tab_id: int
        :return - None
        """

        with DBConnectionHandler() as db_conn:
            try:
                tab = db_conn.session.query(TabsModel).filter_by(id=tab_id).one()
                db_conn.session.delete(tab)
                db_conn.session.commit()
            except:
                db_conn.session.rollback()
                raise
            finally:
                db_conn.session.close()
            return None
