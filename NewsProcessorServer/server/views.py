from server import app, db #, login_manager
from models import Article, User, Visit
from db_helpers import dbExecute
from recommendArticles import BingSearch
from news_article import NewsArticle

from dateutil import parser as dateparser

from flask import render_template, request
import httplib2
from apiclient import discovery
from oauth2client import client
import json
import random

"""
Docs:
1) Flask Login: 
		- https://flask-login.readthedocs.io/en/latest/
		- https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask
		- https://pythonhosted.org/Flask-Social/

"""
################ FRONTEND ROUTES ##################################################
COLOR_WHEEL = ['#000000', '#00FF00', '#0000FF', '#FF0000', '#01FFFE', '#FFA6FE', '#FFDB66', '#006401', \
'#010067', '#95003A', '#007DB5', '#FF00F6', '#FFEEE8', '#774D00', '#90FB92', '#0076FF', '#D5FF00',\
'#FF937E', '#6A826C', '#FF029D', '#FE8900', '#7A4782', '#7E2DD2', '#85A900', '#FF0056', '#A42400',\
'#00AE7E', '#683D3B', '#BDC6FF', '#263400', '#BDD393', '#00B917', '#9E008E', '#001544', '#C28C9F',\
'#FF74A3', '#01D0FF', '#004754', '#E56FFE', '#788231', '#0E4CA1', '#91D0CB', '#BE9970', '#968AE8',\
'#BB8800', '#43002C', '#DEFF74', '#00FFC6', '#FFE502', '#620E00', '#008F9C', '#98FF52', '#7544B1',\
'#B500FF', '#00FF78', '#FF6E41', '#005F39', '#6B6882', '#5FAD4E', '#A75740', '#A5FFD2', '#FFB167',\
'#009BFF', '#E85EBE']

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/usage')
@app.route('/usage/<int:time>')
def ext_usage_chart(time):
		# how often you actually click on the extension
				# for every news site you visited in last month, what % of the time do you use extension
				# what % of the time do you navigate to an alternative article when you actually click on extension in last month
				# how many times per week do you use extension

	legend_ext = "How Often Extension is Used per News Site Visit"
	
	values_ext = [1, 2] #TODO: retrieve_from_db()
	colors_ext = list(map(lambda _: random.choice(COLOR_WHEEL), range(len(values_ext))))
	labels_ext = ["Navigated Away Without Using Extension", "Clicked on Extension"]
			
	legend_alt_art = "How Often Extension Article Recommendations are Read"
	values_alt_art = [1, 2] #TODO: retrieve_from_db()
	colors_alt_art = list(map(lambda _: random.choice(COLOR_WHEEL), range(len(values_alt_art))))
	labels_alt_art = ["Did Not Read Recommended Articles", "Read at Least One Recommended Article"]

	# QUERY THE DATABASE
	visits = Visit.query.all() # TODO: Filter by date
	totalVisits = len(visits)
	numExtensionClicks = sum(int(v.receivedSuggestions) for v in visits)
	numLinkFollows = sum(int(v.clickedSuggestion) for v in visits)

		# RENDER THE DATA
	values_ext[0] = totalVisits
	values_ext[1] = numExtensionClicks
	values_alt_art[0] = totalVisits - numLinkFollows
	values_alt_art[1] = numTotalLinkFollows         
	return render_template("ext_usage.html", 
													legend_ext=legend_ext,
													colors_ext=colors_ext, 
													values_ext=values_ext, 
													labels_ext=labels_ext, 
													legend_alt_art = legend_alt_art, 
													colors_alt_art = colors_alt_art, 
													values_alt_art = values_alt_art, 
													labels_alt_art = labels_alt_art)

@app.route('/reading/<int:time>')
def read_analysis(time):
	legend_sources = "Sources Read"

	# QUERY DATABASE
	visits = Visit.query.all() #TODO: Filter by date 
	visit_data = []
	for i in xrange(50):
			v = visits[i]
			if "www" not in v.url:
					continue

			a = NewsArticle(v.url)
			try: 
					successfulParse = a.parse()
			except: 
					print v.url, "failed to be parsed"
					continue
			if not successfulParse: continue
			visit_data.append(dict(
					source=a.source,
					title=a.title,
					url=a.url
					))

	# RENDER THE DATA
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
	colors_sources = list(map(lambda _: random.choice(COLOR_WHEEL), range(len(sources))))
	return render_template("read_analysis.html", 
																						legend_sources = legend_sources, 
																						colors_sources = colors_sources, 
																						values_sources = source_visit_values, 
																						labels_sources = sources)


