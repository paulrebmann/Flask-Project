#Importing necessary modules and classes from Flask and related extensions
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Creating a Flask web application instance
app = Flask(__name__)

#Configuring the Flask app using settings from the Config class
app.config.from_object(Config)

#Creating an SQLAlchemy database instance, associated with the Flask app
db = SQLAlchemy(app)

#Creating a migration instance for handling database migrations
migrate = Migrate(app, db)

#Importing routes and models from the 'app' package
from app import routes, models