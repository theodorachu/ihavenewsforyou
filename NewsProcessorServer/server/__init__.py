from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config.from_object(os.environ['APP_SETTINGS']) #get the config from the config.py file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Nathaniel does not know why or if we need this line
db = SQLAlchemy(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

from server import views, models