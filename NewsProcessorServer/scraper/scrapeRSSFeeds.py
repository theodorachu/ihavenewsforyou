import feedparser as fp
import re
from BeautifulSoup import BeautifulSoup
from collections import defaultdict
import json
import newspaper
import sys


# The newspaper package requires that you download(), parse() and nlp() before getting information
# about the article. Since we are using the Python 2 module, it has a small bug where nlp() will start before
# the previous two steps have finished.
def setUpParsedArticle(parsedArticle):
	articleParsed = False
	loopCount = 0
	while not articleParsed:
		try:
			parsedArticle.download()
			parsedArticle.parse()
			parsedArticle.nlp()
			articleParsed = True
		except: # Something went wrong because the newspaper module is a little buggy. Try again!
			loopCount += 1
			if loopCount > 5:
				print 'The parser is looping due to a bug in the newspaper module. Try again'
				sys.exit()



class NewsArticle:
	def __init__(self, rssSummaryDetail, newsSource, url, bias='NONE'):
		# We will use the information in the article as parsed by the 'newspaper' package
		# whenever the rss feed does not have all the information we want.
		parsedArticle = newspaper.Article(url)
		setUpParsedArticle(parsedArticle)
		self.source = newsSource
		self.image = parsedArticle.top_image
		self.keywords = parsedArticle.keywords
		self.bias = bias

		if rssSummaryDetail:
			self.publishedDate = self._parsePublishDate(rssSummaryDetail)
			self.authors = self._parseAuthors(rssSummaryDetail, parsedArticle)
			self.title = rssSummaryDetail['title_detail']['value']
			self.url = url
			self.summary = self._parseArticleSummary(rssSummaryDetail, parsedArticle)
			self.tags = self._parseTags(rssSummaryDetail)
			self.text = self._extractArticleText(self.url, parsedArticle)
		else:
			self.publishedDate = str(parsedArticle.publish_date)
			self.authors = parsedArticle.authors
			self.title = parsedArticle.title
			self.url = url
			self.summary = parsedArticle.summary
			self.tags = []
			self.text = parsedArticle.text

		#ENCODE EVERYTHING IN UTF 6
		for k, v in self.__dict__.iteritems():
			if isinstance(v, unicode) or isinstance(v, str):
				self.__dict__[k] = v.encode('utf-8')


	def prettyPrint(self):
		print 'Title:', self.title
		print 'Source:', self.source
		print 'Published on:', self.publishedDate
		print 'Authored by:', ', '.join(self.authors)
		print 'Url:', self.url
		print 'Summary:', self.summary
		print 'Tags:', self.tags
		print 'Keywords:', self.keywords
		print 'Text:', self.text

	def _parsePublishDate(self, rssSummaryDetail):
		# TODO: Look into whether newspaper package collects this information
		if 'published' not in rssSummaryDetail: 
			return ""
		else:
			return  rssSummaryDetail['published']

	def _parseArticleSummary(self, rssSummaryDetail, parsedArticle):
		if 'summary' not in rssSummaryDetail: return parsedArticle.summary
		
		summary = BeautifulSoup(rssSummaryDetail['summary']).text # Strip the html tags that often appear in summaries
		if summary == '': return parsedArticle.summary
		return summary

	def _parseAuthors(self, rssSummaryDetail, parsedArticle):
		if 'author' in rssSummaryDetail and rssSummaryDetail['author'] != '':
			authorStr = rssSummaryDetail['author']
		else:
			return parsedArticle.authors
		authors = re.split(',|\s+and\s+', authorStr)
		return map(lambda name: name.strip(), authors)

	# PSA: Many rss feeds do not have tags! 
	def _parseTags(self, rssSummaryDetail):
		if 'tags' not in rssSummaryDetail: return []
		tags = []
		for infoBlock in rssSummaryDetail['tags']:
			tags.append(infoBlock['term'])
		return tags

	def _extractArticleText(self, url, parsedArticle):
		return parsedArticle.text

	# Feel free to change this hash function. We'd like to be unique per article.
	def hash(self):
		return self.title + ','.join(self.authors) + self.url


"""
Scrapes news articles from a list of rss feeds. 
Also keeps track of which fields are missing from which source.

Input: Dict of newsSource: RSS feed url
Ouput: Array of NewsArticles
"""
def scrapeNewsArticles(rssFeeds):
	overallParsingErrors = defaultdict(int)	
	articles = []
	for newsSource, url in rssFeeds.iteritems():
		parsingErrors = defaultdict(int)
		feed = fp.parse(url)
		for entry in feed['entries']:
			if len(articles) % 10 == 0: print len(articles), 'Articles Parsed'
			if 'link' in entry and entry['link'].endswith('.mp4'): continue
			article = NewsArticle(entry, newsSource, entry['link'])
			updateErrorCount(article, parsingErrors)
			updateErrorCount(article, overallParsingErrors)
			articles.append(article)
		print newsSource, 'has the following missing Fields'
		print parsingErrors
		print 'Num. Articles:', len(feed['entries'])

	print 'Overall missing fields:'
	print overallParsingErrors
	print "Num. Articles in total:", len(articles)
	return articles

def updateErrorCount(article, parsingErrors):
	if article.title == '': parsingErrors['title'] += 1
	if article.source == '': parsingErrors['source'] += 1
	if article.publishedDate == '': parsingErrors['publishedDate'] += 1
	if len(article.authors) == 0: parsingErrors['authors'] += 1
	if article.url == '': parsingErrors['url'] += 1
	if article.summary == '': parsingErrors['summary'] += 1
	if len(article.tags) == 0: parsingErrors['tags'] += 1
	if article.text == '': parsingErrors['text'] += 1
	if len(article.keywords) == 0: parsingErrors['keywords'] += 1
	if article.image == '': parsingErrors['image'] += 1

def scrapeRSSFeeds():
	rssFeedsPolitics = {
		'New York Times': 'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml',
		# 'Washington Post': 'http://feeds.washingtonpost.com/rss/politics', 
		# 'Fox News': 'http://feeds.foxnews.com/foxnews/politics?format=xml',
		# 'CNN': 'http://rss.cnn.com/rss/cnn_allpolitics.rss?ftm=xml',
		# 'WSJ': 'http://www.wsj.com/xml/rss/3_7087.xml',
		# 'Reuters': 'http://feeds.reuters.com/Reuters/PoliticsNews?ftm=xml',
		# 'ABC News': 'http://feeds.abcnews.com/abcnews/politicsheadlines',
		# 'CBS News': 'http://www.cbsnews.com/latest/rss/politics',
		# 'PBS': 'http://feeds.feedburner.com/pbs/qMdg',
		# 'USA Today': 'http://rssfeeds.usatoday.com/UsatodaycomWashington-TopStories',
		# 'The Hill': 'http://thehill.com/rss/syndicator/19109'

	}

	newsArticles = scrapeNewsArticles(rssFeedsPolitics)
	return newsArticles


if __name__ == '__main__':
	scrapeRSSFeeds()
