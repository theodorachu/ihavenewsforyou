import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from server import app, db

app.config.from_object(os.environ['APP_SETTINGS']) # Get the config settings, using the local APP_SETTINGS variable

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()