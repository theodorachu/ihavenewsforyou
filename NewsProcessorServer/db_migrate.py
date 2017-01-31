#!virtualenv/bin/python

import imp
from migrate.versioning import api
from server import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

"""
From the tutorial I got this script from:

The script looks complicated, but it doesn't really do much. 
The way SQLAlchemy-migrate creates a migration is by comparing the 
structure of the database (obtained in our case from file app.db) 
against the structure of our models (obtained from file app/models.py). 
The differences between the two are recorded as a migration script 
inside the migration repository. The migration script knows how to apply
a migration or undo it, so it is always possible to upgrade or downgrade 
a database format.

While I have never had problems generating migrations automatically with the
above script, I could see that sometimes it would be hard to determine what 
changes were made just by comparing the old and the new format. To make it 
easy for SQLAlchemy-migrate to determine the changes I never rename existing fields,
I limit my changes to adding or removing models or fields, or changing types of 
existing fields. And I always review the generated migration script to make sure it is right.

It goes without saying that you should never attempt to migrate your database
without having a backup, in case something goes wrong. Also never run a migration
for the first time on a production database, always make sure the migration works
correctly on a development database.
"""

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))