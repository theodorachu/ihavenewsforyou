from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS']) #get the config from the config.py file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Nathaniel does not know why or if we need this line
db = SQLAlchemy(app)

from server import views, models