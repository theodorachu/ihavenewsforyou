from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
# from flask_cors import CORS, cross_origin

# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
# from flask_social import Social
# from flask_social.datastore import SQLAlchemyConnectionDatastore

from flask_login import LoginManager, UserMixin

app = Flask(__name__)
# CORS(app)

app.config['SECRET_KEY'] = 'thisisthesecretkey'
app.config.from_object(os.environ['APP_SETTINGS']) #get the config from the config.py file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Nathaniel does not know why or if we need this line

app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '153629798477210',
        'secret': '7aa2a1778d69d1efc359be284dc354aa'
    }
}

db = SQLAlchemy(app)
lm = LoginManager(app)

from server import models, views
from models import User

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

