from server import app
from scraper.scrapeRSSFeeds import scrapeRSSFeeds
from server import db
from models import Article

@app.route('/')
@app.route('/index')
def index():
	return "Hello, World!"

@app.route('/scrape', methods=['GET'])
def scrape_articles():
	articles = scrapeRSSFeeds()
	for article in articles:
		dbArticle = Article(article)
		print addToDB(dbArticle)
	for article in Article.query.all():
		print article
	return "Articles scraped!"

def addToDB(item):
	try:
		db.session.add(item)
		db.session.commit()
	except: #An error occurred
		db.session.rollback()
		return False
	return True


