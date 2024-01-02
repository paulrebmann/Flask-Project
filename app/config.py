import os

class Config(object):
    SQLALCHEMY_DATABASE_URL = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
