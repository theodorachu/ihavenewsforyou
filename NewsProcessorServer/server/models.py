from server import db #, login_manager
from db_helpers import dbExecute
from dateutil import parser as dateparser
from flask_login import UserMixin

class User(UserMixin, db.Model):
	__tablename__ = 'users'

	userID = db.Column(db.Integer, primary_key=True)
	# googleID = db.Column(db.String(64), nullable=False, unique=True)
	socialID = db.Column(db.String(64), nullable=False, unique=True)
	name = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True, unique=True)

	def __repr__(self):
		return '<User %r>' % (self.name)


class Visit(db.Model):
	__tablename__ = 'visits'

	url = db.Column(db.String(256), primary_key=True)
	userID = db.Column(db.Integer, primary_key=True)
	timeIn = db.Column(db.DateTime, primary_key=True)
	timeOut = db.Column(db.DateTime)
	receivedSuggestions = db.Column(db.Boolean)
	clickedSuggestion = db.Column(db.Boolean)

	def __init__(self, url, userID, timeIn, timeOut=None, receivedSuggestions=False, clickedSuggestion=False):
		self.url =  url
		self.userID = int(userID)
		self.timeIn = timeIn
		self.timeOut = timeOut
		self.receivedSuggestions = receivedSuggestions
		self.clickedSuggestion = clickedSuggestion

	@staticmethod
	def getMostRecentVisit(userID, url):
		return db.session.query(Visit) \
					.filter_by(userID=userID, url=url) \
					.order_by(Visit.timeIn.desc()).first()

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
								timeIn =visit.timeIn,
								url=visit.url
							) \
							.update(updateParams)
		success = dbExecute(updateCommand)
		return success

	@staticmethod
	def createVisitFromRequest(request):
		url = request.form['url']
		timeIn = dateparser.parse(request.form['timeIn'])
		userID = request.form['id']
		optionalParams = {}
		if 'timeOut' in request.form: optionalParams['timeOut'] = dateparser.parse(request.form['timeOut'])
		if 'receivedSuggestions' in request.form: optionalParams['receivedSuggestions'] = dateparser.parse(request.form['receivedSuggestions'])
		if 'clickedSuggestion' in request.form: optionalParams['clickedSuggestion'] = dateparser.parse(request.form['clickedSuggestion'])
		return Visit(url, userID, timeIn, **optionalParams)	


	def __repr__(self):
		return '<Visit %s>' % self.url


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
