from flask import Flask
from . import auth
from flask_bootstrap import Bootstrap
from app.config import config

from flask_pymongo import PyMongo
__db = None

def create_app():    
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    
    Config = config()
    app.config.from_object(config)
    app.register_blueprint(auth)
    _start_db(app)

    return app

def _start_db(app):
    global __db
    mongo = PyMongo(app)
    __db = mongo.db

def database():
    return __db