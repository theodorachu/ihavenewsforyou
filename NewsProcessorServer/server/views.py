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
from collections import defaultdict 

"""
Docs:
1) Flask Login: 
    - https://flask-login.readthedocs.io/en/latest  /
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
NUM_FRIENDS_TO_DISPLAY = 5

@app.route('/')
@app.route('/<int:time>')
def index(time=4):
  if current_user.is_authenticated:
    print current_user
    ext_data = ext_usage_chart(time)
    source_data = source_analysis(time) 
    read_data = read_analysis(time)
  else:
    ext_data = {}
    source_data = {}
    read_data = {}
  return render_template("index.html", ext=ext_data, source = source_data, read = read_data)

def getArticle(url):
  article = Article.get(url)
  if article is None:
    article = NewsArticle(url)
    successfulParse = article.parse()
    if not successfulParse:
      return None
  return article

@app.route('/friends')
@login_required
def friends():
  # Gets top 5 friends
  fb = OAuthSignIn.get_provider('facebook')
  friends = fb.getFriends()['data']
  friends_data = []
  for friend in friends[:NUM_FRIENDS_TO_DISPLAY]:
    name = friend['name']
    user_id = friend['id']
    social_id = user_id

    # Obtain user profile picture
    imgsrc = fb.getProfilePic(user_id)['data']['url']

    # Obtain user's visit information
    user = User.query.filter_by(socialID=social_id).first()
    if user is None:
      continue 
    visits = Visit.getByUserID(user.socialID)
    visit_urls = [visit.url for visit in visits]

    # Get the most recently read article
    most_recent_visit = sorted(visits, key=lambda x: x.timeOut)[-1]
    article = getArticle(most_recent_visit.url)
    most_recent_title = article.title if article else "N/A"
    most_recent_url = article.url if article else "#"

    # Get the top read source
    source_count = defaultdict(int) 
    for visit in visits:
      article = Article.get(visit.url)
      if not article:
        continue
      source_count[article.source] += 1

    best_source = max(source_count, key=source_count.get)
    friends_data.append({
      "name": name, 
      "imgsrc": imgsrc,
      "most_recent_title": most_recent_title,
      "most_recent_url": most_recent_url,
      "best_source": best_source
    })
  return friends_data

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
  if not current_user.is_anonymous:
    return redirect(url_for('index'))
  return OAuthSignIn.get_provider('facebook').authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    social_id, name = OAuthSignIn.get_provider('facebook').authorize_callback()
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
@login_required
def ext_usage_chart(time=4):
    # how often you actually click on the extension
        # for every news site you visited in last month, what % of the time do you use extension
        # what % of the time do you navigate to an alternative article when you actually click on extension in last month
        # how many times per week do you use extension

  legend_ext = "How Often Extension is Used per News Site Visit"
  
  values_ext = [1, 2]
  colors_ext = list(map(lambda _: random.choice(COLOR_WHEEL), range(len(values_ext))))
  labels_ext = ["Navigated Away Without Using Extension", "Clicked on Extension"]
      
  legend_alt_art = "How Often Extension Article Recommendations are Read"
  values_alt_art = [1, 2] #TODO: retrieve_from_db()
  colors_alt_art = list(map(lambda _: random.choice(COLOR_WHEEL), range(len(values_alt_art))))
  labels_alt_art = ["Did Not Read Recommended Articles", "Read at Least One Recommended Article"]


  # QUERY THE DATABASE
  visits = Visit.getByUserID(current_user.socialID) # TODO: Filter by date
  totalVisits = len(visits)
  numExtensionClicks = sum(int(v.receivedSuggestions) for v in visits)
  numLinkFollows = sum(int(v.clickedSuggestion) for v in visits)
  #friends_data = friends()
  friends_data = []

    # RENDER THE DATA
  values_ext[0] = totalVisits
  values_ext[1] = numExtensionClicks
  values_alt_art[0] = totalVisits - numLinkFollows
  values_alt_art[1] = numLinkFollows         

  return {'legend_ext':legend_ext, 'colors_ext': colors_ext, 'values_ext': values_ext, 'labels_ext': labels_ext,
            'legend_alt_art': legend_alt_art, 'colors_alt_art': colors_alt_art, 'values_alt_art': values_alt_art, 'labels_alt_art': labels_alt_art,
            'friends_data': friends_data}
  '''
  return render_template("ext_usage.html", 
                          legend_ext=legend_ext,
                          colors_ext=colors_ext, 
                          values_ext=values_ext, 
                          labels_ext=labels_ext, 
                          legend_alt_art = legend_alt_art, 
                          colors_alt_art = colors_alt_art, 
                          values_alt_art = values_alt_art, 
                          friends_data = friends())
  '''

@app.route('/reading/<int:time>')
@login_required
def read_analysis(time=4):
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
    visits = Visit.getByUserID(current_user.socialID)
    total_time_spent = sum([visit.timeSpent for visit in visits])
    average_time_spent = int(total_time_spent / len(visits) if len(visits) > 0 else 0)
    m, s = divmod(average_time_spent, 60)
    h, m = divmod(m, 60)
    if h > 0: average_time_spent_str = "%d hours %02d minutes %02d seconds" % (h, m, s)
    else: average_time_spent_str = "%02d minutes %02d seconds" % (m, s)

    # Set up article labels
    labels_article_frequency = [0]*size
    for i in xrange(len(labels_article_frequency)): # creates the array starting from present to past
        day = today - datetime.timedelta(days = i)
        labels_article_frequency[i] = day.strftime("%B %d, %Y")
    legend_article_frequency = "Num Articles Read Per Day"
    labels_article_frequency = labels_article_frequency[::-1]

    values_article_frequency = [0]*size
    url_dict = defaultdict(int)
    for visit in visits:
      # y-axis
      day = (today - visit.timeOut).days
      if day < size and day >= 0:
          values_article_frequency[size - 1 - day] += 1

      url_dict[visit.url] += 1
    # # Articles
    # article = Article.get(visit.url)
    # if article:
    #     articles.append(article.title)
    # else:
    #     articles.append(visit.url)
    read_data = {'num_articles': len(url_dict.keys()), 'average_time_spent_str': average_time_spent_str, 'labels_article_frequency': labels_article_frequency,
                'values_article_frequency': values_article_frequency, 'legend_article_frequency': legend_article_frequency}
    return read_data

    '''
    return render_template("read_analysis.html",    
            articles = articles,
            average_time_spent = [average_min, average_sec],
            labels_article_frequency = labels_article_frequency,
            values_article_frequency = values_article_frequency,
            legend_article_frequency = legend_article_frequency)
    '''

@login_required
@app.route('/sources/<int:time>')
def source_analysis(time=4):
    # QUERY DATABASE
    visits = Visit.getByUserID(current_user.socialID) #TODO: Filter by date 
    visit_data = []
    for visit in visits:
        article = Article.get(visit.url)
        if not article:
            article = NewsArticle(visit.url)
            successfulParse = article.parse()
            if not successfulParse: continue

        visit_data.append(dict(
            source=article.source,
            title=article.title,
            url=article.url
            ))

    # RENDER THE DATA
    sources = list(set([str(x["source"]) for x in visit_data]))
    source_visit_counts = []
    for i, source in enumerate(sources):
        source_visit_counts.append(0)
        for visit in visit_data:
            source_visit_counts[i] += visit['source'] == source

    colors_sources = list(map(lambda _: random.choice(COLOR_WHEEL), range(len(sources))))
    source_data = {'legend_sources': 'Sources Read', 'colors_sources': colors_sources, 'values_sources': source_visit_counts, 'labels_sources': sources}
    return source_data

    '''
    return render_template("source_analysis.html", 
        legend_sources = "Sources Read", 
        colors_sources = list(map(lambda _: random.choice(COLOR_WHEEL), range(len(sources)))), 
        values_sources = source_visit_counts, 
        labels_sources = sources)
    '''


################ BACKEND ROUTES ##################################################
################ BACKEND ROUTES ##################################################
################ BACKEND ROUTES ##################################################
################ BACKEND ROUTES ##################################################
################ BACKEND ROUTES ##################################################

@app.route('/stats', methods=['GET'])
def stats():
  if 'weeksago' not in request.values.keys():
      return createJSONResp(error="Missing temporal field")

  visits = Visit.getByUserID(current_user.socialID) # TODO: Filter by date
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

  visits = Visit.getByUserID(current_user.socialID) #TODO: Filter by date 
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
  article = Article.get(request.values['url'])
  if not article:
    article = NewsArticle(request.values['url'])
    successfulParse = article.parse()
    if not successfulParse:
        return createJSONResp(error='Failed to parse article')
  search = BingSearch()
  suggestions = search.get_suggestions(article)
  suggestions = filter(lambda x: x['url'] != request.values['url'], suggestions)
  return json.dumps(suggestions)


@app.route('/is_news_source', methods=['GET'])
def checkWhetherURLIsForNewsSource():
  if 'url' not in request.values.keys():
    return createJSONResp(error="Missing url field")
  url = request.values['url']
  newsSourceOrigin = NewsSource.getSourceByURL(url)
  return json.dumps({'is_news_article': newsSourceOrigin != None})

@app.route('/visits', methods=['POST'])
def storeVisitBegun():
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
  storedVisit = Visit.getVisit(userID, url)

  if storedVisit and not visitStateChangeIsConsistent(storedVisit, visitUpdateType):
    return createJSONResp(error='Invalid request change type')

  # Visit created (or reactivated)
  if visitUpdateType == 'activate' and storedVisit == None:
    newVisit = Visit(url, userID, timeStr)
    success = Visit.add(newVisit)
    article = NewsArticle(url)
    if (article.parse()):
      print "putting article in db"
      Article.add(Article(article))
  elif visitUpdateType == 'activate' and storedVisit:
    success = Visit.update(storedVisit, {
      'state': 'active',
      'lastActiveTime': timeStr
    })

  # Visit suspended
  if visitUpdateType == 'suspend':
    additionalTime = (dateparser.parse(timeStr) - storedVisit.lastActiveTime).total_seconds()
    success = Visit.update(storedVisit, {
      'state': 'suspended',
      'lastActiveTime': timeStr,
      'timeOut': timeStr,
      'timeSpent': storedVisit.timeSpent + additionalTime
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
        fields = ['url', 'id']
        if areFieldsMissing(request, fields):
                return createJSONResp(error="missing field(s). fields are %s" % ','.join(fields))

        visit = Visit.getVisit(request.form['id'], request.form['url'])
        success = Visit.update(visit, {'clickedSuggestion': True})
        if not success:
                return createJSONResp('Failed to update visit')
        return createJSONResp(success=True)

@app.route('/suggestions_received', methods=['POST'])
def suggestionsReceived():
    fields = ['url', 'id']
    if areFieldsMissing(request, fields):
            return createJSONResp(error="missing field(s). fields are %s" % ','.join(fields))
    visit = Visit.getVisit(request.form['id'], request.form['url'])
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




