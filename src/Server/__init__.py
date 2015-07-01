from flask import Flask
from flask.ext.mongoengine import MongoEngine
from pymongo import read_preferences

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

db = MongoEngine()

app.config['MONGODB_SETTINGS'] = {
	'db': 'TML',
	'host': 'localhost',
	'port': 27017,
	'read_preference': read_preferences.ReadPreference.PRIMARY
	#'username': 'T@M53M7534L',
	#'password': 'T@M53M7534L'
}

db.init_app(app)

from src import models
from src import views