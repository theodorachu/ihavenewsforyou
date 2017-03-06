from server import app, db #, login_manager
from server.models import NewsSource
from server.news_article import NewsArticle

from dateutil import parser as dateparser
from pyquery import PyQuery as pq 
import json

"""
This script scrapes all the sources contained in all sides. Only need to run once.
"""

# Given an image url from AllSides, return the leaning the image shows
def chooseBiasFromURL(url):
	if 'leaning-left' in url: return -1
	if 'leaning-right' in url: return 1
	if 'right' in url: return 2
	if 'left' in url: return -2
	if 'center' in url: return 0
	return 0

def main():
	numPages = 3
	allSidesURLS = []
	for pageNum in range(numPages):
		allSidesSourcesJQ = pq(url='http://www.allsides.com/bias/bias-ratings?' + 'page=' + str(pageNum))
		newsSources = allSidesSourcesJQ('.source-title')
		for source in newsSources:
			sourceExtension = pq(source).find('a').attr('href')
			allSidesURLS.append('http://www.allsides.com' + sourceExtension)
	
	for url in allSidesURLS:
		newsInfoPage = pq(url=url)
		bias = chooseBiasFromURL(pq(newsInfoPage).find('.rating-area').find('img').attr('src'))
		sourceName = pq(newsInfoPage).find('.span8').find('h1').html()
		sourceURL = pq(newsInfoPage).find('.source-image').find('a').attr('href')
		print sourceName, bias
		source = NewsSource(name=sourceName, url=sourceURL, bias=bias, allSidesURL=url)
		NewsSource.add(source)

if __name__ == '__main__':
	main()
