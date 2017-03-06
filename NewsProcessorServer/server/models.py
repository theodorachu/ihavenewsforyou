from server import db #, login_manager
from db_helpers import dbExecute
from dateutil import parser as dateparser
import re
class User(db.Model):
	__tablename__ = 'users'

	userID = db.Column(db.Integer, primary_key=True)
	googleID = db.Column(db.String(64), nullable=False, unique=True)
	name = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True, unique=True)

	def __repr__(self):
		return '<User %r>' % (self.name)


class Visit(db.Model):
	__tablename__ = 'visits'

	url = db.Column(db.String(256))
	userID = db.Column(db.Integer, primary_key=True)
	timeIn = db.Column(db.DateTime, primary_key=True)
	timeOut = db.Column(db.DateTime)
	lastActiveTime = db.Column(db.DateTime)
	state = db.Column(db.String(32))
	timeSpent = db.Column(db.Float)
	receivedSuggestions = db.Column(db.Boolean)
	clickedSuggestion = db.Column(db.Boolean)

	def __init__(self, url, userID, timeIn, timeOut=None, timeSpent=0.0, receivedSuggestions=False, clickedSuggestion=False):
		self.url =  url
		self.userID = int(userID)
		self.timeIn = timeIn
		self.timeOut = timeOut
		self.timeSpent = timeSpent
		self.lastActiveTime = timeIn
		self.state = 'active' #can be active, closed, suspended
		self.receivedSuggestions = receivedSuggestions
		self.clickedSuggestion = clickedSuggestion

	@staticmethod
	def getVisit(userID, url):
		return db.session.query(Visit) \
					.filter_by(userID=userID, url=url).first()

	@staticmethod
	def getByUserID(userID):
		visits = db.session.query(Visit).filter_by(userID=userID)
		return visits

	@staticmethod
	def add(visit):
		return dbExecute(lambda session: session.add(visit))

	@staticmethod
	def update(visit, updateParams):
		updateCommand = lambda session: session.query(Visit) \
							.filter_by(
								userID=visit.userID, 
								url=visit.url
							) \
							.update(updateParams)
		success = dbExecute(updateCommand)
		return success

	def __repr__(self):
		return '<Visit %s>' % self.url

class NewsSource(db.Model):
	__tablename__ = 'sources'

	name = db.Column(db.String(128), primary_key=True)
	url = db.Column(db.String(128))
	bias = db.Column(db.Integer)
	allSidesURL = db.Column(db.String(128))
	
	def __repr__(self):
		return '<NewsSource %s>' % self.name

	@staticmethod
	def add(source):
		return dbExecute(lambda session: session.add(source))

	@staticmethod
	def getSourceByURL(url):
		baseURLMatch = re.search('[\.a-z0-9A-Z]+.com', url)
		if baseURLMatch:
			url = baseURLMatch.group(0)
		print url
		source = db.session.query(NewsSource) \
			.filter(NewsSource.url.like("%" + url + "%"))
		if source: 
			return source.one()
		return None


class Article(db.Model):
	__tablename__ = 'articles'

	source = db.Column(db.String(128))
	image = db.Column(db.String(128))
	bias = db.Column(db.String(64))
	publishedDate = db.Column(db.DateTime)
	url = db.Column(db.String(256), primary_key=True)
	authors = db.Column(db.String(256))
	keywords = db.Column(db.String(256))
	summary = db.Column(db.Text)
	title = db.Column(db.String(128))
	text = db.Column(db.Text)

	def __init__(self, article):
		# Not included: tags, keywords
		self.source = article.source
		self.image = article.image
		self.bias = article.bias
		self.publish_date = dateparser.parse(article.publishedDate)
		self.url = article.url
		self.authors = ",".join(article.authors)
		self.keywords = ",".join(article.keywords)
		self.summary = article.url
		self.title = article.title
		self.text = article.text

	@staticmethod
	def add(article):
		return dbExecute(lambda session: session.add(article))

	def __repr__(self):
		return '<Article %s>' % (self.title.encode('utf-8'))
