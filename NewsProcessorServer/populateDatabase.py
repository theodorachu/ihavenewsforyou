from server import app, db #, login_manager
from server.models import Article, User, Visit, NewsSource 
from server.news_article import NewsArticle
import random
from datetime import datetime

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
  return 1

def addRandomVisit(user, url):
  yearStart = random.randint(2010, 2017)
  monthStart = random.randint(1, 12) 
  dayStart = random.randint(1, 28)
  hourStart = random.randint(0, 24 - 1) # inclusive
  secondStart = random.randint(0, 60 - 10)
  startDate = datetime(yearStart, monthStart, dayStart, hourStart, secondStart)

  yearEnd = random.randint(yearStart, 2017)
  monthEnd = random.randint(monthStart, 12)
  dayEnd = random.randint(dayStart, 28)
  hourEnd = random.randint(hourStart, 24 - 1)
  if (yearEnd == yearStart) and (monthEnd == monthStart) and (dayEnd == dayStart):
    secondStart = 0
  secondEnd = random.randint(secondStart + 1, 60 - 1)
  endDate = datetime(yearEnd, monthEnd, dayEnd, hourEnd, secondEnd)

  newVisit = Visit(url, user.id, startDate, endDate)
  success = newVisit.add(newVisit)
  if success:
    print("Visit added!")
    print(str(len(Visit.query.all())) + " visits added to the database.")
  else:
    print("Visit adding failed")

############################## SCRIPT CODE ############################

autofill = raw_input("Autofill database? [y/n]")

