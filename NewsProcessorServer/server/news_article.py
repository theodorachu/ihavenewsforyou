import feedparser as fp
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import newspaper
import sys
import os
import re
from lxml.etree import XMLSyntaxError, DocumentInvalid 

NEWS_SOURCES = [
    'ourfuture',
    'shadowproof',
    'counterpunch',
    'dailykos',
    'democraticunderground',
    'crooksandliars',
    'thepoliticalcarnival',
    'alternet',
    'motherjones',
    'thenation',
    'thinkprogress',
    'progressive',
    'rollingstone',
    'prospect',
    'americanprogress',
    'salon',
    'msnbc',
    'mediamatters',
    'newrepublic',
    'businessinsider',
    'huffingtonpost',
    'thedailybeast',
    'foreignpolicy',
    'nationaljournal',
    'mediaite',
    'talkingpointsmemo',
    'theguardian',
    'ap',
    'nytimes',
    'bloomberg',
    'theweek',
    'msn',
    'reuters',
    'realclearpolitics',
    'bbc',
    'washingtonexaminer',
    'washingtonindependent',
    'aol',
    'aljazeera',
    'newser',
    'thehill',
    'politifact',
    'washingtonpost',
    'cnn',
    'economist',
    'ft',
    'politico',
    'slate',
    'theamericanconservative',
    'wsj',
    'forbes',
    'nationalreview',
    'foxnews',
    'freerepublic',
    'weeklystandard',
    'washingtontimes',
    'newsmax',
    'theblaze',
    'wnd',
    'breitbart',
    'esquire',
    'newyorker',
    'vanityfair',
    'newsweek',
    'time',
    'usnews',
    'rawstory',
    'nbcnews',
    'npr',
    'cnbc'    
  ]



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
		except XMLSyntaxError as e: # Something went wrong because the newspaper module is a little buggy. Try again!
			loopCount += 1
			if loopCount > 5:
				return False
		except:
			loopCount += 1
			if loopCount > 5:
				return False
	return True



class NewsArticle:
	def __init__(self, url):
		self.url = url

	def isNewsArticle(self):
		return 'cnn' in self.url

	def parse(self):
		parsedArticle = newspaper.Article(self.url)
		success = setUpParsedArticle(parsedArticle)
		if success:
			self.source = NewsArticle.parseSource(self.url)
			self.image = parsedArticle.top_image
			self.keywords = parsedArticle.keywords
			self.publishedDate = str(parsedArticle.publish_date)
			self.authors = parsedArticle.authors
			self.title = parsedArticle.title
			self.summary = parsedArticle.summary
			self.text = parsedArticle.text

			#ENCODE EVERYTHING IN UTF 6
			for k, v in self.__dict__.iteritems():
				if isinstance(v, unicode) or isinstance(v, str):
					self.__dict__[k] = v.encode('utf-8')
		return success

	@staticmethod
	def parseSource(url):
		sourceMatch = re.search('www\.([a-zA-Z0-9]+)\.com', url)
		if not sourceMatch:
			sourceMatch = re.search('([a-zA-Z0-9]+)\.com', url)
		if not sourceMatch: 
			return "unknown"
		return sourceMatch.group(1)

	@staticmethod
	def is_news_source(url):
		sourceMatch = re.search('www\.([a-zA-Z0-9]+)\.', url)
		if not sourceMatch:
			sourceMatch = re.search('([a-zA-Z0-9]+)\.', url)
		if not sourceMatch: 
			return False
		return (sourceMatch.group(1) in NEWS_SOURCES)





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

	# Feel free to change this hash function. We'd like to be unique per article.
	def hash(self):
		return self.title + ','.join(self.authors) + self.url

