from .__init__ import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    #creates User model for data base entries
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
