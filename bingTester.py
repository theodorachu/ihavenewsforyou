from bingSearch import BingSearch
from corpusInterface import CorpusInterface
from pewExtractor import PewExtractor

corpusInterface = CorpusInterface()
contents = corpusInterface.extractContent()

bingSearch = BingSearch()
suggestions = bingSearch.get_suggestions(contents[0])

pewExtractor = PewExtractor()
suggestions_to_display = pewExtractor.get_ordering(contents[0]["source"], suggestions)

print contents[0]["source"]

# print suggestions_to_display
print [x['providers'] for x in suggestions_to_display]


