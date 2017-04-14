from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item, Base

# Initialize the app
app = Flask(__name__)

# Connect to the DB
engine = create_engine('postgresql:///item_catalog')
Base.metadata.bind = engine

# Start DB session
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home_page():
    """
    The main page, i.e. list of categories, and most recently added items
    """
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.time_created.desc()).limit(10)
    # return "This page will show all my restaurants"
    return render_template('landing_page.html',
                           categories=categories,
                           items=items)


@app.route('/catalog/<string:category_name>/items')
def category_json(category_name):
    """
    JSON endpoint an individual category
    """
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category=category).all()
    return render_template('category_items.html',
                           category=category,
                           categories=categories,
                           items=items)


@app.route('/hello')
def hello_world():
    """
    Just a hello world function to get the ball rolling
    """

    categories = session.query(Category).all()
    items = []

    for category in categories:
        id = category.id
        print "ID: " + str(id)
        print "Category: " + str(category.name)
        items.extend(session.query(Item).filter_by(category=category).all())

    return jsonify(list=[i.serialize for i in items])


@app.route('/category/<int:category_id>/item/<int:item_id>/json')
def item_json(category_id, item_id):
    """
    JSON endpoint for an individual item
    """
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(item.serialize)


@app.route('/category/<int:category_id>/items')
def category_items(category_id):
    """
    JSON endpoint for all items in a single category
    """
    items = session.query(Item).filter_by(category_id=category_id).all()


@app.route('/category/<int:category_id>/items/json')
def category_items_json(category_id):
    """
    JSON endpoint for all items in a single category
    """
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(list=[i.serialize for i in items])


if __name__ == '__main__':
    # Enable automatic reloading on code changes
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
