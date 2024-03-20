# db_connection.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SqlLiteEngine:
    """
    Class to create the connection to the SQLite database

    init_args:
        db: str ["wikipedia", "wikipedia_complete"]  : The name of the database to connect to. Default is 'wikipedia'
        root_folder: str : The root folder of the project where the database URI file is located.

    Attributes:
    db_uri: str: The URI of the database
    engine: create_engine: The engine object for the database
    Session: sessionmaker: The session object for the database

    Methods:
    get_engine: Returns the engine object
    get_session: Returns the session object
    close: Closes the connection to the database
    """
    _instance: None = None  # Singleton instance

    def __new__(cls, db="wikipedia"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_uri = ""
            if db == "wikipedia":
                cls._instance.db_uri = "sqlite:///wikipedia/database/wikipedia.db"
            elif db == "wikipedia_complete":
                cls._instance.db_uri = "sqlite:///wikipedia/database/wikipedia.db"
            else:
                raise ValueError("Invalid database name. Please provide a valid database name")
            cls._instance.engine = create_engine(cls._instance.db_uri, pool_pre_ping=True)
            cls._instance.Session = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=cls._instance.engine,
            )
        return cls._instance

    @classmethod
    def get_engine(cls):
        return cls._instance.engine if cls._instance else None

    def get_session(self):
        return self.Session()

    def close(self):
        self.engine.dispose()
