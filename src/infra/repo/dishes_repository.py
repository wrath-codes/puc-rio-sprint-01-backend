from typing import List

from sqlalchemy.orm.exc import NoResultFound

from src.domain.models import Dishes
from src.infra.config.database import DBConnectionHandler
from src.infra.entities import Dishes as DishesModel


class DishesRepository:
    """Class to manage the Dishes Repository"""

    @classmethod
    def insert_dish(cls, name: str, description: str, price: int) -> Dishes:
        """Insert a new dish in the database
        :params - name: str
                - description: str
                - price: int
        :return - Dishes
        """

        with DBConnectionHandler() as db_conn:
            try:
                new_dish = DishesModel(name=name, description=description, price=price)
                db_conn.session.add(new_dish)
                db_conn.session.commit()
                return Dishes(
                    id=new_dish.id,
                    name=new_dish.name,
                    description=new_dish.description,
                    price=new_dish.price,
                )
            except:
                db_conn.session.rollback()
                raise
            finally:
                db_conn.session.close()
            return None

    @classmethod
    def select_dish(cls, dish_id: int = None, dish_name: str = None) -> List[Dishes]:
        """Select dishes from the database
        :params - dish_id: int
                - dish_name: str
        :return - List[Dishes]
        """

        try:
            query_data = None

            if dish_id and not dish_name:
                with DBConnectionHandler() as db_conn:
                    data = (
                        db_conn.session.query(DishesModel).filter_by(id=dish_id).one()
                    )
                    query_data = [data]
            elif not dish_id and dish_name:
                with DBConnectionHandler() as db_conn:
                    data = (
                        db_conn.session.query(DishesModel)
                        .filter_by(name=dish_name)
                        .all()
                    )
                    query_data = data
            elif dish_id and dish_name:
                with DBConnectionHandler() as db_conn:
                    data = (
                        db_conn.session.query(DishesModel)
                        .filter_by(id=dish_id, name=dish_name)
                        .one()
                    )
                    query_data = [data]
            else:
                with DBConnectionHandler() as db_conn:
                    data = db_conn.session.query(DishesModel).all()
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
    def update_dish(
        cls,
        dish_id: int = None,
        dish_name: str = None,
        dish_description: str = None,
        dish_price: int = None,
    ) -> Dishes:
        """Update a dish from the database
        :params - dish_id: int
                - dish_name: str
                - dish_description: str
                - dish_price: int
        :return - Dishes
        """

        with DBConnectionHandler() as db_conn:
            try:
                dish = db_conn.session.query(DishesModel).filter_by(id=dish_id).one()
                if dish_name:
                    dish.name = dish_name
                if dish_description:
                    dish.description = dish_description
                if dish_price:
                    dish.price = dish_price
                db_conn.session.commit()
                return dish
            except:
                db_conn.session.rollback()
                raise
            finally:
                db_conn.session.close()

    @classmethod
    def delete_dish(cls, dish_id: int) -> None:
        """Delete a dish from the database
        :params - dish_id: int
        :return - None
        """

        with DBConnectionHandler() as db_conn:
            try:
                dish = db_conn.session.query(DishesModel).filter_by(id=dish_id).one()
                db_conn.session.delete(dish)
                db_conn.session.commit()
            except:
                db_conn.session.rollback()
                raise
            finally:
                db_conn.session.close()
