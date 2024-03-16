from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Animals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(200), nullable=False)
    kind = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(200), nullable=False)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    login = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Integer, nullable=False)