################ BACKEND ROUTES ##################################################

@app.route('/stats', methods=['GET'])
def stats():
  if 'weeksago' not in request.values.keys():
      return createJSONResp(error="Missing temporal field")

  visits = Visit.query.all() # TODO: Filter by date
  totalVisits = len(visits)
  numExtensionClicks = sum(int(v.receivedSuggestions) for v in visits)
  numLinkFollows = sum(int(v.clickedSuggestion) for v in visits)
  return json.dumps(dict(
      totalVisits=totalVisits,
      numExtensionClicks=numExtensionClicks,
      numLinkFollows=numLinkFollows
      ))

@app.route('/visits', methods=['GET'])
def visits():
  if 'weeksago' not in request.values.keys():
      return createJSONResp(error="Missing temporal field")   

  visits = Visit.query.all() #TODO: Filter by date 
  results = []
  for i in xrange(50):
      v = visits[i]
      if "www" not in v.url:
          continue

      a = NewsArticle(v.url)
      try: 
          successfulParse = a.parse()
      except: 
          print v.url, "failed to be parsed"
          continue
      if not successfulParse: continue
      results.append(dict(
          source=a.source,
          title=a.title,
          url=a.url
          ))
  return json.dumps(results)

@app.route('/recommend_articles', methods=['GET'])
def recommendArticles():
		if 'url' not in request.values.keys():
				return createJSONResp(error="Missing url field")
		article = NewsArticle(request.values['url'])
		successfulParse = article.parse()
		if not successfulParse:
				return createJSONResp(error='Failed to parse article')
		search = BingSearch()
		suggestions = search.get_suggestions(article)
		return json.dumps(suggestions)

@app.route('/login', methods=['POST'])
def login():
		pass
		# form = LoginForm()
		# if form.validate_on_submit():
		#   login_user(user)
		#   flask.flash('Logged in successfully')
		#   next = flask.request.args.get('next')
		#   if not is_safe_url(next):
		#       return flask.abort(400)
		#   return flask.redirect(next or flask.url_for('index'))
		# return flask.render_template('login.html', form=form)


@app.route('/visit_begun', methods=['POST'])
def storeVisitBegun():
		fields = ['url', 'timeIn', 'id']
		if areFieldsMissing(request, fields):
				return createJSONResp(error="missing field(s). fields are %s" % ','.join(fields))

		visit = Visit.createVisitFromRequest(request)
		success = Visit.add(visit)
		if not success:
				return createJSONResp(error='Failed to add visit to db')
		return createJSONResp(success=True)

@app.route('/visit_ended', methods=['POST'])
def storeVisitEnded():
		fields = ['url', 'timeOut', 'id']
		if areFieldsMissing(request, fields):
				return createJSONResp(error="missing field(s). fields are %s" % ','.join(fields))

		visit = Visit.getMostRecentVisit(request.form['id'], request.form['url'])
		success = Visit.update(visit, {'timeOut': dateparser.parse(request.form['timeOut'])})
		if not visit:
				return createJSONResp(error='Visit does not exist')
		if not success:
				return createJSONResp(error='Failed to update visit')
		return createJSONResp(success=True)

@app.route('/suggestion_clicked', methods=['POST'])
def suggestionClicked():
		fields = ['url', 'timeIn', 'id']
		if areFieldsMissing(request, fields):
				return createJSONResp(error="missing field(s). fields are %s" % ','.join(fields))

		visit = Visit.createVisitFromRequest(request)
		success = Visit.update(visit, {'clickedSuggestion': True})
		if not success:
				return createJSONResp('Failed to update visit')
		return createJSONResp(success=True)

@app.route('/suggestions_received', methods=['POST'])
def suggestionsReceived():
		fields = ['url', 'timeIn', 'id']
		if areFieldsMissing(request, fields):
				return createJSONResp(error="missing field(s). fields are %s" % ','.join(fields))

		visit = Visit.createVisitFromRequest(request)
		success = Visit.update(visit, {'receivedSuggestions': True})
		if not success:
				return createJSONResp('Failed to update visit')
		return createJSONResp(success=True)

############## HELPER METHODS #####################
def areFieldsMissing(request, fields):
		for field in fields:
				if field not in request.form.keys(): 
						return True
		return False

def createJSONResp(error=None, success=False):
		return json.dumps({'error': error, 'success': success})




