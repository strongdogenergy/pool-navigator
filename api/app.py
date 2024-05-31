import time
import redis
from flask_cors import CORS, cross_origin

# Python standard libraries
import json
import os
import sqlite3

# Third-party libraries
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command, hello_db, init_db
from user import User

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

cache = redis.Redis(host='redis', port=6379)
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get_secure_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('secure_hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
@cross_origin()
def hello():
    count = get_hit_count()
    return {
        "hits": count,
    }

@app.route('/secure')
@cross_origin()
def getSecureHits():
    count = get_hit_count()
    secure_count = get_secure_hit_count()
    return {
        "hits": count,
        "secure_hits": secure_count,
        "client_id": GOOGLE_CLIENT_ID,
    }