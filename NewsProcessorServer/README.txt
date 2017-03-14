To Run:
1) source .env (you only need to do this once per opening of the terminal)
2) Set up the database (see below)
3) ./runFlaskServer.py

To Use the Database:
1) Download postgresql (I recommend using brew)
2) Create the database: createdb news_db
3) Instantiate the db:
	a) python manage.py db init
	b) python manage.py db migrate
	c) python manage.py db upgrade
	NOTE: you may need to run postgres -D /usr/local/var/postgres to get psql to start up
4) Whenever you change the models in models.py, run 3b) and 3c) to complete the migration
5) Type: psql news_db to examine the contents of the database
	- Type \dt. There should be 4 tables as of 2/13 - alembic, Visits, Users and Articles

Push to Heroku:
1) git commit as per usual
2) git push heroku master
NOTE: Things sometimes do not work on heroku that work locally. This is generally due to dependencies like python libraries or nltk_data. Definitely manually check that everything works after pushing to heroku.



LESS URGENT STUFF:
I used:
	1) https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world 
		- Theo, this has an angular tutorial in it
	2) https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
to learn Flask, PostgresSQL and Heroku.

Things to learn:
We are using SQLAlchemy to manage our database. And Alembic to manage migrations. You don't really need to learn Alembic (just follow the migration instructions). See docs: http://www.sqlalchemy.org/ to learn sqlalchemy.

HEROKU! Our app is called across-the-aisle
Set environment variables: heroku config:set VAR_NAME=VALUE -a across-the-aisle
Upgrade/migrate database: heroku run python NewsProcessorServer/manage.py db upgrade -a across-the-aisle

When pushing to Herok, remember:
1) python scrapeAllSides.py

Heroku Files
1) runtime.txt - specifies python version for heroku
2) Procfile - also for heroku

Are you annoyed by the "accept incoming network request dialogue"?
Follow this: http://stackoverflow.com/questions/19688841/add-python-to-os-x-firewall-options

