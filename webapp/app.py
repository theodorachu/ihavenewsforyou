from flask import Flask, render_template, Markup
#from flask.ext.sqlalchemy import SQLAlchemy
from urllib2 import Request, urlopen, URLError
import os

#POSTGRES_URL = 'postgresql://localhost/pre-registration' #TODO: change this bc it's wrong

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URL
#app.config.from_pyfile('config.py')
#db = SQLAlchemy(app)

#from models import History

@app.route('/')
def homepage():
    author = "Me"
    name = "You"
    return render_template("index.html", author=author, name=name)

@app.route('/usage')
def ext_usage_chart():
    # how often you actually click on the extension
        # for every news site you visited in last month, what % of the time do you use extension
        # what % of the time do you navigate to an alternative article when you actually click on extension in last month
        # how many times per week do you use extension
    #hist = db.session.query(History).all()

    legend_ext = "How Often Extension is Used per News Site Visit"
    colors_ext = ["#04a35b", "#F7464A"]
    values_ext = [1, 2] #TODO: retrieve_from_db()
    labels_ext = ["Navigated Away Without Using Extension", "Clicked on Extension"]
        
    """
    ext_request = Request("https://across-the-aisle.herokuapp.com/%E2%80%9C/stats?weeksago=4")
    try:
        response = urlopen(ext_request)
        clickingstats = response.read()
        values_ext[1] = len(clickingstats)
    except URLError, e:
        print "can't query extension click stats"

    total_clicks = Request("https://across-the-aisle.herokuapp.com/%E2%80%9C/visits?weeksago=4")
    try:
        response = urlopen(total_clicks)
        visits = response.read()
        values_ext[0] = len(visits)-values_ext[0]
    except URLError, e:
        print "can't query visits"
    """

    legend_alt_art = "How Often Extension Article Recommendations are Read"
    colors_alt_art = colors_ext
    values_alt_art = [1, 2] #TODO: retrieve_from_db()
    labels_alt_art = ["Did Not Read Recommended Articles", "Read at Least One Recommended Article"]

    return render_template("ext_usage.html", legend_ext=legend_ext, colors_ext=colors_ext, values_ext=values_ext, labels_ext=labels_ext, legend_alt_art = legend_alt_art, colors_alt_art = colors_alt_art, values_alt_art = values_alt_art, labels_alt_art = labels_alt_art)

#def read_analysis_chart():

if __name__ == '__main__':
    app.run()

