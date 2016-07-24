""" Models and database function for YouMate"""

# python std libs

# third-part libs
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# connect to database here.
# replace "my_database" with the name of your database 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///youmate'
db = SQLAlchemy()

# All models go here
class User(db.Model):
    """Users model"""

    __tablename__ = "users"

    # Set up the basic info each user will have
    user_id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(30), nullable=False)
    l_name = db.Column(db.String(30), nullable=True)
    # sex = db.Column(db.String(1), nullable=True)
    # dob = db.Column(db.Date, nullable=True)
    # age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    password = db.Column(db.String(30), nullable=True)
    # profile_pic = db.Column(db.Text, default="Koala.jpg")
    # bio = db.Column(db.Text, nullable=True)

class User(db.Model):
    """Users model"""

    __tablename__ = "preferences"

    # Set up the basic info each user will have
    user_id = db.Column(db.Integer, primary_key=True,nullable=False)
    pets = db.Column(db.Boolean, nullable=True)
    queer = db.Column(db.Boolean, nullable=True)
    smoke = db.Column(db.Boolean, nullable=True)
    # sex = db.Column(db.String(1), nullable=True)
    # dob = db.Column(db.Date, nullable=True)
    # age = db.Column(db.Integer, nullable=True)
    tenant_landlord = db.Column(db.String(50), nullable=True, unique=True)
    
def connect_to_db(app, db_uri=None):
    """ Connect application to database """
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgres:///youmate'
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    print("Successful Connected to database")