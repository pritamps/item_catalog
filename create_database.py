import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class Category(Base):
    """
    Definitions for the categories table
    """
    __tablename__ = 'categories'
    # Here we define columns for the categories table.
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    description = Column(String(2500))


class Item(Base):
    """
    Definitions for the items table
    """
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(2500), nullable=False)
    description = Column(String(250), nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    person = relationship(Category)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
db_engine = create_engine('sqlite:///sqlalchemy_example.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(db_engine)