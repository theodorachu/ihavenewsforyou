# ihavenewsforyou
Recommend articles that hold different perspectives from the current one

# Virtual Environment
Using Virtual Environment:
I'm using a virtual environment so you don't have to download anything. To start it AND initiate all environment variables, type:
1. source NewsProcessorServer/.env

# Setup for scraping RSS feeds
1. pip install feedparser
2. to install goose
mkvirtualenv --no-site-packages goose
git clone https://github.com/grangier/python-goose.git
cd python-goose
pip install -r requirements.txt
python setup.py install
3. pip install newspaper

# Setup for format corpus
sudo easy_install -U gensim

# All serving and scraping is done in NewsProcessorServer.
Check out the README there.

# Push to Heroku
1) Make sure that the virtual env is activated (so that our requirements file stays small)
2) pip freeze > requirements.txt
3) git push heroku master
4) heroku open (to open the website)

Random Stuff:
The migrations folder is a symbolic link.