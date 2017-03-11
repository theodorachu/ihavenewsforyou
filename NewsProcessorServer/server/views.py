from server import app, db #, login_manager
from models import Article, User, Visit, NewsSource
from db_helpers import dbExecute
from recommendArticles import BingSearch
from news_article import NewsArticle

from dateutil import parser as dateparser

from flask import render_template, request, redirect, url_for, flash
from apiclient import discovery
from oauth2client import client
import json
import random

import datetime
from sqlalchemy import and_
from flask_login import login_user, logout_user, current_user, login_required
from OAuthUtil import OAuthSignIn

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

LAST_WEEK = 1
LAST_MONTH = 4
LAST_YEAR = 52

@app.route('/')
def index():
	return render_template("index.html")

# @app.route('/friends')
# def get_friends():
# 	fbAuth = OAuthSignIn.get_provider('facebook').service
# 	return fbAuth.authorize(callback=url_for('friends_callback', 
# 																						provider='facebook',
# 																						_external=True))

# @app.route('/friends2')
# def friends_callback(provider):
# 	fbAuth = OAuthSignIn.get_provider(provider).service

# 	return render_template("friends.html")

@app.route('/test')
@login_required
def test():
	print OAuthSignIn.get_provider('facebook').getFriends()
	return render_template("index.html")


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, name = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(socialID=social_id).first()
    if not user:
        user = User(socialID=social_id, name=name)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

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
	values_alt_art[1] = numLinkFollows         
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
    if time == LAST_WEEK:   # TODO: extract this into external function
        size = 7
    elif time == LAST_MONTH:
        size = 28
    elif time == LAST_YEAR:
        size = 364
    else:
        raise ValueError("unexpected value for time parameter")

    today = datetime.datetime.today()

    # time spent per article
    # TODO: edit time spent to be hours and min (curr in secs)
    visits = Visit.query.all() #TODO: Filter by date
    total_time_spent = sum([visit.timeSpent for visit in visits])
    average_time_spent = total_time_spent / len(visits)
    average_min = int(average_time_spent/60)
    average_sec = int(average_time_spent % 60)

    # score for bias of articles
    #TODO

    # line graph for how frequently you read articles

    labels_article_frequency = [0]*size
    values_article_frequency = [0]*size
    for i in xrange(len(values_article_frequency)): # creates the array starting from present to past
        day = today - datetime.timedelta(days = i)
        visits_on_day = Visit.query.filter(and_(today - Visit.timeIn > datetime.timedelta(days=i-1), today - Visit.timeIn < datetime.timedelta(days=i+1))).all()
        values_article_frequency[i] = len(visits_on_day)
        labels_article_frequency[i] = day.strftime("%B %d, %Y")
    legend_article_frequency = "Num Articles Read Per Day"

    '''
    # show every article read in time frame
    visits_in_time_frame = Visit.query.filter(today - Visit.timeIn <= datetime.timedelta(days=size)).all()
    articles = []
    for visit in visits_in_time_frame:
        article = Article.query.filter(Article.url == visit.url).all()
        if article:
            articles.append(article[0].title)
        else:
            raise ValueError("Unexpected value error - article filter should return a value")
    labels_article_frequency = labels_article_frequency[::-1]
    values_article_frequency = values_article_frequency[::-1]
    '''

    articles = ['cnn','test2']
    return render_template("read_analysis.html",    
                                                    articles = articles,
                                                    average_time_spent = [average_min, average_sec],
                                                    labels_article_frequency = labels_article_frequency,
                                                    values_article_frequency = values_article_frequency,
                                                    legend_article_frequency = legend_article_frequency)

@app.route('/sources/<int:time>')
def source_analysis(time):
	legend_sources = "Sources Read"

	# QUERY DATABASE
	visits = Visit.query.all() #TODO: Filter by date 
	visit_data = []
	for i in xrange(min(len(visits), 50)): # TODO: Go through all the visits
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
	return render_template("source_analysis.html", 
																						legend_sources = legend_sources, 
																						colors_sources = colors_sources, 
																						values_sources = source_visit_values, 
																						labels_sources = sources)



################ BACKEND ROUTES ##################################################
################ BACKEND ROUTES ##################################################
################ BACKEND ROUTES ##################################################
################ BACKEND ROUTES ##################################################
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


@app.route('/is_news_source', methods=['GET'])
def checkWhetherURLIsForNewsSource():
	if 'url' not in request.values.keys():
		return createJSONResp(error="Missing url field")
	url = request.values['url']
	newsSourceOrigin = NewsSource.getSourceByURL(url)
	return json.dumps({'is_news_article': newsSourceOrigin != None})

@app.route('/visits', methods=['POST'])
def storeVisitBegun():
	print request.form
	fields = ['url', 'time', 'id', 'visitUpdateType']
	if areFieldsMissing(request, fields):
			return createJSONResp(error="missing field(s). fields are %s" % ','.join(fields))

	visitUpdateType = request.form['visitUpdateType'].lower()
	if visitUpdateType not in ['activate', 'suspend']:
		return createJSONResp(error='Invalid request change type: ' + visitUpdateType)
	url = request.form['url']
	timeStr = request.form['time']
	userID = request.form['id']
	success = True
	visit = Visit.getVisit(userID, url)

	if visit and not visitStateChangeIsConsistent(visit, visitUpdateType):
		return createJSONResp(error='Invalid request change type')

	# Visit created (or reactivated)
	if visitUpdateType == 'activate' and visit == None:
		visit = Visit(url, userID, timeStr)
		success = Visit.add(visit)
		# article = NewsArticle(url)
		# if (article.parse()):
		# 	Article.add(Article(article))
	elif visitUpdateType == 'activate' and visit:
		success = Visit.update(visit, {
			'state': 'active',
			'lastActiveTime': timeStr
		})

	# Visit suspended
	if visitUpdateType == 'suspend':
		additionalTime = (dateparser.parse(timeStr) - visit.lastActiveTime).total_seconds()
		success = Visit.update(visit, {
			'state': 'suspended',
			'lastActiveTime': timeStr,
			'timeOut': timeStr,
			'timeSpent': visit.timeSpent + additionalTime
		})

	if not success:
			return createJSONResp(error='Failed to add visit to db')
	return createJSONResp(success=True)

def visitStateChangeIsConsistent(visit, visitUpdateType):
	if visit.state == 'active':
		return visitUpdateType in ['suspend']
	if visit.state == 'suspended':
		return visitUpdateType in ['activate']
	return False



@app.route('/visit_ended', methods=['POST'])
def storeVisitEnded():
		fields = ['url', 'timeOut', 'id']
		if areFieldsMissing(request, fields):
				return createJSONResp(error="missing field(s). fields are %s" % ','.join(fields))

		visit = Visit.getVisit(request.form['id'], request.form['url'])
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




