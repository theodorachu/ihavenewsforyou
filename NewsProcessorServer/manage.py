import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import config
from server import app, db

"""
So you ask yourself - what the hell does this file do? Good question.
SOURCE OF TRUTH: https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/

Whenever you change the models in models.py, you need to do the following
1) python manage.py db migrate
2) python manage.py db upgrade

"""

app.config.from_object(os.environ['APP_SETTINGS']) # Get the config settings, using the local APP_SETTINGS variable

# Uncomment below when you need to create the test db
# app.config.from_object(os.environ['TEST_SETTINGS']) 

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()