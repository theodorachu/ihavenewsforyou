# ihavenewsforyou
Recommend articles that hold different perspectives from the current one

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

# Push to Heroku
git subtree push --prefix NewsProcessorServer heroku master