from server import db

class Article(db.Model):
	__tablename__ = 'articles'

	title = db.Column(db.String(128), primary_key=True)
	text = db.Column(db.Text)

	def __init__(self, article):
		self.title = article.title
		self.text = article.text

	def __repr__(self):
		return '<Article %s>' % (self.title)