if autofill:
  left_urls = [
    "http://www.cnn.com/2017/03/23/politics/house-health-care-vote/index.html",
    "http://www.cnn.com/2017/03/14/politics/wiretapping-congressional-investigation/index.html",
    "http://www.newyorker.com/news/benjamin-wallace-wells/how-the-house-freedom-caucus-dominated-trump-on-health-care",
    "https://www.nytimes.com/interactive/2017/03/20/us/politics/health-care-whip-count.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=b-lede-package-region&region=top-news&WT.nav=top-news&_r=0",
    "https://www.nytimes.com/2017/03/23/us/politics/fact-check-trump-misleads-surveillance-wiretapping.html?rref=homepage&module=Ribbon&version=origin&region=Header&action=click&contentCollection=Home%20Page&pgtype=Multimedia",
    "https://www.nytimes.com/2017/03/23/us/politics/democrats-filibuster-neil-gorsuch-nomination.html?ribbon-ad-idx=4&rref=homepage&module=Ribbon&version=origin&region=Header&action=click&contentCollection=Home%20Page&pgtype=article",
    "https://www.nytimes.com/2017/03/23/world/europe/london-attack-victims-westminster-parliament.html?ribbon-ad-idx=4&rref=homepage&module=Ribbon&version=origin&region=Header&action=click&contentCollection=Home%20Page&pgtype=article",
    "https://www.nytimes.com/2017/03/23/us/election-fraud-voter-ids.html?ribbon-ad-idx=4&rref=homepage&module=Ribbon&version=origin&region=Header&action=click&contentCollection=Home%20Page&pgtype=article",
    "http://www.nbcnews.com/politics/congress/scheduled-health-care-vote-looms-house-gop-remains-short-support-n737491",
    "http://www.nbcnews.com/politics/white-house/white-house-comey-testimony-countering-trump-s-wiretap-claim-nothing-n735871",
    "http://www.nbcnews.com/politics/congress/these-are-republicans-opposing-trump-s-health-care-bill-n737116",
    "http://www.cnn.com/2017/02/13/politics/michael-flynn-white-house-national-security-adviser/index.html",
    "http://www.cnn.com/2017/03/23/politics/trump-health-care/index.html",
    "http://www.cnn.com/2017/03/14/politics/wiretapping-congressional-investigation/index.html",
    "http://www.cnn.com/2017/03/10/politics/counterintelligence-division-fbi-spy-catchers/index.html",
    "http://www.cnn.com/2017/03/09/politics/fbi-investigation-continues-into-odd-computer-link-between-russian-bank-and-trump-organization/index.html",
    "http://www.cnn.com/2017/03/09/politics/fbi-director-james-comey-meets-with-congress-gang-of-eight/index.html",
    "http://www.cnn.com/2017/03/07/politics/graham-russia-ukraine-poland-hearing/index.html",
    "http://www.cnn.com/2017/03/09/politics/general-votel-seal-raid-yemen-hearing/index.html",
    "http://www.cnn.com/2017/03/08/politics/marines-raqqa-assault-syria/index.html",
    "http://www.cnn.com/2017/03/23/politics/trump-health-care/index.html?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+rss%2Fcnn_allpolitics+%28RSS%3A+CNN+-+Politics%29",
    "http://www.cnn.com/2017/03/23/politics/house-health-care-vote/index.html?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+rss%2Fcnn_allpolitics+%28RSS%3A+CNN+-+Politics%29",
    "http://www.cnn.com/2017/03/23/politics/moderate-ryan-health-care/index.html?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+rss%2Fcnn_allpolitics+%28RSS%3A+CNN+-+Politics%29",
    "http://www.cnn.com/2017/03/23/politics/adam-schiff-trump-russia-grand-jury/index.html?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+rss%2Fcnn_allpolitics+%28RSS%3A+CNN+-+Politics%29"
  ]

  right_urls = [
    "http://www.foxnews.com/politics/2017/03/23/gop-leaders-delay-obamacare-replacement-vote-amid-opposition.html",
    "http://www.foxnews.com/politics/2017/03/23/potential-smoking-gun-showing-obama-administration-spied-on-trump-team-source-says.html",
    "http://www.foxnews.com/opinion/2017/03/23/karl-rove-first-real-test-new-republican-government.html",    
    "http://www.foxnews.com/politics/2017/03/23/senate-democrats-may-seek-deal-with-gop-to-confirm-gorsuch-stave-off-nuclear-option.html",
    "http://www.breitbart.com/big-government/2017/03/23/chaos-inside-gop-house-conference-forces-speaker-ryan-to-cancel-thursdays-ryancare-vote/",
    "http://www.breitbart.com/big-government/2017/03/23/polls-ryancare-even-unpopular-obamacare-hillarycare/",
    "http://www.breitbart.com/big-government/2017/03/23/koch-network-says-will-defend-republicans-vote-against-ahca/",
    "http://www.foxnews.com/world/2017/03/23/london-rampage-8-detained-on-suspicion-preparing-terror-attacks.html",
    "http://www.foxnews.com/world/2017/03/23/starving-venezuelans-dying-for-eating-poisonous-yuca-sold-in-black-market.html",
    "https://heatst.com/politics/ny-man-charged-with-faking-swastika-hate-crime-against-himself/",
    "http://www.foxnews.com/us/2017/03/23/authorities-find-veterans-decomposed-body-charge-3-family-members-with-collecting-his-benefits.html",
    "https://www.aol.com/article/finance/2017/03/22/20-hidden-sources-of-income-lying-around-your-house/21918888/?ncid=txtlnkusaolp00000058&",
    "http://www.foxnews.com/us/2017/03/23/wwii-vet-wins-300000-lottery-for-94th-birthday.html",
    "http://www.foxnews.com/us/2017/03/23/chiropractor-conned-medicare-private-insurers-in-10-million-scheme-feds-say.html",
    "http://insider.foxnews.com/2017/03/23/companies-bidding-contracts-build-donald-trumps-mexico-border-wall",
  ]

  def getRandomURLList(numUrls, left=True):
    url_list = left_urls if left else right_urls
    return [url_list[i] for i in random.sample(range(0, len(url_list)), numUrls)]

  names_url = {
    "Theodora Chu": getRandomURLList(6, True),
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




