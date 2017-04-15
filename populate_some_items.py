from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from time import sleep

from database_setup import Category, Item, Base, User

engine = create_engine('postgresql:///item_catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user = User(email="pritamps+firstuser@gmail.com", name="God User")

# ---- FANTASY BOOKS BEGIN ----
category_books = Category(name="Fantasy Book Series",
                          description="Some of my favourite fantasy book series",
                          creator=user)

session.add(category_books)
session.commit()
sleep(1)


book1 = Item(name="The Book of the New Sun",
             description="Fantasy series set in a future where the sun is dying out",
             category=category_books,
             creator=user)

session.add(book1)
session.commit()
sleep(1)


book2 = Item(name="The Earthsea Chronicles",
             description="Harry Potter's got nothing on the Earthsea Chronicles",
             category=category_books,
             creator=user)

session.add(book2)
session.commit()

book3 = Item(name="The Golden Compass",
             description="A lovely series of books suitable for both kids and adults",
             category=category_books,
             creator=user)

session.add(book3)
session.commit()
sleep(1)

# ---- FANTASY BOOKS END ----

# ---- SCIFI MOVIES BEGIN ----
category_books = Category(name="Scifi Movies", 
                          description="Some of my favourite SciFi movies",
                          creator=user)

session.add(category_books)
session.commit()
sleep(1)

movie1 = Item(name="The Fifth Element",
              description="Not much science, but a crazy amount of fun",
              category=category_books,
              creator=user)

session.add(movie1)
session.commit()
sleep(1)


movie2 = Item(name="Arrival",
              description="New movie that takes the time to be cool",
              category=category_books,
              creator=user)

session.add(movie2)
session.commit()
# ---- SCIFI MOVIES END ----

print "A few items were added to your little database. Go play now!"
