from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:
    """SQLAlchemy database connection handler"""

    def __init__(self) -> None:
        self.__connection_string = "sqlite:///db.sqlite3"
        self.session = None

    def get_engine(self):
        """Return connection engine
        :param: None
        :return: engine connection to database
        """
        engine = create_engine(self.__connection_string)
        return engine

    def __enter__(self):
        engine = create_engine(self.__connection_string)
        session_maker = sessionmaker(bind=engine)
        self.session = session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
