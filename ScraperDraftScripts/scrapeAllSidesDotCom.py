from pyquery import PyQuery as pq 
from scrapeRSSFeeds import NewsArticle
import json

"""
This script scrapes AllSidesDotCom. As of 2/1/17 it could use improvement - see the TODOs.
We scrape it using the following method:
	1) Get the list of top stories - one per day for the last few years
	2) Scrape the page of allides (e.g 'allsides/story/TOPIC') that corresponds to each url
		- We currently only get three stories per page. To fix this, we need to fix the scrapeAllSidesStoryPages() method.
	3) Dump it into a JSON file

"""

# AllSides has a page that lists out one top story per day. 
# This method returns the url's of all of the AllSides front pages which correspond to
# those stories. 
# Note that only one story gets added everday, so we really only need to scrape them once.
def getTopicURLs():
	jq = pq(url='http://www.allsides.com/story-list')
	topicStories = jq('.story-list-row')
	topicURLs = [] 
	for story in topicStories:
		topicURL = jq(story).find('.story-list-story').find('a').attr('href')
		topicURLs.append('http://www.allsides.com' + topicURL)
	return topicURLs



# This method scrapes the article. It gets 60 articles from the front page and 
# 60 articles from every "story page", e.g http://www.allsides.com/story/gorsuch-tapped-scotus
# TODO: Article might be opinion - we need to omit opinion pieces for now
def scrapeAllSidesFrontPage(url):
	jq = pq(url=url)
	newsStories = jq('.top-content-wrapper')
	sources = jq('.source-area')
	# sourceTypes = jq('div.type-of-content')

	biases = []
	articles = []
	for source, story in zip(sources, newsStories):
		print 'Scraped a story'
		url = jq(story).find('.news-title').find('a').attr('href')
		bias =  jq(source).find('.bias-image').find('img').attr('title')
		try:
			source = jq(source).find('.news-source').find('a').text()
			# The following line is commented out because pyquery ocassionally freaks out when getting text
			# TODO: Investigate
			# contentType = jq(source).find('div.type-of-content').text() 
		except:
			print 'exception'
			continue

		# if contentType != 'News: Facts': continue

		article = NewsArticle(None, source, url, bias)
		articles.append(article)
		break

	return articles

# We don't currently use this method. It is also not currently finished
# It exists because the "/story/TITLE" url at allsides has a different HTML format than the front page
def scrapeAllSidesStoryPages(url):
	jq = pq(url=url)
	print jq.innerHTML()
	allSideArticles = jq('li.articles')
	print len(allSideArticles)

	biases = []
	parsedArticles = []
	for article in articles:
		storyUrl = jq(article).find('a').attr('href')
		biasImageURL =  jq(source).find('.bias-image').attr('src')
		bias = chooseBiasFromURL(biasImageURL)

		return

		# article = NewsArticle()
		# articles.append((, bias))

	return parsedArticles

# Given an image url from AllSides, return the leaning the image shows
def chooseBiasFromURL(url):
	if 'leaning-left' in url: return 'leaning-left'
	if 'leaning-right' in url: return 'learning-right'
	if 'right' in url: return 'right'
	if 'left' in url: return 'left'
	if 'center' in url: return 'center'

if __name__ == '__main__':
	numToScrape = 300
	topicURLs = getTopicURLs() + ['http://www.allsides.com']
	articles = []
	for url in topicURLs:
		articles += scrapeAllSidesFrontPage(url)
		if len(articles) > numToScrape: break

	with open('allSidesArticles.json', 'w') as f:
		f.write(json.dumps([article.__dict__ for article in articles]))
