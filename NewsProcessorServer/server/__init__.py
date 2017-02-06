from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config') #get the config from the config.py file
db = SQLAlchemy(app)

from server import views, models