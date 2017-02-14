import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	DEBUG = False
	CSRF_ENABLED = True
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] # required by Flask-SQLAlchemy
	OAUTH_CLIENT_ID = os.environ['OAUTH_CLIENT_ID']
	CLIENT_SECRET = os.environ['CLIENT_SECRET']
	CORS_HEADERS = 'Content-Type'

class LocalConfig(Config):
	DEBUG = True

class HerokuConfig(Config):
	DEBUG = False

class TestConfig(Config):
	SQLALCHEMY_DATABASE_URI = "postgresql://localhost/news_testing_db"
	TESTING = True
