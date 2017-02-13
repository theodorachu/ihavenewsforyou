import json
import requests
import random
import urllib2

# Table hardcoded from:
# https://www.washingtonpost.com/news/the-fix/wp/2014/10/21/lets-rank-the-media-from-liberal-to-conservative-based-on-their-audiences/?utm_term=.0df4726d156b
BIAS_TABLE = {
	'new yorker': 11,
	'slate': 11,
	'daily show': 10,
	'the guardian': 10,
	'al jazeera america': 10,
	'npr': 10,
	'colbert report': 10,
	'new york times': 10,
	'nytimes.com': 10,
	'buzzfeed': 9,
	'pbs': 9,
	'bbc': 9,
	'huffington post': 9,
	'washington post': 9,
	'the economist': 9,
	'politico': 9,
	'msnbc': 8,
	'cnn': 7,
	'nbc news': 6,
	'cbs news': 5,
	'google news': 5,
	'bloomberg': 5,
	'abc news': 5,
	'usa today': 5,
	'yahoo news': 4,
	'wall street journal': 4,
	'fox news': 3,
	'drudge report': 2,
	'breitbart': 1,
	'rush limbaugh show': 1,
	'the blaze': 1,
	'sean hannity show': 1,
	'glenn beck program': 1
}

class BingSearch:

	def __init__(self, numArticles=20, numSuggestions=3):
		self.url = "https://api.cognitive.microsoft.com/bing/v5.0/news/search"
		self.key1 = "8175a289e9e143d589269678b9b4603c"
		self.key2 = "37dc1d03772e41fe936e91641d8dcc41"
		self.numArticles = numArticles # from the Bing Search
		self.numSuggestions = numSuggestions
 
	@staticmethod
	def sanitizeSrc(s):
		return s.lower().strip()

	@staticmethod
	def getURLAfterRedirection(url):
		req = urllib2.Request(url)
		try:
			res = urllib2.urlopen(req)
		except:
			return url
		return res.geturl()

	@staticmethod
	# Gets the bias value of a given source
	def getSourceBias(src):
		src = BingSearch.sanitizeSrc(src)
		matches = [x for x in BIAS_TABLE.keys() if src.find(x) != -1]
		if len(matches) >= 1:
			return BIAS_TABLE[matches[0]]
		return -1
	
	# Gets the "bias difference" between current source and the entry
	def calcBiasDifference(self, entry, sourceBias):
		sugg_src = entry["providers"][0] # TODO: run through all the providers when querying?

		suggestedSourceBias = BingSearch.getSourceBias(sugg_src)
		if sourceBias >= 0:
			if suggestedSourceBias >= 0:
				return abs(sourceBias - suggestedSourceBias)
			else:
				return	-1

		return random.randint(0, self.numArticles)

 # Argument: NewsArticle class
	def get_suggestions(self, news_article):
		headers = {'Ocp-Apim-Subscription-Key': self.key1}
		query = " ".join(news_article.keywords)
		payload = {'q': query, "count": self.numArticles} 
		r = requests.get(self.url, headers=headers, params=payload).json()
#		r.encoding = 'ascii'
		# TODO: "thumbnail" parameter for Brandon
		# print r["value"][0]["url"]
		# print r["value"][0]["name"]
		# print r["value"][0]["provider"][0]["name"]
		# print r["value"][0]["description"]

		# Gets all the search results from Bing
		searchResults = []
		for i in xrange(min(self.numArticles, len(r["value"]))):
			entry = r["value"][i]
			providers = []
			for j in xrange(len(entry["provider"])):
				providers.append(entry["provider"][j]["name"])

			searchResults.append({
				"url": entry["url"],
				"title": entry["name"],
				"providers": providers,
				"description": entry["description"]
				})

		# Get the bias of the article you are currently on
		sourceBias = BingSearch.getSourceBias(BingSearch.sanitizeSrc(news_article.source))

		# Sort the suggestions and return the ones that are the most different
		sortedSearchResults = sorted(searchResults, key=lambda x: self.calcBiasDifference(x, sourceBias), reverse=True)
		finalSearchResults = [{
								'url': BingSearch.getURLAfterRedirection(searchResult['url']),
								'title': searchResult['title']
							  } for searchResult in sortedSearchResults]

		return finalSearchResults[:self.numSuggestions] 







