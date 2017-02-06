I used:
	1) https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world 
	2) https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
to learn Flask, PostgresSQL and Heroku.


To Use the Database:
1) Download postgresql (I recommend using brew)
2) Create the database: createdb article_db
3) Instantiate the db:
	a) python manage.py db init
	b) python manage.py db migrate
	c) python manage.py db upgrade
4) Whenever you change the models in models.py, run 3b) and 3c) to complete the migration
5) Type: psql article_db to examine the contents of the database


To Run:
1) source .env (you only need to do this once per opening of the terminal)
2) ./runFlaskServer.py


To Use the Database:
We are using SQLAlchemy. See docs: http://www.sqlalchemy.org/

Using Virtual Environment:
I'm using a virtual environment so you don't have to download anything. To start it AND initiate all environment variables, type
source .env

Weird files, but you have to know about them:
1) runtime.txt - specifies python version for heroku
2) Procfile - also for heroku
