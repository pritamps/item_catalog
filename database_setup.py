import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


Base = declarative_base()


class Category(Base):
    """
    Definitions for the categories table
    """
    __tablename__ = 'category'
    # Here we define columns for the categories table.
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    description = Column(String(2500))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    @property
    def serialize(self):
        """
        Return dictionary of current category in nice JSON format
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'time_created': self.time_created,
            'time_updated': self.time_updated
        }

    @property
    def serialize_mini(self):
        """
        Return dictionary of current category in nice JSON format
        including only major info
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }


class Item(Base):
    """
    Definitions for the items table
    """
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(2500), nullable=False)
    description = Column(String(250), nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    @property
    def serialize(self):
        """
        Return dictionary of current object in nice JSON format
        """
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.serialize_mini,
            'description': self.description,
            'time_created': self.time_created,
            'time_updated': self.time_updated
        }


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
# db_engine = create_engine('postgresql:///vagrant:vagrant@localhost/item_catalog')
engine = create_engine("postgresql:///item_catalog")
if not database_exists(engine.url):
    create_database(engine.url)


# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)