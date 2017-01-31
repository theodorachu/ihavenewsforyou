from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config') # Set the config file
db = SQLAlchemy(app)

from server import views, models