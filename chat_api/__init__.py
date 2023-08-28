from flask import Flask
from .pages import *
from .auth import *
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

#login database
db = SQLAlchemy()
DB_NAME = "user_data.db"

from .db_models import *

def get_db():
   global db

   if db is None: # creates db if it does not exist
      db = SQLAlchemy()

   return db


def create_app():

   # intializing Flask
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'jdvbonfewhf ewfwepuihfnv'


   # configuring db with Flask
   app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
   db.init_app(app)
   #registers the two files that contain the Flask blueprints
   app.register_blueprint(pages, url_prefix='/')
   app.register_blueprint(auth, url_prefix='/')

   create_db(app)

   #setting up Flask Login
   login_manager = LoginManager()
   login_manager.login_view = 'auth.login'
   login_manager.init_app(app)

   @login_manager.user_loader
   def load_user(id):
      return User.query.get(int(id)) #returns given user from database

   return app


def create_db(app):
   # creates SQL data base if not already created
   if not os.path.exists('chat_api/' + DB_NAME):
      with app.app_context():
         db.create_all()
