from app import db

class History(db.Model):
    __tablename__ = 'webhist'

    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String())
    is_news_article = db.Column(db.Boolean)
    access_time = db.Column(db.DateTime())
    leave_time = db.Column(db.DateTime())
    source = db.Column(db.String())

    def __init__(self, url, is_news_article, access_time, leave_time, source):
        self.url = url
        self.is_news_article = is_news_article
        self.access_time = access_time
        self.leave_time = leave_time
        self.source = source

    def __repr__(self):
        return '<id {}>'.format(self.id)
