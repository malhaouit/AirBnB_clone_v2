#!/usr/bin/python3
"""Database storage module"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        MYSQL_USER = getenv('HBNB_MYSQL_USER')
        MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        MYSQL_DB = getenv('HBNB_MYSQL_DB')
        connection_string = (
                f'mysql+mysqldb://{MYSQL_USER}:{MYSQL_PWD}'
                f'@{MYSQL_HOST}/{MYSQL_DB}'
                )
        self.__engine = create_engine(connection_string, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects depending on the class name"""
        all_objects = {}
        if cls:
            for obj in self.__session.query(cls).all():
                key = '{}.{}'.format(cls.__name__, obj.id)
                all_objects[key] = obj
        else:
            classes = [State, City]
            for cls in classes:
                for obj in self.__session.query(cls).all():
                    key = '{}.{}'.format(cls.__name__, obj.id)
                    all_objects[key] = obj
        return all_objects

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False
                )
        Session = scoped_session(session_factory)
        self.__session = Session()
