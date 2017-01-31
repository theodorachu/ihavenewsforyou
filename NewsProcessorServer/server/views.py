from server import app
from flask import render_template

@app.route('/')
@app.route('/index')

# This doesn't serve any purpose yet. I'm just trying to learn Flask.
def index():
    user = {'nickname': 'Nathaniel'}
    return render_template('index.html',
                           title='Home',
                           user=user)