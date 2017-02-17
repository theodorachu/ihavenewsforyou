from flask import Flask, render_template, Markup
#from flask.ext.sqlalchemy import SQLAlchemy
from urllib2 import Request, urlopen, URLError
import ast
import random
import os
import json

#POSTGRES_URL = 'postgresql://localhost/pre-registration' #TODO: change this bc it's wrong

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URL
#app.config.from_pyfile('config.py')
#db = SQLAlchemy(app)

#from models import History

COLOR_WHEEL = ['#000000', '#00FF00', '#0000FF', '#FF0000', '#01FFFE', '#FFA6FE', '#FFDB66', '#006401', \
'#010067', '#95003A', '#007DB5', '#FF00F6', '#FFEEE8', '#774D00', '#90FB92', '#0076FF', '#D5FF00',\
'#FF937E', '#6A826C', '#FF029D', '#FE8900', '#7A4782', '#7E2DD2', '#85A900', '#FF0056', '#A42400',\
'#00AE7E', '#683D3B', '#BDC6FF', '#263400', '#BDD393', '#00B917', '#9E008E', '#001544', '#C28C9F',\
'#FF74A3', '#01D0FF', '#004754', '#E56FFE', '#788231', '#0E4CA1', '#91D0CB', '#BE9970', '#968AE8',\
'#BB8800', '#43002C', '#DEFF74', '#00FFC6', '#FFE502', '#620E00', '#008F9C', '#98FF52', '#7544B1',\
'#B500FF', '#00FF78', '#FF6E41', '#005F39', '#6B6882', '#5FAD4E', '#A75740', '#A5FFD2', '#FFB167',\
'#009BFF', '#E85EBE']

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
    
    values_ext = [1, 2] #TODO: retrieve_from_db()
    colors_ext = list(map(lambda _: random.choice(COLOR_WHEEL), range(len(values_ext))))
    labels_ext = ["Navigated Away Without Using Extension", "Clicked on Extension"]
    print values_ext
        
    legend_alt_art = "How Often Extension Article Recommendations are Read"
    values_alt_art = [1, 2] #TODO: retrieve_from_db()
    colors_alt_art = list(map(lambda _: random.choice(COLOR_WHEEL), range(len(values_alt_art))))
    labels_alt_art = ["Did Not Read Recommended Articles", "Read at Least One Recommended Article"]
    
    ext_request = Request("https://across-the-aisle.herokuapp.com/stats?weeksago=4")
    try:
        response = urlopen(ext_request)
        clickingstats = response.read()
        clickingstats = ast.literal_eval(clickingstats)
        values_ext[1] = clickingstats["numExtensionClicks"]
        values_ext[0] = clickingstats["totalVisits"]
        values_alt_art[1] = clickingstats["numLinkFollows"]
        values_alt_art[0] = clickingstats["totalVisits"]-clickingstats["numLinkFollows"]
    except URLError, e:
        print "can't query extension click stats"
    
    return render_template("ext_usage.html", legend_ext=legend_ext, colors_ext=colors_ext, values_ext=values_ext, labels_ext=labels_ext, legend_alt_art = legend_alt_art, colors_alt_art = colors_alt_art, values_alt_art = values_alt_art, labels_alt_art = labels_alt_art)

@app.route('/reading')
def read_analysis():
    legend_sources = "Sources Read"
    visit_req = Request("https://across-the-aisle.herokuapp.com/visits?weeksago=4")
    try:
        response = urlopen(visit_req)
        visit_data = response.read()
        # visit_data = ast.literal_eval(visit_data)
        visit_data = json.loads(visit_data)
        for visit in visit_data:
            visit['source'] = str(visit['source'])
        sources = list(set([x["source"] for x in visit_data]))
        num_source_visits = {}
        for visit in visit_data:
            if visit["source"] in num_source_visits:
                num_source_visits[visit["source"]] += 1
            else:
                num_source_visits[visit["source"]] = 1
        source_visit_values = []
        for source in sources:
            source_visit_values.append(num_source_visits[source])
    except URLError, e:
        print "can't get visits data"
    colors_sources = list(map(lambda _: random.choice(COLOR_WHEEL), range(len(sources))))
    return render_template("read_analysis.html", legend_sources = legend_sources, colors_sources = colors_sources, values_sources = source_visit_values, labels_sources = sources)


if __name__ == '__main__':
    app.run()

