from flask import Flask, jsonify, request, render_template, make_response
from flask import session as login_session, flash, redirect
import random
import string

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item, Base, User
from config import config

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

# Initialize the app
app = Flask(__name__)
app.config.from_object(config['default'])

# Some constants (following Udacity FSND classroom material)
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"


# Connect to the DB
engine = create_engine('postgresql:///item_catalog')
Base.metadata.bind = engine

# Start DB session
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    """
    Create anti forgery token and display login plage
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, is_login_page=True)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    Deal with response after clicking on the Google Sign-in button
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    email = data['email']
    user = session.query(User).filter_by(email=email).first()
    if user is None:
        print "YO: New user"
        user = User()
        user.email = email
        user.avatar = data['picture']
        user.name = data['name']
        session.add(user)
        session.commit()
    else:
        print "YO: User exists dude, be happy!"

    login_session['username'] = user.name
    login_session['picture'] = user.avatar
    login_session['email'] = user.email

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return redirect('/')


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


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
                           items=items,
                           login_session=login_session)


@app.route('/catalog/<string:category_name>/items')
def category_list(category_name):
    """
    Endpoint for category items
    """
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category=category).all()
    return render_template('category_items.html',
                           category=category,
                           categories=categories,
                           items=items,
                           login_session=login_session)


@app.route('/catalog/<string:category_name>/<string:item_name>')
def item_detail_page(category_name, item_name):
    """
    JSON endpoint for an individual item
    """
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(category=category).filter_by(name=item_name).one()
    return render_template('item_detail.html',
                           item=item,
                           login_session=login_session)


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
