from server import app, db
from models import Article

@app.route('/')
@app.route('/index')
def index():
	return "Hello, World!"


