from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Animals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    photo = db.Column(db.String(200), nullable=False)
    kind = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(200), nullable=False)
    orders = db.relationship('Orders', backref='animal', lazy=True)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(200), nullable=False)
    name2 = db.Column(db.String(200))
    number = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    login = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    orders = db.relationship('Orders', backref='user', lazy=True)


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    id_animal = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(2000))
    date = db.Column(db.Date(), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    cart_number = db.Column(db.String(200), nullable=False)


class Breeds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_breed = db.Column(db.String(200), nullable=False)
    health = db.Column(db.String(2000), nullable=False)
    activity = db.Column(db.String(2000), nullable=False)
    nutrition = db.Column(db.String(2000), nullable=False)
    grooming = db.Column(db.String(2000), nullable=False)


class Applications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    animal = db.Column(db.String(200), nullable=False)
    number = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date(), nullable=False)