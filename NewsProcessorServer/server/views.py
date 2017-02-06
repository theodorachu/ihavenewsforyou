from server import app
from scraper.scrapeRSSFeeds import scrapeRSSFeeds
from server import db
from models import Article

@app.route('/')
@app.route('/index')
def index():
	article = scrapeRSSFeeds()
	print article[0].title
	return "Hello, World!"

@app.route('/scrape', methods=['GET'])
def scrape_articles():
	articles = scrapeRSSFeeds()
	for article in articles:
		dbArticle = Article(article)
		print addToDB(article)
	for article in Article.query.all():
		print article
	return "Articles scraped!"

def addToDB(item):
	try:
		transaction = db.Session()
		transaction.add(item)
		transaction.commit()
	except:
		transaction.rollback()
		return False
	return True


