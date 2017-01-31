import feedparser as fp
import re
from goose import Goose
from BeautifulSoup import BeautifulSoup
from collections import defaultdict
import json
import urllib2

"""
Scrapers:
1) Scrapy
2) Newspaper (requires Python 3)
3) BeautifulSoup
"""

"""
Resources:
1) Scrape with Scrapy: https://www.smallsurething.com/web-scraping-article-extraction-and-sentiment-analysis-with-scrapy-goose-and-textblob/
2) Web crawler with scrapy: https://blog.siliconstraits.vn/building-web-crawler-scrapy/
3) Goose documentation: https://github.com/grangier/python-goose
"""


class NewsArticle:
	def __init__(self, rssSummaryDetail, newsSource):
		self.source = newsSource
		self.publishedDate = self._parsePublishDate(rssSummaryDetail)
		self.authors = self._parseAuthors(rssSummaryDetail)
		self.title = rssSummaryDetail['title_detail']['value']
		self.url = rssSummaryDetail['link']
		self.summary = self._parseArticleSummary(rssSummaryDetail)
		self.tags = self._parseTags(rssSummaryDetail)
		self.text = self._extractArticleText(self.url)

	# Required for JSON dump
	def toJSON(self):
		return json.dumps(self, default=lambda article: article.__dict__, indent=4)

	def prettyPrint(self):
		print 'Title:', self.title
		print 'Source:', self.source
		print 'Published on:', self.publishedDate
		print 'Authored by:', ', '.join(self.authors)
		print 'Url:', self.url
		print 'Summary:', self.summary
		print 'Tags:', self.tags
		print 'Text:', self.text

	def _parsePublishDate(self, rssSummaryDetail):
		if 'published' not in rssSummaryDetail: 
			return ""
		else:
			return  rssSummaryDetail['published']
	def _parseArticleSummary(self, rssSummaryDetail):
		if 'summary' not in rssSummaryDetail: return ''
		# Strip the html tags that often appear in summaries
		summary = BeautifulSoup(rssSummaryDetail['summary']).text
		return summary

	def _parseAuthors(self, rssSummaryDetail):
		if 'author' in rssSummaryDetail:
			authorStr = rssSummaryDetail['author']
		elif 'authors' in rssSummaryDetail:
			authorStr = rssSummaryDetail['authors']
		else:
			return ""

		authors = re.split(',|\s+and\s+', authorStr)
		return map(lambda name: name.strip(), authors)

	def _parseTags(self, rssSummaryDetail):
		if 'tags' not in rssSummaryDetail: return []
		tags = []
		for infoBlock in rssSummaryDetail['tags']:
			tags.append(infoBlock['term'])
		return tags

	def _extractArticleText(self, url):
		extractor = Goose()
		try:
			article = extractor.extract(url=url)
		except:
			article = None
		if article == None or len(article.cleaned_text) == 0:
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
			raw_html = opener.open(url).read()
			article = extractor.extract(raw_html)

		return article.cleaned_text if article else ""



def scrapeNewsArticles(rssFeeds):
	articles = []
	for newsSource, url in rssFeeds.iteritems():
		parsingErrors = {
			'title': 0,
			'source': 0,
			'publishedDate': 0,
			'authors': 0,
			'url': 0,
			'summary': 0,
			'tags': 0,
			'text': 0
		}	
		feed = fp.parse(url)
		for entry in feed['entries']:
			if len(articles) % 10 == 0: print len(articles), 'Articles Parsed'
			if 'link' in entry and entry['link'].endswith('.mp4'): continue
			article = NewsArticle(entry, newsSource)
			updateErrorCount(article, parsingErrors)
			articles.append(article)
		print newsSource, 'Missing Fields'
		print parsingErrors
		print 'Num. Articles:', len(feed['entries'])
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

def main():
	rssFeedsPolitics = {
		'New York Times': 'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml', # goose cannot scrape from NYT
		# # 'Washington Post': 'http://www.washingtonpost.com/news-politics-sitemap.xml', # doesn't work
		# 'Fox News': 'http://feeds.foxnews.com/foxnews/politics?format=xml',
		# 'CNN': 'http://rss.cnn.com/rss/cnn_allpolitics.rss?ftm=xml',
		# 'WSJ': 'http://www.wsj.com/xml/rss/3_7087.xml',
		# 'Reuters': 'http://feeds.reuters.com/Reuters/PoliticsNews?ftm=xml'
	}

	newsArticles = scrapeNewsArticles(rssFeedsPolitics)
	print len(newsArticles)
	with open('newsArticles.json', 'w') as f:
		json.dump([article.__dict__ for article in newsArticles], f)



if __name__ == '__main__':
	main()
