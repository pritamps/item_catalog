"""
Contains app configuration, including Google OAuth Credentials
Tutorial followed: http://bitwiser.in/2015/09/09/add-google-login-in-flask.html
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Auth:
    """
    Google OAuth specific variables
    """
    CLIENT_ID = ('1052207294010-0h2cfp8u3ktjiqaf04qdm0a4rrfs9rof.'
                 'apps.googleusercontent.com')
    CLIENT_SECRET = 'zgdTvLWBhoLvhK2qyBeUEuqa'
    REDIRECT_URI = 'https://localhost:5000/gauthcallback'
    AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'


class Config:
    DEBUG = False
    APP_NAME = "Test Google Login"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "somethingsecret"
    SQLALCHEMY_DATABASE_URI = 'postgresql:///item_catalog'


config = {
    "default": Config
}
