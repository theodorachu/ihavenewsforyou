from server import db
from dateutil import parser as dateparser

class Article(db.Model):
	__tablename__ = 'articles'

	source = db.Column(db.String(128), primary_key=True)
	image = db.Column(db.String(128))
	bias = db.Column(db.String(64))
	publishedDate = db.Column(db.DateTime)
	url = db.Column(db.String(256))
	authors = db.Column(db.String(256))
	summary = db.Column(db.Text)
	title = db.Column(db.String(128), primary_key=True)
	text = db.Column(db.Text)

	def __init__(self, article):
		# Not included: tags, keywords
		self.source = article.source
		self.image = article.image
		self.bias = article.bias
		self.publish_date = dateparser.parse(article.publishedDate)
		self.url = article.url
		self.authors = ",".join(article.authors)
		self.summary = article.url
		self.title = article.title
		self.text = article.text



	def __repr__(self):
		return '<Article %s>' % (self.title.encode('utf-8'))

		# self.source = newsSource
		# self.image = parsedArticle.top_image
		# self.keywords = parsedArticle.keywords
		# self.bias = bias

		# if rssSummaryDetail:
		# 	self.publishedDate = self._parsePublishDate(rssSummaryDetail)
		# 	self.authors = self._parseAuthors(rssSummaryDetail, parsedArticle)
		# 	self.title = rssSummaryDetail['title_detail']['value']
		# 	self.url = url
		# 	self.summary = self._parseArticleSummary(rssSummaryDetail, parsedArticle)
		# 	self.tags = self._parseTags(rssSummaryDetail)
		# 	self.text = self._extractArticleText(self.url, parsedArticle)
		# else:
		# 	self.publishedDate = str(parsedArticle.publish_date)
		# 	self.authors = parsedArticle.authors
		# 	self.title = parsedArticle.title
		# 	self.url = url
		# 	self.summary = parsedArticle.summary
		# 	self.tags = []
		# 	self.text = parsedArticle.text