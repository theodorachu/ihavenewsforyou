from server import app, db
from server.models import Article
from scraper.scrapeRSSFeeds import scrapeRSSFeeds

def scrapeArticles():
	articles = scrapeRSSFeeds()
	nonDuplicates = 0
	for article in articles:
		dbArticle = Article(article)
		nonDuplicates += addToDB(dbArticle)
	print nonDuplicates, "new articles out of", len(articles), "added to the database"

def addToDB(item):
	try:
		db.session.add(item)
		db.session.commit()
	except: #An error occurred
		db.session.rollback()
		return False
	return True

if __name__ == '__main__':
	scrapeArticles()