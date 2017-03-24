from server import app, db #, login_manager
from server.models import Article, User, Visit, NewsSource 
from server.news_article import NewsArticle
from random import randint, random, sample
from datetime import datetime, timedelta
import json

def addArticle(url):
  article = Article.get(url)
  if not article:
    article = NewsArticle(url)
    successfulParse = article.parse()
    if not successfulParse:
      return 0

  # Add the article to database
    try: 
      Article.add(Article(article))
    except ValueError as err:
      # print "Failed to add " + url + " to article database."
      print "Error: {0}".format(err)
      return 0
    print "Added article to database!"
  else:
    print "Article already exists in database."
  return 1

def addRandomVisit(user, url, prob_sugg=0.7, prob_clicked=0.8):

  def getRandomDatetimePair(current):
    endDate = current - timedelta(days=randint(0, 30), 
                               hours=randint(0, 24),
                               minutes=randint(0, 60),
                               seconds=randint(0, 60))

    startDate = endDate - timedelta(days=randint(0, 2),
                                      hours=randint(0, 24),
                                      minutes=randint(0, 60),
                                      seconds=randint(0, 60))
    return startDate, endDate

  # Get start and end times
  startTime, endTime = getRandomDatetimePair(datetime.now())

  # Calculate time spent
  time_spent = int((endTime - startTime).total_seconds() * random())

  # Calculate whether we received or clicked on the suggestions or not
  receivedSuggestions = random() < prob_sugg
  clickedSuggestions = False
  if receivedSuggestions:
    clickedSuggestions = random() < prob_clicked

  newVisit = Visit(url, user.socialID, startTime, endTime, time_spent, receivedSuggestions, clickedSuggestions)
  success = Visit.add(newVisit)
  if success:
    print("Visit added!")
    print(str(len(Visit.query.all())) + " visits added to the database.")
  else:
    print("Visit adding failed")

############################## SCRIPT CODE ############################
def getURLsFromFile():
  filename = '../ScraperDraftScripts/allSidesArticles.json'
  right_urls = []
  left_urls = []
  center_urls = []
  with open(filename) as f:
    articles = json.load(f)
    for article in articles:
      bias = article["bias"].lower()
      if "right" in bias:
        right_urls.append(article["url"])
      if "left" in bias:
        left_urls.append(article["url"])
      else:
        center_urls.append(article["url"])
  return left_urls, center_urls, right_urls

if autofill:
  left_urls, center_urls, right_urls = getURLsFromFile()

  def getRandomURLList(numUrls, left=True):
    url_list = left_urls if left else right_urls
    return [url_list[i] for i in sample(range(0, len(url_list)), numUrls)]

  names_url = {
    "Theodora Chu": getRandomURLList(6, False),
    "Brandon Solis": getRandomURLList(8, True), 
    "Kenneth Xu": getRandomURLList(4, False),
    "Nathaniel Okun": getRandomURLList(7, True)
  }

  num_success_articles = 0
  for name in names_url.keys():
    user = User.query.filter_by(name=name).first()
    if not user:
      continue

    # Get visits
    for url in names_url[name]:
      addRandomVisit(user, url)
      num_success_articles += addArticle(url)
  print str(num_success_articles) + " articles added."

else:
  name = raw_input("Please enter User's name: ")
  user = User.query.filter_by(name=name).first()
  if not user:
    print "User does not exist in the database. Aborting."
    5/0

  while True:
    # Creates a visit from the URL
    url = raw_input("Visit URL: ")
    addRandomVisit(user, url)
    addArticle(url)




