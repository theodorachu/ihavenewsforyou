import json
import requests

class BingSearch:

  def __init__(self):
    self.url = "https://api.cognitive.microsoft.com/bing/v5.0/news/search"
    self.key1 = "8175a289e9e143d589269678b9b4603c"
    self.key2 = "37dc1d03772e41fe936e91641d8dcc41"
    self.numArticles = 20
 
 # Argument: news articles in json format
  def get_suggestions(self, news_article):
    headers = {'Ocp-Apim-Subscription-Key': self.key1}

    query = " ".join(news_article["keywords"])
    payload = {'q': query, "count": self.numArticles} 

    r = requests.get(self.url, headers=headers, params=payload).json()
#    r.encoding = 'ascii'
    # TODO: "thumbnail" parameter for Brandon
    # print r["value"][0]["url"]
    # print r["value"][0]["name"]
    # print r["value"][0]["provider"][0]["name"]
    # print r["value"][0]["description"]

    suggestions = []
    for i in xrange(self.numArticles):
      entry = r["value"][i]
      providers = []
      for j in xrange(len(entry["provider"])):
        providers.append(entry["provider"][j]["name"])

      suggestions.append({
        "url": entry["url"],
        "title": entry["name"],
        "providers": providers,
        "description": entry["description"]
        })

    return suggestions




# bingSearch = BingSearch()
# bingSearch.get_suggestions({"keywords": ["hello", "world"]})







