from bingSearch import BingSearch
from corpusInterface import CorpusInterface

corpusInterface = CorpusInterface()
contents = corpusInterface.extractContent()

bingSearch = BingSearch()
suggestions = bingSearch.get_suggestions(contents[0])


print contents[0]["source"]
print suggestions
print [x['providers'] for x in suggestions]


