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


def connect_to_db(app, db_uri=None):
    """ Connect application to database """
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgres:///youmate'
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    print "Successful Connected to database"