import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	DEBUG = False
	CSRF_ENABLED = True
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] # required by Flask-SQLAlchemy

class LocalConfig(Config):
	DEBUG = True

class HerokuConfig(Config):
	DEBUG = False
